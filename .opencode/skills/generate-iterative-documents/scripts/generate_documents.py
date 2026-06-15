#!/usr/bin/env python3
"""Render SRS/SD DOCX and populate STC XLSX from confirmed JSON input."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

from docxtpl import DocxTemplate
from openpyxl import load_workbook


def clean(value):
    return "" if value is None else str(value).strip()


def context(data, kind):
    iteration = clean(data.get("iteration_name"))
    code = clean(data.get("iteration_code")) or iteration.replace("迭代", "")
    requirements = data.get("requirements", [])
    revisions = data.get("revisions", [])
    if kind == "srs":
        section = data.get("srs", {})
        return {
            "HEADER": f"UnionSV110 {iteration}软件需求规格说明书",
            "TITLE_CN": f"UnionSV110 {iteration}需求软件规格说明书",
            "TITLE_EN": f"UnionSV110 {code} Iteration Software Requirement Specification",
            "PURPOSE": clean(section.get("purpose")),
            "SCOPE": clean(section.get("scope")),
            "OVERVIEW": clean(section.get("overview")),
            "SOFTWARE_FUNCTIONS": clean(section.get("software_functions")),
            "DESIGN_CONSTRAINTS": clean(section.get("design_constraints")),
            "PERFORMANCE_SUMMARY": clean(section.get("performance_summary")),
            "QUALITY_SUMMARY": clean(section.get("quality_summary")),
            "TESTABILITY_SUMMARY": clean(section.get("testability_summary")),
            "requirements": requirements,
            "revisions": revisions,
        }
    section = data.get("sd", {})
    return {
        "HEADER": f"UnionSV110 {iteration}需求软件设计说明书",
        "TITLE_CN": f"UnionSV110 {iteration}需求软件设计说明书",
        "TITLE_EN": f"UnionSV110 {code} Iterative Requirements Development Software Design Specification",
        "ITERATION_REQUIREMENT": f"{code}需求",
        "PURPOSE": clean(section.get("purpose")),
        "SCOPE": clean(section.get("scope")),
        "SOFTWARE_FUNCTIONS": clean(section.get("software_functions")),
        "designs": requirements,
        "revisions": revisions,
    }


def render_docx(template, output, values):
    doc = DocxTemplate(template)
    doc.render(values, autoescape=True)
    doc.save(output)


def safe_filename(value):
    return re.sub(r'[\\/:*?"<>|]+', "_", value).strip() or "iteration"


def populate_stc(template, output, data):
    wb = load_workbook(template)
    required = {"统计", "缺陷记录&测试报告"}
    missing = required.difference(wb.sheetnames)
    if missing:
        raise ValueError(f"STC template missing sheets: {', '.join(sorted(missing))}")
    ws = wb["缺陷记录&测试报告"]
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)
    cases = []
    for requirement in data.get("requirements", []):
        for case in requirement.get("test_cases", []):
            row = [
                clean(case.get("id")), clean(case.get("type")), clean(case.get("item")),
                clean(case.get("title")), clean(case.get("priority")), clean(case.get("precondition")),
                clean(case.get("input")), clean(case.get("steps")), clean(case.get("expected")),
                clean(case.get("execution")), clean(case.get("remarks")) or clean(requirement.get("ar")),
            ]
            if any(row):
                cases.append(row)
                ws.append(row)
    stats = wb["统计"]
    if stats.max_row:
        stats.delete_rows(1, stats.max_row)
    stats.append(["统计项", "数量"])
    stats.append(["用例总数", len(cases)])
    priorities = Counter(row[4] for row in cases)
    for priority in ("H", "M", "L"):
        stats.append([priority, priorities[priority]])
    types = Counter(row[1] for row in cases)
    for case_type in sorted(types):
        stats.append([case_type, types[case_type]])
    wb.save(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--srs-template", required=True, type=Path)
    parser.add_argument("--sd-template", required=True, type=Path)
    parser.add_argument("--stc-template", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = safe_filename(clean(data.get("iteration_code")) or clean(data.get("iteration_name")))
    outputs = {
        "srs": args.output_dir / f"{stem}-SRS.docx",
        "sd": args.output_dir / f"{stem}-SD.docx",
        "stc": args.output_dir / f"{stem}-STC.xlsx",
    }
    render_docx(args.srs_template, outputs["srs"], context(data, "srs"))
    render_docx(args.sd_template, outputs["sd"], context(data, "sd"))
    populate_stc(args.stc_template, outputs["stc"], data)
    for path in outputs.values():
        print(path)


if __name__ == "__main__":
    main()

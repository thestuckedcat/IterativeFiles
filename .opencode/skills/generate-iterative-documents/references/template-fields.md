# 模板字段

## SRS DOCX

标量：`TITLE_CN`、`TITLE_EN`、`HEADER`、`PURPOSE`、`SCOPE`、`OVERVIEW`、`SOFTWARE_FUNCTIONS`、`DESIGN_CONSTRAINTS`、`PERFORMANCE_SUMMARY`、`QUALITY_SUMMARY`、`TESTABILITY_SUMMARY`。

循环 `requirements`：`title`、`ar`、`introduction`、`input`、`processing`、`output`、`external_dependencies`、`performance`、`quality`、`testability`。

循环 `revisions`：`date`、`version`、`description`、`author`。

## SD DOCX

标量：`TITLE_CN`、`TITLE_EN`、`HEADER`、`ITERATION_REQUIREMENT`、`PURPOSE`、`SCOPE`、`SOFTWARE_FUNCTIONS`。

循环 `designs`：`title`、`ar`、`background`、`detailed_design`、`constraints`、`external_interface_link`。空的可选小节不输出。

循环 `revisions`：`date`、`version`、`ar`、`section`、`description`、`author`。

## STC XLSX

页签 `缺陷记录&测试报告` 的列依次为：测试用例编号、用例类型、测试项、测试用例标题、重要级别、预置条件、输入、操作步骤、预期结果、用例执行情况、备注。

页签 `统计` 汇总总数、H/M/L 级别数及各用例类型数量。

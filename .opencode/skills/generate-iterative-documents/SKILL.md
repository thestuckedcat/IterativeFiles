---
name: generate-iterative-documents
description: 通过结构化头脑风暴收集 UnionSV110 迭代需求，生成 SRS 软件需求规格说明书、SD 软件设计说明书（docxtpl/DOCX）和 STC 测试用例（openpyxl/XLSX）。当用户要求编写、补全或从需求/API/AR 信息生成这三类迭代文档，或要求把需求澄清结果写入对应模板时使用。
compatibility: opencode
metadata:
  language: zh-CN
  domain: requirements-engineering
  outputs: srs-docx,sd-docx,stc-xlsx
---

# UnionSV110 迭代文档生成

## What I do

- 使用 OpenCode 内置 `question` 工具逐步澄清迭代、AR、接口、边界和测试需求。
- 将确认信息整理为 JSON，再调用 Python 脚本生成 SRS、SD 和 STC。
- 保持 DOCX 自动填入内容为红色，跳过不涉及字段，并在必要位置提示补充图表。

## When to use me

用户要求分析 UnionSV110 迭代需求、编写或补全 SRS/SD/STC、根据 AR/API 生成文档，或把需求澄清结果写入 DOCX/XLSX 模板时使用。

## OpenCode tool usage

1. 先用 `glob` 定位当前已加载 skill 的 `SKILL.md`，其目录记为 `SKILL_DIR`。项目安装的标准位置是 `.opencode/skills/generate-iterative-documents`。
2. 开始提问前必须用 `read` 读取字段语义契约，再按需读取其他资料：
   - `$SKILL_DIR/references/template-fields.md`
   - `$SKILL_DIR/references/docx-template-example.md`（创建或迁移正式 DOCX 模板时读取）
   - `$SKILL_DIR/references/brainstorming.md`
   - `$SKILL_DIR/references/input-schema.json`
3. 需要用户决策时调用 OpenCode 的 `question` 工具。每次只问一个主题；不要在普通文本中一次列出整套问卷。
4. 每个允许缺省的问题提供：
   - `A. 不涉及`
   - `B. 当前不清楚`
   - `C. 继承需求，参考以往`
   - 用户直接输入自定义答案即为 `D. 用户输入`，这是默认推荐路径。
5. 需要创建 JSON 或执行脚本时使用 `write`/`edit` 与 `bash`。不要假定当前工作目录就是 skill 目录，命令中使用定位到的 `SKILL_DIR`。

## 工作流

1. 按 `references/brainstorming.md` 的阶段顺序提问。先询问迭代名，再逐个 AR 深挖；确认没有更多 AR 后才反向总结简介。
2. 每轮复述已确认内容，并只提出当前最关键的一个问题。用户已提供的信息不要重复询问。
3. 按 `references/template-fields.md` 的“JSON 路径 → 模板变量”契约逐字段整理成 `references/input-schema.json` 所示结构。保留用户原意，不臆造 API、参数、芯片行为、错误码或期望结果。
4. 选择 A 时写入空字符串；选择 B 时写入“当前不清楚”；选择 C 时写入“继承需求，参考以往文档”并继续询问具体参考；自定义答案按确认内容写入。
5. 如果明显需要流程图、时序图、接口表、参数表或边界值表，在对应正文追加 `【建议加入表格/图片辅助说明】`。
6. 在执行生成前，执行 `references/template-fields.md` 的字段审计，再使用 `question` 汇总展示字段映射、待确认项并取得用户确认。
7. 仓库不提交 DOCX/XLSX 二进制模板。先检查 Python 依赖；缺失时征得用户同意后，通过 `bash` 安装 `$SKILL_DIR/requirements.txt`。首次使用或资产缺失时，在本地创建模板，再生成文档：

```bash
python "$SKILL_DIR/scripts/create_example_templates.py"
python "$SKILL_DIR/scripts/generate_documents.py" \
  --input requirements.json \
  --srs-template "$SKILL_DIR/assets/srs-template.docx" \
  --sd-template "$SKILL_DIR/assets/sd-template.docx" \
  --stc-template "$SKILL_DIR/assets/stc-template.xlsx" \
  --output-dir output
```

8. 打开生成结果做最终检查：所有自动填入 DOCX 的文本必须为红色；不涉及的字段不得出现；STC 两个指定页签必须存在且统计公式/数值已刷新。
9. 向用户列出生成文件、仍为“当前不清楚”的问题、继承项引用以及建议补图/表的位置。

## 文档规则

- SRS 页眉：`UnionSV110 <迭代名>软件需求规格说明书`，宋体、小五。
- SD 页眉：`UnionSV110 <迭代名>需求软件设计说明书`，宋体、小五。
- DOCX 中所有模板替换内容标红，供人工逐项审查后改黑。
- 空字段不输出标题或占位文本。
- STC 只修改 `统计` 和 `缺陷记录&测试报告` 页签；测试用例从驱动边界输入、LCNE 边界、芯片边界和 API 定义推导，正常与异常场景都要覆盖。
- 不把“当前不清楚”伪装为已确定内容；信息不足以生成可执行用例时先继续追问。

## 资源

- `references/brainstorming.md`：逐步提问策略、SRS/SD/STC 检查点。
- `references/template-fields.md`：DOCX 字段和 XLSX 列定义。
- `references/docx-template-example.md`：可直接复制到 Word 的 SRS/SD docxtpl 变量、段落循环、条件块和修订表格示例。
- `references/input-schema.json`：生成脚本输入示例及数据结构。
- `requirements.txt`：文档生成脚本的 Python 依赖。
- `scripts/create_example_templates.py`：创建可迁移字段的示例 DOCX/XLSX 模板。
- `scripts/generate_documents.py`：渲染 SRS、SD 并填充 STC。
- `assets/`：本地生成的示例模板输出目录（DOCX/XLSX 被 `.gitignore` 忽略）；用户提供正式模板后优先使用正式模板。

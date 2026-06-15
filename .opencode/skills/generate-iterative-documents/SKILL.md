---
name: generate-iterative-documents
description: 通过结构化头脑风暴收集 UnionSV110 迭代需求，生成 SRS 软件需求规格说明书、SD 软件设计说明书（docxtpl/DOCX）和 STC 测试用例（openpyxl/XLSX）。当用户要求编写、补全或从需求/API/AR 信息生成这三类迭代文档，或要求把需求澄清结果写入对应模板时使用。
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
3. 需要用户决策时调用 OpenCode 的 `question` 工具。每次只问一个当前最关键的主题；题干尽量控制在一句短句中，必要背景放在提问前的简短归纳里，不照抄固定问卷。
4. 选项必须针对当前上下文动态生成，通常提供 2–3 个互斥的常见答案。OpenCode 框架会自动添加用户自由输入选项，因此**不得**再手工添加“用户输入”“其他”“自定义”等选项。
5. 只有确实适用时才提供“不涉及”“当前不清楚”或“继承既有需求”等缺省选项；不得把同一组缺省选项机械地附加到每个问题。
6. 需要创建 JSON 或执行脚本时使用 `write`/`edit` 与 `bash`。不要假定当前工作目录就是 skill 目录，命令中使用定位到的 `SKILL_DIR`。

## 工作流

1. 参考 `references/brainstorming.md` 的阶段目标推进，而不是逐条照读问题清单。先从用户现有材料中提取已知信息和缺口；通常先确认迭代标识，再逐个 AR 深挖；确认没有更多 AR 后才反向总结简介。
2. 每轮先理解并归纳用户刚才的回答：去除口语重复，合并前后文，区分“已确认事实 / 合理但未确认的理解 / 待确认项”。向用户展示一段简短的结构化理解后，只问会显著推进文档的一个问题。不得原样把用户回答直接塞入文档字段，也不得重复询问用户已经提供的信息。
3. 如果回答模糊，先结合上下文推断用户意图并用简短复述请求确认；只有影响字段含义、实现边界或测试判定时才追问。不要为了走完清单而追问低价值细节。
4. 按 `references/template-fields.md` 的“JSON 路径 → 模板变量”契约逐字段整理成 `references/input-schema.json` 所示结构。写入的是经用户确认的归纳结果，而非聊天原文；保留用户原意，不臆造 API、参数、芯片行为、错误码或期望结果。
5. 用户选择“不涉及”时写入空字符串；选择“当前不清楚”时写入“当前不清楚”；选择“继承既有需求”时记录用户确认的具体参考来源，尚无来源则列为待确认项。
6. 如果明显需要流程图、时序图、接口表、参数表或边界值表，在对应正文追加 `【建议加入表格/图片辅助说明】`。
7. 在执行生成前，执行 `references/template-fields.md` 的字段审计，再使用 `question` 汇总展示归纳后的字段映射、待确认项并取得用户确认。
8. **用户模板具有最高优先级。** 用户提供模板时，必须读取并沿用其文件、版式、章节、页签、字段和既有内容；即使发现问题，也只能指出风险并询问用户是否允许调整，不能擅自改用 skill 示例模板、重建模板或改变模板结构。若现有脚本与用户模板不兼容，应优先调整字段映射或脚本以适配用户模板。
9. 仅当用户没有提供任何模板时，才询问用户是稍后提供正式模板，还是明确同意使用 skill 示例模板。未获得明确同意不得运行 `create_example_templates.py`。
10. 仓库不提交 DOCX/XLSX 二进制模板。先检查 Python 依赖；缺失时征得用户同意后，通过 `bash` 安装 `$SKILL_DIR/requirements.txt`。生成脚本必须先把选定的模板复制到 `result/`，然后只修改复制品，不得直接修改原模板：

```bash
# 仅在用户明确同意使用示例模板后运行：
python "$SKILL_DIR/scripts/create_example_templates.py"
python "$SKILL_DIR/scripts/generate_documents.py" \
  --input requirements.json \
  --srs-template "$SKILL_DIR/assets/srs-template.docx" \
  --sd-template "$SKILL_DIR/assets/sd-template.docx" \
  --stc-template "$SKILL_DIR/assets/stc-template.xlsx" \
  --output-dir result
```

省略 `--output-dir` 时默认输出到当前工作目录的 `result/`。不得把输出目录设置为 `assets/`。

11. 打开 `result/` 中的生成结果做最终检查：确认用户模板原件未发生变化；自动填入内容遵循用户模板已有格式要求。只有用户模板或用户明确认可的规范要求标红、隐藏空字段、固定页签时，才执行对应检查，不能用示例模板规则覆盖用户模板。
12. 向用户列出生成文件、仍为“当前不清楚”的问题、继承项引用以及建议补图/表的位置。

## 文档规则

- 用户提供模板时，以模板中的页眉、字体、颜色、章节、空字段处理方式和 XLSX 页签为准。
- 下列约定只适用于用户明确选择 skill 示例模板的情况：SRS/SD 默认页眉、DOCX 替换内容标红、空字段隐藏，以及 STC 的 `统计` 和 `缺陷记录&测试报告` 页签。
- 测试用例从驱动边界输入、LCNE 边界、芯片边界和 API 定义推导，正常与异常场景都要覆盖。
- 不把“当前不清楚”伪装为已确定内容；信息不足以生成可执行用例时先继续追问。

## 资源

- `references/brainstorming.md`：逐步提问策略、SRS/SD/STC 检查点。
- `references/template-fields.md`：DOCX 字段和 XLSX 列定义。
- `references/docx-template-example.md`：可直接复制到 Word 的 SRS/SD docxtpl 变量、段落循环、条件块和修订表格示例。
- `references/input-schema.json`：生成脚本输入示例及数据结构。
- `requirements.txt`：文档生成脚本的 Python 依赖。
- `scripts/create_example_templates.py`：创建可迁移字段的示例 DOCX/XLSX 模板。
- `scripts/generate_documents.py`：渲染 SRS、SD 并填充 STC。
- `assets/`：仅在用户明确同意时生成的示例模板目录（DOCX/XLSX 被 `.gitignore` 忽略）；它不能替代用户提供的正式模板。

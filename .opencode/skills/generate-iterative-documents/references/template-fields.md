# 字段语义与映射契约

Python 脚本只按 JSON 路径向模板变量赋值，不判断内容语义。Agent 在提问、汇总和写入 JSON 时必须遵守本文件；不得仅凭变量名猜测。

## 通用规则

1. 每个事实只写入最匹配的字段，不为“让文档看起来完整”而在多个字段重复。
2. 用户确认“无/不涉及”时写空字符串；“当前不清楚”原样写入；“继承需求”写明参考来源；自由输入内容经归纳并由用户确认后写入。选项字母不固定，且不要手工提供框架已经自动添加的自由输入选项。
3. `requirements[]` 中一个对象只对应一个 AR/功能需求。一个 AR 含多个独立功能时，先询问是否拆分。
4. 先完成逐 AR 字段，再由这些事实汇总 SRS/SD 简介字段。汇总不得引入新事实。
5. 生成前按本文件逐项回读 JSON；含“当前不清楚”的字段必须向用户列出。

## 标题字段（脚本计算，不由 Agent填写）

| 模板变量 | 生成规则 | 示例 |
|---|---|---|
| `HEADER`（SRS） | `UnionSV110 {iteration_name}软件需求规格说明书` | `UnionSV110 B240迭代软件需求规格说明书` |
| `TITLE_CN`（SRS） | `UnionSV110 {iteration_name}需求软件规格说明书` | `UnionSV110 B240迭代需求软件规格说明书` |
| `TITLE_EN`（SRS） | `UnionSV110 {iteration_code} Iteration Software Requirement Specification` | `UnionSV110 B240 Iteration Software Requirement Specification` |
| `HEADER`（SD） | `UnionSV110 {iteration_name}需求软件设计说明书` | `UnionSV110 B240迭代需求软件设计说明书` |
| `TITLE_CN`（SD） | 与 SD 页眉正文相同 | 同上 |
| `TITLE_EN`（SD） | `UnionSV110 {iteration_code} Iterative Requirements Development Software Design Specification` | — |
| `ITERATION_REQUIREMENT` | `{iteration_code}需求` | `B240需求` |

标题字段来自顶层 `iteration_name` 和 `iteration_code`，由 `generate_documents.py` 计算。不要在 JSON 中另建同名字段。

## SRS 简介与汇总字段

| JSON 路径 → 模板变量 | 字段含义 | Agent 应询问/汇总什么 | 不应写什么 |
|---|---|---|---|
| `srs.purpose` → `PURPOSE` | 文档为什么存在、覆盖哪些需求 | 用所有 AR 标题概括“本文档主要描述……所涉及的接口设计、软件功能、产品环境、设计约束等” | 具体实现步骤、接口参数 |
| `srs.scope` → `SCOPE` | 本文档边界 | 分列新功能和继承需求，并明确不涉及的其他 UDK 需求 | 背景故事、测试步骤 |
| `srs.overview` → `OVERVIEW` | 各需求的高层背景概述 | 概括新功能/继承需求的业务或产品背景以及彼此关系 | 逐参数 API 定义 |
| `srs.software_functions` → `SOFTWARE_FUNCTIONS` | 软件提供的能力摘要 | 用动宾短语概括所有需求实现了什么能力 | 实现算法、调用链 |
| `srs.design_constraints` → `DESIGN_CONSTRAINTS` | 功能可用的条件和限制汇总 | 汇总芯片版本、debug/release、ko、初始化、权限等约束 | 性能指标、正常输出 |
| `srs.performance_summary` → `PERFORMANCE_SUMMARY` | 全部 AR 的性能要求汇总 | 汇总时延、吞吐、并发、资源、满规格、时序指标 | 一般功能正确性 |
| `srs.quality_summary` → `QUALITY_SUMMARY` | 全部 AR 的质量属性汇总 | 汇总可靠性、安全性、兼容性、恢复、资源泄漏、日志要求 | 测试命令 |
| `srs.testability_summary` → `TESTABILITY_SUMMARY` | 全部 AR 如何被验证 | 汇总测试入口、观测点、异常注入、mock/stub 和自动化限制 | 详细设计流程 |

## SRS 逐需求字段

模板循环为 `requirements`，数据源是 `requirements[]`。

| JSON 路径 → 模板变量 | 字段含义 | Agent 应询问/填写什么 | 边界 |
|---|---|---|---|
| `requirements[i].title` → `req.title` | 功能需求名称 | 用户确认的稳定需求标题 | 不使用测试用例标题代替 |
| `requirements[i].ar` → `req.ar` | 需求追踪编号 | 完整 AR 号 | 不自行编造 |
| `requirements[i].introduction` → `req.introduction` | 单项需求背景简介 | 为什么需要、现状问题、目标价值、受影响模块 | 不写实现流程 |
| `requirements[i].input` → `req.input` | 驱动边界处的输入/API 定义 | API 签名、参数、类型、方向、单位、合法范围、默认值，以及 LCNE/芯片边界输入 | 不写内部处理动作 |
| `requirements[i].processing` → `req.processing` | 对外接口被调用后的可观察处理 | 以需求语言描述前置校验、行为顺序、状态结果、同步/异步和失败契约，使测试人员可从外部判定 | 不写内部函数拆分、锁实现或资源管理细节 |
| `requirements[i].output` → `req.output` | 正常和异常时的对外结果 | 返回值、输出参数、事件、日志、状态、副作用和成功判据 | 不写测试操作 |
| `requirements[i].external_dependencies` → `req.external_dependencies` | 功能成立所依赖的外部条件 | ko、固件、芯片版本、服务、配置、其他接口、初始化顺序 | 不写本模块内部函数 |
| `requirements[i].performance` → `req.performance` | 当前 AR 的量化性能要求 | 时延、吞吐、并发、CPU/内存、满规格及时序 | 无量化要求时留空，不虚构数字 |
| `requirements[i].quality` → `req.quality` | 当前 AR 的质量属性 | 可靠性、安全性、兼容性、恢复、资源释放、日志 | 不写性能指标 |
| `requirements[i].testability` → `req.testability` | 当前 AR 的可测试设计 | dt 函数、观测点、异常注入、mock/stub、自动化限制 | 不等同于测试用例列表 |

## SD 简介字段

| JSON 路径 → 模板变量 | 字段含义 | 填写规则 |
|---|---|---|
| `sd.purpose` → `PURPOSE` | SD 的用途和读者 | 说明方案与详细设计用于指导开发和测试 |
| `sd.scope` → `SCOPE` | SD 覆盖与不覆盖的需求 | 与 SRS 范围保持需求集合一致，但从设计文档角度表述 |
| `sd.software_functions` → `SOFTWARE_FUNCTIONS` | 本次设计实现的软件能力摘要 | 从所有 `requirements[].detailed_design` 和功能标题概括，不加入未确认能力 |

## SD 逐需求字段

模板循环名是 `designs`，但脚本直接把同一个 `requirements[]` 传给它；`designs[i]` 与 `requirements[i]` 是同一项。

| JSON 路径 → 模板变量 | 字段含义 | Agent 应询问/填写什么 | 与 SRS 的区别 |
|---|---|---|---|
| `requirements[i].title` → `design.title` | 设计项标题 | 与 SRS 同一需求标题 | 必须保持一致 |
| `requirements[i].ar` → `design.ar` | AR 追踪编号 | 与 SRS 同一 AR | 必须保持一致 |
| `requirements[i].background` → `design.background` | 设计所需的背景 | 影响方案理解的现状、架构背景、继承关系 | 可比 SRS 介绍更技术化 |
| `requirements[i].detailed_design` → `design.detailed_design` | 功能实现方案 | 模块/函数职责、调用流程、关键分支、状态或资源生命周期、错误转换、并发处理，以及经开发者确认的伪代码或等价结构化流程 | 必须足以指导编码并可追溯到 SRS，但不臆造接口、状态或算法 |
| `requirements[i].constraints` → `design.constraints` | 接口使用和方案适用约束 | 芯片/版本、调用时机、前置状态、debug/release、并发与权限约束 | 说明“何时能用/不能用” |
| `requirements[i].external_interface_link` → `design.external_interface_link` | 正式接口定义的位置 | 用户确认的文档链接、章节、代码或 API 规范引用 | 没有来源则留空，不生成假链接 |

## 修订记录字段

同一个 `revisions[]` 同时用于 SRS 和 SD：

| JSON 路径 | SRS | SD | 含义 |
|---|---:|---:|---|
| `revisions[i].date` | 使用 | 使用 | 修订日期，建议 `YYYY-MM-DD` |
| `revisions[i].version` | 使用 | 使用 | 文档修订版本 |
| `revisions[i].ar` | 不显示 | 使用 | 本次修订关联 AR |
| `revisions[i].section` | 不显示 | 使用 | 修改章节 |
| `revisions[i].description` | 使用 | 使用 | 修改内容摘要 |
| `revisions[i].author` | 使用 | 使用 | 作者 |

## STC XLSX 字段

`requirements[i].test_cases[]` 只写入 `测试用例` 页签；不进入 DOCX。

| JSON 键 | XLSX 列 | 填写规则 |
|---|---|---|
| `id` | 测试用例编号 | 需求稳定缩写加三位序号，项目内唯一 |
| `type` | 用例类型 | 功能/异常/性能/安全/可靠性/兼容性/满规格/时序/资源回收/并发/边界校验之一 |
| `item` | 测试项 | 本条用例要验证的具体目标 |
| `title` | 测试用例标题 | 可读且能区分场景的验证性标题 |
| `priority` | 重要级别 | 仅 `H`、`M`、`L` |
| `precondition` | 预置条件 | “无条件”“mami已纳管设备”或用户确认的具体条件 |
| `input` | 输入 | 抽象输入类别和关键边界，不替代操作命令 |
| `steps` | 操作步骤 | 优先使用 `./udk_dt_tool <dt_func_name> <parameters...>`；信息不足时继续询问 |
| `expected` | 预期结果 | 可观察、可判定；功能用例写正常输出，异常用例写错误码/报错退出 |
| `execution` | 用例执行情况 | 新生成文档通常留空 |
| `remarks` | 备注 | 补充说明；为空时脚本回填所属 AR |

## 生成前字段审计

Agent 必须在调用脚本前完成以下检查：

1. `iteration_name`、`iteration_code` 已确认。
2. 每个 `requirements[i]` 的 `title` 和 `ar` 已确认且能一一对应。
3. `introduction/input/processing/output` 没有互相混写。
4. `processing` 是需求级行为；`detailed_design` 是设计级实现，两者粒度不同。
5. SRS/SD 汇总只来源于逐 AR 内容。
6. 所有性能数字、错误码、接口名、dt 函数和链接都有用户或已有材料依据。
7. 测试用例的 `priority`、`type`、命令和预期结果可判定。
8. 所有“当前不清楚”和继承引用已在最终确认中展示。
9. 每个 AR 已向开发者展示并确认 SRS 候选内容、SD 候选内容和伪代码；伪代码能覆盖主流程、主要失败路径以及必要的回滚/资源清理。
10. SRS 中的每条行为都有可观察结果或验收方式；SD 中的关键设计能追溯到 SRS，且不存在“按原逻辑”“正常处理”“失败返回错误”等未展开的实现空洞。

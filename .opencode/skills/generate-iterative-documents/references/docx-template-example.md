# 可复制到 DOCX 的 docxtpl 完整模板示例

本文件展示“用户总结字段 → JSON 路径 → Python context → DOCX 占位符”的最终写法。创建正式模板时，把下面的模板正文逐段复制到 Word，再设置字体、标题样式、自动编号、页眉和表格边框。

## 复制到 Word 前必须知道

1. `{{ VARIABLE }}` 是普通替换字段，可以和固定文字放在同一段。
2. `{%p ... %}` 是**段落控制标签**。它所在的段落只放这一条标签，不要放其他文字；渲染后控制段落会被删除。
3. `{%tr ... %}` 是**表格行控制标签**。它所在的表格行只放这一条标签；渲染后控制行会被删除。
4. 所有标签都保留花括号内侧空格，例如 `{{ TITLE_CN }}`、`{%p if req.input %}`。
5. 不要让 Word 把同一个标签拆成多个不同格式的 run。最稳妥的方式是一次性粘贴或输入完整标签，再统一设置其格式。
6. 需要自动填入的普通变量设置为红色；固定标题文字保持黑色。循环/条件控制标签本身不会出现在结果中，颜色不影响最终文档。
7. `A. 不涉及` 对应空字符串；下面的条件块会让相应标题和内容一起消失。
8. 标题编号建议由 Word 的多级列表控制，不要把 `3.n.x` 写死。下面用“功能需求”“背景”等文字标识应套用的标题级别。

---

# SRS 模板正文

## 页眉

在 Word 页眉中输入下面一整段，并设置为宋体、小五、居中、红色：

```text
{{ HEADER }}
```

`HEADER` 由脚本根据 `iteration_name` 计算。例如：

```text
UnionSV110 B240迭代软件需求规格说明书
```

## 封面标题

```text
{{ TITLE_CN }}
```

```text
{{ TITLE_EN }}
```

建议两段均居中、红色；字号和中英文字体按正式模板设置。

## 1 简介

### 1.1 目的

```text
{{ PURPOSE }}
```

对应 `srs.purpose`。由所有 AR 完成后反向汇总，例如：

```text
本文档主要描述B240迭代中，需求A、需求B、需求C所涉及的接口设计、软件功能、产品环境和设计约束等。
```

### 1.2 范围

```text
{{ SCOPE }}
```

对应 `srs.scope`，例如：

```text
描述UnionSV110中继承需求A、需求B，新功能需求C、需求D，不涉及其他UDK需求。
```

### 1.3 总体概述

```text
{{ OVERVIEW }}
```

对应 `srs.overview`。

### 1.4 软件功能

```text
{{ SOFTWARE_FUNCTIONS }}
```

对应 `srs.software_functions`。

### 1.5 设计约束

```text
{{ DESIGN_CONSTRAINTS }}
```

对应 `srs.design_constraints`。

## 2 功能需求

从下一行开始建立 AR 循环。`{%p for req in requirements %}` 和 `{%p endfor %}` 必须各自占一个独立段落。

```text
{%p for req in requirements %}
```

### 功能需求 {{ loop.index }}：{{ req.title }}

```text
AR号：{{ req.ar }}
```

下面每个可选字段都使用三段结构：

1. 单独一段 `{%p if ... %}`
2. 一段或多段实际内容
3. 单独一段 `{%p endif %}`

```text
{%p if req.introduction %}
```

#### 介绍

```text
{{ req.introduction }}
```

```text
{%p endif %}
```

```text
{%p if req.input %}
```

#### 输入

```text
{{ req.input }}
```

```text
{%p endif %}
```

```text
{%p if req.processing %}
```

#### 处理

```text
{{ req.processing }}
```

```text
{%p endif %}
```

```text
{%p if req.output %}
```

#### 输出

```text
{{ req.output }}
```

```text
{%p endif %}
```

```text
{%p if req.external_dependencies %}
```

#### 外部依赖

```text
{{ req.external_dependencies }}
```

```text
{%p endif %}
```

```text
{%p if req.performance %}
```

#### 性能需求

```text
{{ req.performance }}
```

```text
{%p endif %}
```

```text
{%p if req.quality %}
```

#### 质量需求

```text
{{ req.quality }}
```

```text
{%p endif %}
```

```text
{%p if req.testability %}
```

#### 可测试性

```text
{{ req.testability }}
```

```text
{%p endif %}
```

AR 循环结束：

```text
{%p endfor %}
```

> Word 操作建议：把“功能需求……”设置为需求章节标题级别；把“介绍/输入/处理/输出……”设置为其下一级标题。使用 Word 多级列表自动得到 `2.n`、`2.n.x`，不要依赖 `loop.index` 拼出所有章节号。

## 3 非功能需求汇总

如果希望没有汇总时连标题一起删除，使用：

```text
{%p if PERFORMANCE_SUMMARY %}
```

### 3.1 性能需求

```text
{{ PERFORMANCE_SUMMARY }}
```

```text
{%p endif %}
```

```text
{%p if QUALITY_SUMMARY %}
```

### 3.2 质量需求

```text
{{ QUALITY_SUMMARY }}
```

```text
{%p endif %}
```

```text
{%p if TESTABILITY_SUMMARY %}
```

### 3.3 可测试性

```text
{{ TESTABILITY_SUMMARY }}
```

```text
{%p endif %}
```

## 4 修订记录

在 Word 中创建四行四列的模板表格：

| 第1列 | 第2列 | 第3列 | 第4列 |
|---|---|---|---|
| 日期 | 修订版本 | 修改描述 | 作者 |
| `{%tr for rev in revisions %}` |  |  |  |
| `{{ rev.date }}` | `{{ rev.version }}` | `{{ rev.description }}` | `{{ rev.author }}` |
| `{%tr endfor %}` |  |  |  |

注意：

- 第二行和第四行是控制行，最终不会显示。
- 第三行是样板数据行，会按照 `revisions[]` 的元素数量复制。
- `{%tr for ... %}` 和 `{%tr endfor %}` 分别放在各自控制行的第一个单元格，其余单元格保持空白。

---

# SD 模板正文

## 页眉

在 Word 页眉中输入并设置为宋体、小五、居中、红色：

```text
{{ HEADER }}
```

## 封面标题

```text
{{ TITLE_CN }}
```

```text
{{ TITLE_EN }}
```

## 1 简介

### 1.1 目的

```text
{{ PURPOSE }}
```

对应 `sd.purpose`，例如：

```text
本文档描述了UnionSV110 B240的UDK软件方案和详细设计，用于指导软件开发人员、测试人员进行开发测试工作。
```

### 1.2 范围

```text
{{ SCOPE }}
```

对应 `sd.scope`。

### 1.3 软件功能

```text
{{ SOFTWARE_FUNCTIONS }}
```

对应 `sd.software_functions`。

## 3 需求详细设计

```text
迭代：{{ ITERATION_REQUIREMENT }}
```

开始逐 AR 设计循环：

```text
{%p for design in designs %}
```

### {{ design.title }}

```text
AR号：{{ design.ar }}
```

```text
{%p if design.background %}
```

#### 背景

```text
{{ design.background }}
```

```text
{%p endif %}
```

```text
{%p if design.detailed_design %}
```

#### 详细设计

```text
{{ design.detailed_design }}
```

```text
{%p endif %}
```

```text
{%p if design.constraints %}
```

#### 场景约束

```text
{{ design.constraints }}
```

```text
{%p endif %}
```

```text
{%p if design.external_interface_link %}
```

#### 对外接口描述

```text
{{ design.external_interface_link }}
```

```text
{%p endif %}
```

结束逐 AR 设计循环：

```text
{%p endfor %}
```

> Word 操作建议：把 `{{ design.title }}` 所在段落设置为 `3.n` 对应标题级别；把“背景/详细设计/场景约束/对外接口描述”设置为下一级标题，由 Word 多级列表产生 `3.n.x`。字段为空时，条件块中的内容会消失；如果要让标题也消失，标题必须放在 `{%p if ... %}` 与 `{%p endif %}` 之间。

## 4 修订记录

在 Word 中创建四行六列的模板表格：

| 第1列 | 第2列 | 第3列 | 第4列 | 第5列 | 第6列 |
|---|---|---|---|---|---|
| 日期 | 修订版本 | AR号 | 修改章节 | 修改描述 | 作者 |
| `{%tr for rev in revisions %}` |  |  |  |  |  |
| `{{ rev.date }}` | `{{ rev.version }}` | `{{ rev.ar }}` | `{{ rev.section }}` | `{{ rev.description }}` | `{{ rev.author }}` |
| `{%tr endfor %}` |  |  |  |  |  |

---

# JSON 与 DOCX 完整对应示例

下面 JSON 有两个 AR。SRS 会循环两次，SD 也会循环两次：

```json
{
  "iteration_name": "B240迭代",
  "iteration_code": "B240",
  "srs": {
    "purpose": "本文档主要描述B240迭代中，端口状态查询、端口状态订阅所涉及的接口设计、软件功能、产品环境和设计约束等。",
    "scope": "描述UnionSV110中新功能需求端口状态查询、端口状态订阅，不涉及其他UDK需求。",
    "overview": "本迭代新增端口状态主动查询和状态变化订阅能力。",
    "software_functions": "提供端口状态查询与状态变化通知能力。",
    "design_constraints": "仅支持目标芯片版本；使用前需要插入port驱动ko并完成mami纳管。",
    "performance_summary": "单次状态查询时延不超过用户确认的指标；订阅回调满足用户确认的时序要求。",
    "quality_summary": "失败路径不得泄漏资源，重复订阅应返回明确错误码。",
    "testability_summary": "通过dt_port_get_status和dt_port_subscribe进行自动化验证。"
  },
  "sd": {
    "purpose": "本文档描述了UnionSV110 B240的UDK软件方案和详细设计，用于指导软件开发人员、测试人员进行开发测试工作。",
    "scope": "描述UnionSV110中新功能需求端口状态查询、端口状态订阅，不涉及其他UDK需求。",
    "software_functions": "实现端口状态查询、订阅注册、事件分发和资源回收。"
  },
  "requirements": [
    {
      "title": "端口状态查询",
      "ar": "AR000101",
      "introduction": "提供应用主动获取指定端口当前状态的能力。",
      "input": "port_get_status(uint32_t port_id, port_status_t *status)；port_id为已纳管端口编号，status为非空输出指针。",
      "processing": "校验端口和输出指针后调用芯片状态查询接口，并转换底层返回码。",
      "output": "成功返回0并填写status；参数非法或芯片调用失败时返回明确错误码。",
      "external_dependencies": "依赖port驱动ko、mami设备纳管及目标芯片查询能力。",
      "performance": "",
      "quality": "失败路径不得修改无效输出，也不得泄漏资源。",
      "testability": "通过dt_port_get_status注入端口号并检查返回值与状态。",
      "background": "现有版本仅能被动接收部分状态事件，缺少统一主动查询入口。",
      "detailed_design": "API层完成参数校验后调用adapter层；adapter根据芯片类型选择操作集，读取状态并转换为统一枚举。",
      "constraints": "仅允许查询已纳管端口；输出指针不能为空。",
      "external_interface_link": "《Port API接口定义》2.1节",
      "test_cases": []
    },
    {
      "title": "端口状态订阅",
      "ar": "AR000102",
      "introduction": "提供端口状态变化时通知上层应用的能力。",
      "input": "port_subscribe(uint32_t port_id, port_event_cb callback, void *private_data)。",
      "processing": "校验参数后注册回调；芯片事件到达后转换状态并通知订阅者。",
      "output": "注册成功返回0；重复注册、非法回调或底层失败时返回明确错误码。",
      "external_dependencies": "依赖port驱动ko、芯片中断和事件分发模块。",
      "performance": "事件通知时延满足用户确认的指标。",
      "quality": "并发取消订阅时不得访问已释放回调上下文。",
      "testability": "通过dt_port_subscribe注册回调并注入芯片事件。",
      "background": "上层应用需要及时感知链路状态变化。",
      "detailed_design": "订阅信息保存到受锁保护的订阅表；事件线程复制有效订阅项后在锁外执行回调。",
      "constraints": "回调不得执行阻塞操作；取消订阅后不再产生新回调。",
      "external_interface_link": "《Port API接口定义》2.2节",
      "test_cases": []
    }
  ],
  "revisions": [
    {
      "date": "2026-06-15",
      "version": "V1.0",
      "ar": "AR000101, AR000102",
      "section": "全文",
      "description": "初始版本",
      "author": "张三"
    }
  ]
}
```

## 循环展开关系

```text
requirements[0]
  ├─ SRS: req.title / req.ar / req.introduction / ...
  └─ SD : design.title / design.ar / design.background / ...

requirements[1]
  ├─ SRS: req.title / req.ar / req.introduction / ...
  └─ SD : design.title / design.ar / design.background / ...
```

Python 将同一个 `requirements[]`：

- 以 `requirements` 名称传给 SRS 模板；
- 以 `designs` 名称传给 SD 模板。

因此同一个 AR 的 SRS 与 SD 内容不会因为维护两份数组而错位。

## 最小字段对应速查

| 用户总结字段 | JSON 路径 | SRS/SD 模板写法 |
|---|---|---|
| 迭代名称 | `iteration_name` | 脚本计算 `HEADER`、`TITLE_CN` |
| 迭代英文标识 | `iteration_code` | 脚本计算 `TITLE_EN`、`ITERATION_REQUIREMENT` |
| SRS 目的 | `srs.purpose` | `{{ PURPOSE }}` |
| SRS 范围 | `srs.scope` | `{{ SCOPE }}` |
| SRS 总体概述 | `srs.overview` | `{{ OVERVIEW }}` |
| SRS 软件功能 | `srs.software_functions` | `{{ SOFTWARE_FUNCTIONS }}` |
| SRS 设计约束 | `srs.design_constraints` | `{{ DESIGN_CONSTRAINTS }}` |
| SRS 性能汇总 | `srs.performance_summary` | `{{ PERFORMANCE_SUMMARY }}` |
| SRS 质量汇总 | `srs.quality_summary` | `{{ QUALITY_SUMMARY }}` |
| SRS 可测试性汇总 | `srs.testability_summary` | `{{ TESTABILITY_SUMMARY }}` |
| 功能需求 | `requirements[i].title` | `{{ req.title }}` / `{{ design.title }}` |
| AR号 | `requirements[i].ar` | `{{ req.ar }}` / `{{ design.ar }}` |
| 介绍 | `requirements[i].introduction` | `{{ req.introduction }}` |
| 输入 | `requirements[i].input` | `{{ req.input }}` |
| 处理 | `requirements[i].processing` | `{{ req.processing }}` |
| 输出 | `requirements[i].output` | `{{ req.output }}` |
| 外部依赖 | `requirements[i].external_dependencies` | `{{ req.external_dependencies }}` |
| 单项性能 | `requirements[i].performance` | `{{ req.performance }}` |
| 单项质量 | `requirements[i].quality` | `{{ req.quality }}` |
| 单项可测试性 | `requirements[i].testability` | `{{ req.testability }}` |
| SD 目的 | `sd.purpose` | `{{ PURPOSE }}`（SD 模板） |
| SD 范围 | `sd.scope` | `{{ SCOPE }}`（SD 模板） |
| SD 软件功能 | `sd.software_functions` | `{{ SOFTWARE_FUNCTIONS }}`（SD 模板） |
| 相关背景 | `requirements[i].background` | `{{ design.background }}` |
| 功能实现流程 | `requirements[i].detailed_design` | `{{ design.detailed_design }}` |
| 接口使用约束 | `requirements[i].constraints` | `{{ design.constraints }}` |
| 对外接口链接 | `requirements[i].external_interface_link` | `{{ design.external_interface_link }}` |
| 修订日期 | `revisions[i].date` | `{{ rev.date }}` |
| 修订版本 | `revisions[i].version` | `{{ rev.version }}` |
| 修订 AR | `revisions[i].ar` | `{{ rev.ar }}` |
| 修改章节 | `revisions[i].section` | `{{ rev.section }}` |
| 修改描述 | `revisions[i].description` | `{{ rev.description }}` |
| 作者 | `revisions[i].author` | `{{ rev.author }}` |

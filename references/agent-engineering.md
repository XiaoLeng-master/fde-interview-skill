# Agent Engineering 专项题库

## 边界

这份资料用于 AI/Agent FDE 或 JD 明确要求 RAG、Tool Use、MCP、Agent Harness、Eval 时。不要对所有 FDE 候选人机械考察多 Agent 或向量数据库。

## 基础模型与 Agent

### Q1：Agent 与普通 LLM 调用有什么区别？

期待：模型在循环中根据状态选择工具和下一步，直到完成/停止；Harness 负责上下文、权限、错误、预算、Trace 和终止。说明更高延迟、成本和累积错误。

### Q2：什么时候不用 Agent？

流程确定、规则稳定、风险高且可验证路径清晰时用普通软件/Workflow；单次检索或抽取用简单调用。复杂度必须用 Eval 证明价值。

## RAG

### Q3：如何设计企业知识 RAG？

覆盖：数据源、Parser/Chunk、Metadata、Hybrid Retrieval、Rerank、权限过滤、引用、更新/删除、评测、无答案、审计。

### Q4：怎样评估 RAG？

分检索与生成：Recall/Precision/MRR、Context Relevance、Faithfulness、Answer Correctness、Citation、业务任务完成；建立真实 Query-Evidence 对和失败集。

### Q5：权限变更后索引怎样一致？

保留 Source ACL/版本，检索时强制过滤；增量事件、删除传播、重建/双索引；监控延迟。不能只依赖 Prompt 告诉模型不要泄露。

## Tool Use 与 MCP

### Q6：如何设计 Tool？

清晰使用/禁用条件、语义化参数、最小 Schema、读写 Effect 分级、输入校验、友好错误、幂等、版本和监控。工具少而正交优于 50 个相似工具。

### Q7：MCP 与 Function Calling 的区别？

Function Calling 是模型表达结构化工具调用的能力；MCP 是工具/资源发现与连接的标准协议。MCP 不替代底层业务 API、授权或安全审查。

### Q8：如何防 Prompt Injection 导致越权？

外部内容视为不可信数据；权限在软件层；工具 Allowlist、最小权限、审批、参数校验、输出脱敏、Sandbox、Audit、Adversarial Eval。模型拒绝不是唯一防线。

## Harness 与状态

### Q9：Harness 负责什么？

计划/控制流、Tool Router、Context、State、Budget、Error Recovery、Termination、Human-in-the-loop、Eval 与 Trace。同一模型因 Harness 不同表现可完全不同。

### Q10：Context 快满了怎么办？

Token Budget、滑动窗口、结构化关键事实、摘要、长 Tool 输出外存、按需检索、父子 Agent 隔离；评测摘要丢失和错误回忆。

### Q11：如何防死循环？

最大轮次/时间/成本、重复动作检测、状态进展判定、错误分类、策略切换、人工升级和当前最佳结果。区分探索与无进展。

## Eval 与 Observability

### Q12：如何建立 Agent Eval？

Unit/Workflow/End-to-end/Adversarial 分层；规则、人工和校准后的 LLM Judge；固定 Release；CI Gate；线上失败回流；质量、成本和延迟共同比较。

### Q13：需要记录什么 Trace？

输入、Prompt/模型版本、Tool 参数/结果、状态变化、审批、Effect、成本、延迟和错误。敏感数据分级/脱敏；支持安全 Replay。

## 多 Agent

### Q14：什么时候使用多 Agent？

当上下文隔离、并行、不同工具/权限或专业边界带来可测价值。只读调研可并行，强一致写操作尽量归一。与单 Agent 基线比较质量和成本。

### Q15：子 Agent 权限和预算怎样控制？

独立上下文、工具子集、Token/时间/层级预算、结构化返回、Trace、部分失败和取消。父 Agent 不应把全部权限自动继承。

## 生产答题必覆盖十项

```text
Tools · State · Permissions · Failure Recovery · Evals
Tracing · Cost · Release Gates · Rollback · Human Oversight
```

只讲 Prompt、Framework 或模型选择，不能构成完整生产方案。

## 难度适配

- 初级：解释核心机制，能写出最小调用链，知道主要失败和安全边界。
- 中级：比较方案、设计 Tool/State/Eval，并能结合真实项目说明取舍。
- 高级：覆盖 Multi-tenant、变更管理、SLO、事故、成本、组织采用和平台复用。
- 架构/Lead：要求定义多个客户之间的公共能力、发布治理、团队边界和停止条件。

## 单题 10 分评分

- 概念与机制 3：不是背名词，能说明控制流和责任边界。
- Trade-off 2：知道何时不用、成本与替代方案。
- 工程落地 2：接口、状态、错误、版本和运行细节。
- 安全与评测 2：权限、Eval、Trace、人工和发布 Gate。
- 真实证据 1：能连接本人项目或清楚承认没有实战。

## 追问链

### RAG

`Chunk/Index → Retrieval → Rerank → Permission → Generation → Citation → Update/Delete → Eval`。候选人在哪层含糊，就要求给一个具体失败 Case 和验证方法。

### Tool/MCP

`Schema → Selection → Auth → Validation → Effect → Error → Idempotency → Version → Monitoring`。追问 Prompt Injection 怎样跨越内容与工具边界。

### Harness

`Loop → State → Context → Budget → Termination → Recovery → Human → Trace`。追问模型供应商变化时如何保证回归。

### Eval

`Task → Dataset → Expected behavior → Grader → Release binding → Online signal → Failure replay`。追问 LLM Judge 如何校准、怎样防评测集过拟合。

### Multi-agent

`Why multiple → Topology → Context isolation → Permission → Write conflict → Budget → Partial failure → Baseline comparison`。如果不能证明优于单 Agent，建议退回更简单方案。

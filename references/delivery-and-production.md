# 交付、生产化与运营题库

## 选择最小充分机制

对每个关键判断分别比较：确定性代码、规则/优化、传统 ML、检索、单次模型调用、受限 Agent、人工复核。选择满足需求的最简单机制；模型和 Agent 不是默认答案。

## Production Checklist

### 工具与集成

- Tool 描述、Schema、输入校验和版本兼容。
- 读、建议、暂存、提交等 Effect 分层。
- API 限流、超时、重试、幂等和熔断。
- Source of Truth、写后 Readback 和冲突处理。

### 状态

- 会话、任务、业务对象和工作流状态分离。
- Checkpoint、恢复、去重和并发控制。
- 长任务的超时、取消、重入和补偿。
- 状态 Schema 与模型/Prompt 版本关联。

### 身份与权限

- 用户身份向 Tool 传递，不使用共享超级账号。
- Least Privilege、Tenant Isolation、字段/行级权限。
- 高风险动作审批，Agent 推荐不等于授权。
- 密钥管理、数据保留、脱敏和审计。

### 评测

- Unit：单工具、解析、规则和权限。
- Workflow：多步任务、状态变化和失败恢复。
- End-to-end：真实用户 Case 和接受事件。
- Adversarial：Prompt Injection、越权、数据泄露、重复写入。
- 回归：线上失败 Case 进入固定评测集。

### 可观测性

- Trace：模型、Prompt、Tool、状态、审批和 Effect。
- Metrics：完成率、质量、延迟、成本、失败、人工接管。
- Logs：调试、运营、审计分层，敏感信息脱敏。
- Replay：能重放关键路径但不重复真实副作用。

### 发布与恢复

- Release 绑定代码、模型、Prompt、Tool、配置和数据版本。
- 离线 Gate → Shadow → 限定用户 → 灰度 → 扩展。
- 明确 Rollback、Kill Switch、Fallback 和人工流程。
- Runbook、On-call、SLO、升级路径和事故复盘。

### 成本

- 模型 Token、向量/存储、外部工具、人工复核、运维和事故。
- 设置单任务和全局 Budget；超限降级或停止。
- 质量相同时优先更简单、成本更低、延迟更稳的方案。

## 系统设计答题顺序

1. 复述用户、工作流、规模、风险和接受事件。
2. 明确非目标和待确认假设。
3. 给出最小 Vertical Slice。
4. 画数据、控制和 Effect 边界。
5. 解释机制选择与 Trade-off。
6. 覆盖权限、状态、失败、Eval、Observability、Cost。
7. 给出试点、发布、回滚、运营和采用。
8. 说明怎样沉淀复用能力。

## 面试题与评分点

### Q1：Agent 调错工具怎么办？

高分：减少/路由工具、Schema 和描述、参数校验、权限分级、Dry-run/Stage、审批、错误反馈、Eval 与 Trace。只说“优化 Prompt”得分低。

### Q2：怎样防止重复退款/重复发消息？

幂等键、业务唯一约束、事务/Outbox、Effect Receipt、写后 Readback、重试只针对安全操作，且 Agent 不直接绕过授权。

### Q3：模型输出不稳定，如何发布？

建立固定 Case 和 Gate，绑定版本，Shadow/Canary，Guardrail、人工复核、分层指标、快速回滚。不要依赖人工随机体验。

### Q4：如何做多租户企业 Agent？

身份传播、Tenant Context、数据/索引隔离、权限过滤、密钥隔离、审计、资源配额、配置版本、跨租户测试和故障域。

### Q5：外部 API 经常超时，Agent 应怎么恢复？

错误分类、超时、有限重试和退避、Circuit Breaker、Fallback、Checkpoint、对用户透明、避免重复 Effect；超过预算转人工或结束。

### Q6：如何评估生产 Agent？

任务接受率、工具/状态正确性、权限违规、人工接管、延迟、成本、用户修正和业务 Guardrail；离线与线上结合，线上失败回流。

### Q7：事故中首先做什么？

保护用户和 Effect：停止/降级/回滚，确认影响和时间线，保存证据，再定位根因。先改 Prompt 可能破坏证据或扩大影响。

### Q8：什么时候使用多 Agent？

只有上下文、工具、权限、并行或组织边界确有差异时。写操作通常归一；只读探索可并行。比较单 Agent 基线和成本收益。

## 高级追问

- 如何把 Evaluation 结果绑定到精确 Release？
- 模型供应商版本变化怎样做 Change Management？
- 人工复核积压后怎样保证系统安全降级？
- 如何让 Replay 不产生真实副作用？
- 如何处理数据删除、权限变更和向量索引一致性？
- 哪些规则必须在确定性软件中，不能交给模型？

## 反面信号

- 架构只有 LLM、Vector DB 和框架。
- 用 Prompt 代替权限与事务。
- 只说重试，不讨论幂等。
- 只看平均准确率，不测危险长尾。
- 只说监控 Token，不监控业务 Effect。
- 发布没有 Owner、Runbook 和 Rollback。


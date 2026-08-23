# fde-interview

一个通用的 Forward Deployed Engineer 求职与面试 Skill，面向 FDE、Forward Deployed AI Engineer、FDSE、Applied AI、AI 解决方案工程师、客户工程和技术交付等相邻岗位。

它关注的不是“会不会背 Agent 名词”，而是候选人能否证明：找到真实客户问题、亲手交付生产系统、推动采用和结果，并把现场经验沉淀为可复用能力。

## 功能

- 准备度诊断：按候选人背景、JD、地区、级别和期限识别差距。
- 自适应路线：选择 14 天、28 天、6–8 周或自定义计划。
- 简历优化：区分事实、推断和证据缺口，生成国内/国际版本。
- 模拟面试：一次只问一个问题，覆盖项目、Discovery、系统设计、生产和价值。
- Case Drill：用分阶段隐藏证据模拟模糊客户现场。
- 双轨评分：通用 100 分＋国内企业交付／国际平台 Overlay。

## 适用背景

- Software、Infrastructure、Data、ML、AI/Agent Engineer；
- Solutions Engineer、Implementation、Technical Consultant；
- 需要从相邻岗位转型 FDE 的候选人；
- 已在做 FDE 式工作，但希望优化简历和面试表达的人。

## 安装

将整个 `fde-interview` 目录安装到支持 Skills 机制的 AI Agent 或开发工具中。不同平台的 Skill 路径和加载方式可能不同，请以对应平台的说明为准。不要只复制 `SKILL.md`，否则题库、参考资料和验证器会丢失。

## 使用示例

```text
我做了 5 年 Java 后端，想一个月内转国内 AI FDE，帮我诊断。
```

```text
根据这份 JD 和脱敏简历，给我生成国内版和国际版 FDE 简历。
```

```text
模拟面试我：目标是 Senior Forward Deployed AI Engineer，全英文。
```

```text
给我一个制造企业设备维修 Agent 的 FDE Case，不要提前给答案。
```

## 目录

```text
fde-interview/
├── SKILL.md
├── references/       # 角色、评分、简历、题库、Case 和来源
├── evals/evals.json  # 五个行为测试场景
└── scripts/validate_skill.py
```

## 验证

```bash
python3 scripts/validate_skill.py .
python3 -m json.tool evals/evals.json >/dev/null
```

验证器检查：Frontmatter、必要文件、相对链接、Eval Schema、核心行为约束，以及 `SKILL.md` 是否保持在 500 行以内。

## 设计边界

- 不承诺 Offer、薪酬或短期转岗结果。
- 不虚构客户、Ownership、指标或生产状态。
- 不把 AI Agent 当成所有 FDE 岗位的唯一技术方向。
- 不把开源方法冒充任何公司的官方面试标准。
- 岗位、公司流程、产品版本和薪酬等时效信息需要重新核验。

## 贡献

欢迎提交：

- 有来源的 FDE 面试题与实际 Case；
- 国内行业场景和海外平台场景；
- 新的验证用例；
- 过期资料和失效链接修正。

提交真实项目案例前请删除客户名称、个人信息、密钥、内部 URL 和受保密协议约束的内容。

## License

MIT。引用的第三方资料保留各自版权和许可证；本仓库不重新分发受限制的原文材料。

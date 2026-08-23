# GitHub 发布建议

## Repository metadata

- 推荐仓库名：`fde-interview-skill`
- 备选仓库名：`codex-fde-interview`
- Description：`A generic Codex skill for FDE readiness diagnosis, evidence-based resume optimization, mock interviews, and staged customer case drills.`
- Visibility：建议先 Public；如果还要加入真实简历测试样本，先保持 Private 并确认已彻底脱敏。
- License：MIT

## Topics

```text
fde
forward-deployed-engineer
ai-engineering
agent-engineering
interview-preparation
resume
codex-skill
customer-engineering
solutions-engineering
llmops
```

## Initial commit

```text
feat: publish generic FDE interview skill
```

Commit body：

```text
Add evidence-based FDE readiness, resume, mock interview, and case-drill workflows.
Include domestic enterprise-delivery and international platform tracks, staged case banks,
source provenance, evaluation fixtures, and a dependency-free validator.
```

## 发布范围

只发布 `fde-interview/` 目录内的文件。不要发布：

- `fde-28-day-plan.md`，这是个人计划；
- `work/` 下的仓库审计、设计稿和内联测试记录；
- 原始或脱敏简历；
- 下载用于研究的第三方仓库；
- 任何 API Key、Cookie、Token、内部 URL 或客户材料。

## 发布前检查

```bash
python3 scripts/validate_skill.py .
python3 -m json.tool evals/evals.json >/dev/null
rg -n 'BEGIN .*PRIVATE KEY|api[_-]?key|access[_-]?token|password' .
```

第三条命令应只出现文档中用于提醒用户的通用安全词，不应出现真实值、个人路径或用户名。

## 发布动作边界

在用户确认仓库名、可见性和 GitHub 目标账号后，再创建远端仓库、提交和推送。不要将验证通过自动解释为推送授权。

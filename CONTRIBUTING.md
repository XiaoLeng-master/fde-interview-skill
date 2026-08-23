# Contributing to fde-interview

Thank you for improving this Skill. Contributions should make FDE preparation more useful without overstating a candidate's experience or exposing private information.

## Who can contribute

Useful perspectives include technical, delivery, consulting, product, business, customer-facing, and domain backgrounds. Beginner contributions are welcome when they are grounded in a clear source, a reproducible check, or a well-described evidence gap.

## What to contribute

- **Cases:** Add realistic but fully fictionalized FDE, customer-engineering, delivery, or interview scenarios. State the context, constraints, decision points, and intended learning outcome. Do not represent a composite or fictional scenario as a real customer engagement.
- **Sources:** Add stable, public sources to `references/source-map.md` with a short note explaining what claim they support. Prefer primary sources. Summarize rather than copying restricted material, and retain attribution and license information.
- **Manual evaluation fixtures:** Add or improve JSON cases under `evals/`. Fixtures define prompts and observable assertions; they are not an automated benchmark or a claim of model quality. Keep IDs unique, assertions testable, and coverage balanced across technical and nontechnical candidates.
- **Documentation:** Correct outdated facts, broken links, unclear instructions, or accessibility gaps.

## Privacy and evidence rules

Never submit a real candidate's personal data, customer or employer names, credentials, internal URLs, source code, interview recordings, confidential documents, or information covered by an NDA. Remove identifying details before sharing an example.

Do not invent ownership, metrics, production status, customer outcomes, or hiring-process claims. Mark uncertain material as an evidence gap, an example, or a hypothesis. A useful contribution is allowed to say that more evidence is needed.

## Validate changes

From the package directory, run:

```bash
python3 scripts/validate_skill.py .
python3 -m json.tool evals/trigger-cases.json >/dev/null
python3 -m json.tool evals/quality-cases.json >/dev/null
python3 -m json.tool evals/adversarial-cases.json >/dev/null
```

The validator checks package structure, links, required contracts, and fixture shape. It cannot determine whether a generated response meets a fixture's assertions; evaluate those manually and record the model version, date, result, and notes outside the fixture files.

## Pull requests

Keep each pull request small and focused. In the description, explain:

1. The user or evidence problem being addressed.
2. Which files changed and why.
3. Any source provenance, fictionalization, or privacy treatment.
4. The validation commands run and their results.

Do not include unrelated formatting changes. Maintainers may request clarification, additional provenance, further de-identification, or a manual evaluation result before merging.

## License

Contributions are accepted under this repository's [MIT License](LICENSE). Third-party material remains subject to its own copyright and license terms.

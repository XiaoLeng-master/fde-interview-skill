# Manual evaluation fixtures

These fixtures are platform-neutral, manual checks for `fde-interview`. They do not prescribe a runner, model, prompt wrapper, scoring API, or hidden chain of thought.

- `trigger-cases.json` checks whether a request is routed to the right mode, or receives one necessary clarification.
- `quality-cases.json` checks the quality and safety of a completed response across the four supported modes.
- `adversarial-cases.json` checks that unsafe, fabricated, private, or instruction-injecting requests are handled without changing the skill's evidence standard.

For each case, record the observed response, pass/fail result, evaluator notes, model version, and evaluation date outside these fixtures. A case passes only when every listed assertion is satisfied. Do not add private candidate data, customer names, credentials, internal URLs, or interview recordings to the fixtures.

The validator checks fixture shape and coverage only. Human evaluators determine whether a response actually satisfies an assertion.

# International Platform FDE Case Bank

## Interview behavior

Present only the Initial Brief in English. Reveal hidden evidence only when the candidate asks a relevant question. Keep feedback until the end. The candidate may clarify in English; if they request bilingual practice, keep interview prompts in English and provide post-round feedback in Chinese.

## Case 1: Multi-tenant enterprise support agent

### Initial Brief

> A global SaaS company wants an AI support agent that can answer product questions, inspect customer accounts, issue limited credits, and escalate complex cases. Design a six-week pilot for three enterprise customers.

### Hidden evidence

- Users: support agents first; fully autonomous customer-facing use is not approved.
- Volume: 30,000 tickets/day globally; pilot customers contribute 600/day.
- Data: product docs, CRM, account telemetry, prior tickets; ACLs differ by tenant and region.
- Effects: credits under $50 can be proposed; execution requires policy check and approval.
- Baseline: median handle time 18 minutes; re-open rate 14%; CSAT varies by segment.
- Risk: cross-tenant leakage is a launch blocker; EU data cannot leave region.
- Owner: VP Support owns outcome; Security and Finance own release gates; Platform receives operations.

### Expected scope

Agent-assist with cited answers, account diagnostics, staged credit proposals, and structured escalation. Use tenant-bound identity, regional data paths, offline/online evals, read/write separation, effect receipts, canary rollout, and human oversight.

### Scoring points

- Establish accepted outcomes beyond answer accuracy.
- Handle tenant isolation, regional constraints, audit, idempotency, and approval.
- Define eval corpus, shadow mode, release binding, telemetry, rollback, and SLO.
- Explain how repeated integrations become reusable platform tools.

### Follow-ups

- How would you prove that the pilot reduced cost without lowering customer outcomes?
- What happens when CRM and telemetry disagree?
- Which controls must remain deterministic?

## Case 2: Data-platform deployment for a regulated customer

### Initial Brief

> A bank has purchased a data and AI platform but has not moved a critical fraud-investigation workflow into production. You are the FDE responsible for delivering a measurable outcome in eight weeks.

### Hidden evidence

- Sponsor believes the bottleneck is model accuracy; investigators say entity resolution and data freshness are worse.
- Seven source systems use inconsistent customer identifiers and event times.
- Investigators currently assemble cases in spreadsheets and email.
- Baseline: 4.5 hours per high-priority case; 22% require rework after supervisor review.
- Policy: investigators may recommend; final account action remains with an authorized officer.
- Operations: customer platform team can own pipelines, but no one owns the investigation app.
- Scale: 2 million events/day; 350 high-priority cases/day.

### Expected scope

Observe representative cases, charter an accepted investigation packet, repair identity/time semantics for the bounded population, build one workflow surface, preserve authorization, and establish a receiving owner before production.

### Scoring points

- Reframe away from premature model optimization.
- Address data readiness, ontology/entity identity, lineage, and freshness.
- Define application workflow, human decision boundary, evaluation, operations, and value.
- Avoid forcing all seven systems into a platform-wide transformation before proving one slice.

### Follow-ups

- What would make you stop the engagement?
- How do you separate forecast value from realized production value?
- What do you upstream into the platform after the first deployment?

## Case 3: Brownfield API integration and customer escalation

### Initial Brief

> A strategic customer cannot create a resource through your public API. Reads work, writes fail with a vague validation error. They need a response today and a reliable integration path this week. Walk me through your approach.

### Hidden evidence

- The request body sends the string `"null"` where the API expects a list.
- Documentation shows an incomplete write example and does not explain update semantics.
- The customer's token has correct scope; the issue reproduces in a test tenant.
- A second validation error appears after fixing the first due to an outdated enum value.
- No production data may be copied into local debugging.
- Product engineering owns the API; the FDE may propose documentation and error-message fixes.

### Expected response

Reproduce safely, minimize and classify the failures, verify authentication separately, produce a working example, explain create/update semantics, write a clear customer email, and file precise product/docs tickets with evidence and impact.

### Scoring points

- Hypothesis-driven debugging and safe reproduction.
- Clear separation of customer configuration, docs gap, and product defect.
- Empathetic, actionable customer communication without blame.
- Reusable fix: improved examples, validation messages, test coverage, or SDK behavior.

### Follow-ups

- What would you include in the customer email versus the internal ticket?
- How do you prevent credentials or customer data from entering logs?
- When do you escalate to product engineering?

## Seniority adjustment

- Junior: guide with one clarification at a time; focus on correct decomposition and safe implementation.
- Mid-level: expect independent discovery, integration, rollout and metrics.
- Senior: add commercial commitments, conflicting stakeholders, multi-region scale, operating model and product roadmap trade-offs.
- Principal/Lead: require portfolio prioritization, staffing, reusable platform strategy and kill decisions across multiple engagements.

## End-of-case output

Require the candidate to summarize: customer outcome, evidence, scope/non-goals, architecture boundary, production controls, adoption/operations, and reusable product capability.


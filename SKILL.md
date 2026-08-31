---
name: digital-anthropology-observation
description: Conduct a bounded, privacy-preserving study of how humans, agents, tools, roles, skills, workbenches, and artifacts interact in context. Use when asked to observe actual work, reconstruct a work episode, identify friction or emergent expertise, compare intended and actual workflow, or propose a capability improvement. Do not use for personnel scoring, covert surveillance, unrestricted telemetry, or unilateral production changes.
---

# Digital anthropology observation

## Mission

Study the work episode, not the person. Produce an evidence-backed account of how purpose, context, roles, skills, tools, agents, judgment, handoffs, and verification combined to produce an artifact and a capability residue.

## Required sequence

1. Confirm an approved study manifest. If there is no manifest, stop and request one.
2. State the question, bounded goal, setting, systems, observation mode, identity scope, privacy class, retention, and stop rules.
3. Use the minimum necessary evidence. Prefer synthetic IDs, coarse time, artifact classes, source references, and redacted summaries.
4. Reconstruct the episode before interpreting it.
5. Separate evidence into:
   - `OBS-LIVE`: direct live observation;
   - `OBS-REPLAY`: authorized replay;
   - `SYS-RECORD`: system event or history;
   - `ART-STATE`: artifact or version state;
   - `PART-REPORT`: participant account;
   - `ANALYST-INFER`: analyst interpretation.
6. Mark context quality, ambiguity, retries, corrections, handoffs, delays, burden, product status, and privacy handling as episode conditions, never as person scores.
7. Compare the intended workflow with the actual trajectory.
8. Include participant meaning, disagreement, uncertainty, and at least one negative case or explicit non-finding when possible.
9. Write a finding with evidence, interpretation, warrant, uncertainty, proposed hypothesis, receiving owner, and re-observation plan.
10. Route the proposal to the proper owner. Do not implement or deploy it from this skill.

## Observation seams

Prefer boundary events over keystroke-level capture:

- intent and specification;
- context package assembly and recovery;
- role or skill selection;
- plan and design sign-off;
- human-agent or agent-agent handoff;
- correction, retry, refusal, or override;
- review and evaluator result;
- artifact checkpoint and delivery status;
- merge, publication, abandonment, or maintenance;
- capability harvest and later transfer.

## Interpretive discipline

Do not infer motive, personality, intelligence, emotion, trust, attention, effort, or competence from activity. Do not treat a retry as incompetence, a delay as idleness, acceptance as correctness, a polished artifact as easy work, a model contribution as authorship, or one episode as a general rule.

If the evidence only establishes sequence, say so. If meaning comes from a participant account, label it as such. If causality is uncertain, write a hypothesis rather than a conclusion.

## Hard stops

Refuse or stop when asked to:

- observe covertly or collect broad telemetry without a bounded question;
- merge identities or cross a workspace/principal boundary without approval;
- copy credentials, tokens, cookies, private prompts, private messages, protected personal data, or unnecessary third-party identifiers;
- create a person-level score or ranking;
- silently modify prompts, skills, workflows, permissions, routing, standards, retention, or production defaults;
- publish raw or identifiable material without the required review.

Escalate privacy, security, safety, consent, or authority concerns to the named study owner and the relevant Counsel/Parliamentarian authority. The observer may pause the study but does not gain production authority.

## Output template

```text
Study / episode:
Question and bounded goal:
Observation mode and boundary:
Evidence sources and privacy class:
Intended workflow:
Actual trajectory:
Context present, missing, degraded, or recovered:
Decisions, handoffs, retries, corrections, and verification:
Participant account and disagreement:
Finding:
Warrant:
Uncertainty / negative case:
Improvement hypothesis:
Receiving owner and approval gate:
Re-observation plan:
Retention and disposition:
```

# Research notes

This note records the external research and GitHub exemplars used to shape the Center. The goal was not to copy an existing product, but to identify design patterns that can be translated into the Navy Yard’s principles: evidence and warrants travel; boundaries constrain; capability is grown; and projects leave institutional capability behind.

## 1. Digital anthropology and organizational ethnography

The useful disciplinary move is to treat digital work as both an **archive** and a **process**. Abdelnour’s work on ethnography in modern organizational settings distinguishes ex-post digital records from real-time interaction and recommends following work across digital sites, learning platforms’ affordances, using longitudinal records for triangulation, preserving multivocality, and remaining reflexive about the observer’s influence. It also emphasizes the ethical problem of access to individual digital traces and the need for informed consent.

- [Confronting the Digital: Doing Ethnography in Modern Organizational Settings (UCL repository PDF)](https://discovery.ucl.ac.uk/10079077/8/Abdelnour_Confronting%20the%20digital.%20Doing%20ethnography%20in%20modern%20organizational%20settings_AOP.pdf)
- [UCL Digital Anthropology MSc](https://www.ucl.ac.uk/prospective-students/graduate/taught-degrees/digital-anthropology-msc)

**Design translation:** the Center must be multi-sited across Hermes, work trackers, Notion, GitHub, workbenches, agent sessions, and artifact history. It should use archive, process, and participant account together; learn the hidden affordances of each platform; make observer influence visible; and protect identity and consent.

## 2. Superpowers: explicit method and skill behavior

[Superpowers](https://github.com/obra/superpowers) is a strong exemplar of composable agent skills organized into a complete software-development method. Its workflow moves through intent clarification, specification, design sign-off, planning, implementation, review, testing, and branch completion. Its subagent-driven workflow emphasizes fresh context, task-sized implementation, review after each task, and a final review.

Useful source documents:

- [Superpowers repository](https://github.com/obra/superpowers)
- [Writing plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md)
- [Subagent-driven development](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md)
- [Requesting code review](https://github.com/obra/superpowers/blob/main/skills/requesting-code-review/SKILL.md)
- [Writing skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md)
- [Release notes and cross-harness skill testing](https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md)

**Design translation:** Superpowers should be a field site and a method laboratory. Observe its seams—specification, sign-off, plan, fresh-context handoff, review, test, merge, and capability harvest. Borrow its practice of pressure-testing skill behavior, but do not put an observer into every implementer prompt or treat plan compliance as quality.

## 3. Kata: work-state and orchestration layer

[Kata Skills](https://github.com/gannonh/kata-skills) provides a specification-driven workflow with issue capture, milestones, phases, codebase mapping, debugging, execution, and audit. [Kata Symphony](https://github.com/gannonh/kata-symphony) adds orchestration across projects, parallel agent sessions, ticket lifecycle, automated review, human review, merge, progress, and milestone completion. [Kata](https://kata.sh/) frames the system around design, plan, build, verify, traceability, context, and human direction.

**Design translation:** Superpowers structures the method inside a task; Kata structures work state across tasks. The Center should compare intended and actual phase transitions, context continuity, blocked/ready paths, scope change, review, verification, and closure. It should link findings to Kata or the adopted work tracker rather than create a parallel ticketing system.

## 4. Gas Town and Beads: durable identity and work lineage

[Gas Town](https://github.com/gastownhall/gastown) and [Beads](https://github.com/gastownhall/beads) explore multi-agent workspaces with persistent work units, identities, mailboxes, handoffs, worktrees, dependency graphs, merge queues, workflow templates, and health/watchdog functions.

**Design translation:** persistent identity, session-to-work linkage, handoff provenance, and durable work lineage are valuable for reconstructing agent work across ephemeral sessions. The Navy Yard should not import an assumption that always-on monitoring, automatic continuation, or activity rules are inherently good. Persistence should support evidence lineage, not surveillance.

## 5. AgentsView: local-first session evidence

[AgentsView](https://www.agentsview.io/) and its [GitHub repository](https://github.com/kenn-io/agentsview) provide a local-first viewer for sessions across coding agents and projects. The design includes adapters, searchable timelines, links from activity back to source, live synchronization, and analysis across sessions and tools.

**Design translation:** borrow the local-first, source-linked, multi-agent viewer pattern. Change the default data posture: a Navy Yard study should expose only approved sessions and redacted evidence, not every conversation, thinking block, tool call, or person’s activity.

## 6. RoboRev: review and rework as a verification signal

[RoboRev](https://github.com/kenn-io/roborev) uses background, read-only review agents, isolated worktrees for fixes, post-commit hooks, and a persistent review ledger.

**Design translation:** a review ledger is useful for tracing findings, rework, resolution, and recurrence. It is one evaluator/verification stream. The Center must join it with artifact states and participant accounts before making a claim about context, friction, or meaning.

## 7. OpenTelemetry, Phoenix, and Langfuse: trace infrastructure without interpretive overreach

[OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md) offer a vendor-neutral vocabulary for agent and model operations. [Phoenix](https://github.com/Arize-ai/phoenix) and its [LLM tracing documentation](https://arize.com/docs/phoenix/tracing/llm-traces) show how OpenTelemetry traces can support timelines, evaluation, datasets, and experiments. [Langfuse observability](https://langfuse.com/docs/observability/overview) shows a related approach for tracing prompts, tool calls, retrieval, latency, annotations, and experiments; its evaluation material stresses human calibration and the limits of noisy judge scores.

**Design translation:** use OTel/OTLP as an event transport and add Navy Yard identifiers for study, episode, work, role, skill, workbench, context package, handoff, artifact checkpoint, claim, warrant, privacy class, and outcome. Treat Phoenix/OpenInference or Langfuse as optional analysis/evaluation infrastructure. Traces and scores are evidence inputs, not ethnographic interpretation.

## 8. Human-AI interaction as an observation lens

[Microsoft’s Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/project/guidelines-for-human-ai-interaction/) and the [HAX Toolkit](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/) provide a practical lens organized around initial interaction, regular interaction, moments when the system is wrong, and interaction over time.

**Design translation:** use the guidelines as questions during observation: how does a participant form a mental model, notice uncertainty, recover from error, learn the system’s boundaries, and decide whether to trust or override it? Do not reduce the Center to a checklist or turn HAI guidance into a person score.

## 9. NIST AI RMF: lifecycle governance and post-deployment learning

[NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) and the [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/manage/) emphasize lifecycle roles, privacy, documentation, testing/evaluation/validation/verification, post-deployment monitoring, user and stakeholder feedback, appeals and overrides, incidents and near misses, drift, and deployment conditions.

**Design translation:** NIST reinforces the Center’s place inside the lifecycle and its need to preserve context and feedback. It does not make the Digital Anthropologist the owner of technical evaluation, legal policy, or compliance. ATS, Counsel, Parliamentarian, and the relevant owner retain those authorities.

## 10. Agent Skills: packaging the role as a maintainable capability

The [Agent Skills specification](https://agentskills.io/specification) defines portable, version-controlled skill directories with a concise `SKILL.md` and optional scripts, references, and assets. Its [best practices](https://agentskills.io/skill-creation/best-practices) emphasize progressive disclosure, clear routing descriptions, deterministic code where useful, and testing. Anthropic’s [Agent Skills engineering note](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) provides an additional implementation perspective.

**Design translation:** package Digital Anthropology as a role charter plus a small executable observation skill. Keep protocols, codebooks, privacy rules, schemas, and tests in referenced files. Use pressure scenarios to test whether the skill refuses person-scoring, raw sensitive capture, motive inference, and automatic intervention.

Emerging research such as [GitSkills](https://arxiv.org/abs/2608.10906) treats the growing population of agent skills as an empirical object and highlights routing and skill-quality questions. This is a timely reason for the Center to study how skills are actually selected, interpreted, modified, and maintained—not merely whether the final artifact passed.

## 11. Synthesis

The sources converge on a stack with distinct layers:

| Layer | Borrowed pattern | Navy Yard adaptation |
|---|---|---|
| Method | Superpowers’ staged workflow and skill tests | observe seams and pressure-test changes |
| Work state | Kata’s phases, issues, milestones, and verification | compare planned and actual work without duplicating the tracker |
| Persistence | Gas Town/Beads identity and handoff lineage | preserve provenance, not activity surveillance |
| Evidence UX | AgentsView’s local-first, source-linked viewer | approved sessions, redaction, and scoped visibility |
| Verification | RoboRev’s review ledger; Phoenix/Langfuse experiments | feed ATS; retain qualitative meaning separately |
| Transport | OpenTelemetry agent spans | add study/episode/context/privacy/warrant fields |
| Field method | archive + process + participant account; reflexivity | triangulate, seek negative cases, record observer influence |
| Learning | Agent Skills progressive disclosure and tests | role package, references, scripts, and realistic evals |
| Governance | NIST lifecycle monitoring and privacy | explicit authority, consent, retention, appeal, and re-observation |

The result is a Center that can see how the Navy Yard works without becoming the thing that makes work unsafe to do.

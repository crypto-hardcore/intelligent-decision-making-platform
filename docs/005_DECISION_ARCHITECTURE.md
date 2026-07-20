# Decision Architecture

**Resolution:** 005  
**Status:** Adopted  
**Version:** 0.0.0  
**Release:** Constitutional Foundation  
**Adopted:** 20 July 2026  

---

## Purpose

This document defines how the Intelligent Decision-Making Platform transforms
Observations into governed actions and validated Knowledge.

It establishes the stages, artifacts, responsibilities, authority, states,
traceability, and failure behavior of the platform's decision process.

## Foundational Principle

A decision is not a prediction.

A decision is a governed commitment made under uncertainty using the best
available Evidence.

The platform must preserve:

- supporting Evidence;
- contradictory Evidence;
- assumptions;
- uncertainty;
- alternatives;
- reservations;
- risk constraints;
- approval authority;
- execution facts;
- actual outcomes.

The objective is not to pretend uncertainty has disappeared.

The objective is to reason through uncertainty consistently and responsibly.

## Canonical Decision Flow

```text
Reality
  ↓
Observations
  ↓
Evidence
  ↓
Domain Assessments
  ↓
Decision Brief
  ↓
Execution Plan
  ↓
Governance Decision
  ↓
Execution
  ↓
Execution Report
  ↓
Review Report
  ↓
Validated Knowledge
```

Every stage has a distinct responsibility.

No stage may silently assume the authority of another.

## Part I — Observations

An Observation is a factual representation of something detected, measured,
received, or recorded.

Examples include:

- a market price;
- traded volume;
- funding rate;
- economic announcement;
- strategy result;
- journal entry;
- execution fill;
- operational error.

An Observation must not contain a recommendation.

An Observation should preserve, where applicable:

- source;
- timestamp;
- subject;
- measured or reported value;
- unit;
- collection method;
- data quality;
- provenance;
- relevant context.

Observation systems collect and normalize information.

They do not decide what the information means.

## Part II — Evidence

Evidence is one or more Observations selected and organized because they are
relevant to a question, hypothesis, Assessment, or decision.

Observations are facts.

Evidence is facts placed into decision context.

Evidence may be classified as:

- supporting;
- contradictory;
- neutral;
- missing;
- unreliable.

Contradictory Evidence must not be discarded because it weakens a preferred
conclusion.

Evidence quality may consider:

- source reliability;
- completeness;
- recency;
- consistency;
- relevance;
- independence;
- susceptibility to noise or manipulation.

Evidence quality and conclusion confidence are related but distinct.

## Part III — Domain Assessments

An Assessment answers:

> What does the available Evidence mean within this domain?

Initial Assessment types include:

- Market Assessment;
- Historical Assessment;
- Strategy Assessment;
- Risk Assessment;
- Trader Assessment.

Every Assessment should contain:

- identity;
- type;
- subject and scope;
- time horizon;
- summary;
- supporting Evidence;
- contradictory Evidence;
- assumptions;
- uncertainty;
- confidence;
- reservations;
- validity period;
- producing module;
- creation timestamp.

Assessments are allowed to disagree.

Disagreement is information.

Decision Intelligence must preserve material disagreement rather than
manufacturing artificial consensus.

## Part IV — Decision Intelligence

Decision Intelligence synthesizes relevant Assessments into a Decision Brief.

It answers:

> Should action be considered?

It considers:

- alignment and conflict among Assessments;
- Evidence quality;
- compatible or incompatible time horizons;
- uncertainty;
- missing information;
- asymmetric risk;
- alternatives;
- invalidation conditions.

Decision Intelligence does not:

- collect raw external data as its primary responsibility;
- calculate final execution mechanics;
- authorize execution;
- place orders;
- rewrite governance policy.

It must not reduce all reasoning to one score when doing so would conceal
important disagreement or uncertainty.

## Part V — Decision Brief

A Decision Brief is the official decision-support artifact.

It may recommend:

- proceed to planning;
- do not proceed;
- defer pending additional Evidence;
- continue observing;
- compare defined alternatives.

The absence of action is a valid outcome.

A Decision Brief should contain:

### Identity

- unique identifier;
- subject;
- decision question;
- creation timestamp;
- validity period;
- time horizon.

### Executive Summary

A concise statement of the recommendation and rationale.

### Context

The environment in which the decision is being considered.

### Supporting Evidence

The strongest Evidence favoring the recommendation.

### Contradictory Evidence

The strongest Evidence opposing or weakening the recommendation.

### Assessment Synthesis

How relevant domain Assessments interact.

### Alternatives

Reasonable alternatives, including no action.

### Assumptions

Conditions treated as true but not fully established.

### Uncertainty

Known limitations, missing information, and unresolved conflicts.

### Reservations

Reasons for caution that do not necessarily invalidate the recommendation.

### Recommendation

The proposed action, rejection, deferral, comparison, or observation.

### Confidence

The strength of support for the recommendation.

### Strengthening Conditions

Future Observations that would strengthen the recommendation.

### Invalidation Conditions

Future Observations that would materially weaken or invalidate it.

A Decision Brief explains why action should be considered.

It must not silently become an Execution Plan.

## Part VI — Execution Planning

The Execution Planner answers:

> If this decision is approved, how should it be carried out?

Planning may consider:

- strategic intent;
- timeframe;
- available capital or resources;
- liquidity;
- costs;
- slippage;
- operational constraints;
- risk limits;
- monitoring;
- fallback procedures.

The Planner may determine that a recommendation cannot be executed safely or
practically.

It must return a planning failure or request reconsideration rather than
manufacture a misleading plan.

## Part VII — Execution Plan

An Execution Plan is a structured proposal for implementing a Decision Brief.

It is not permission to execute.

For trading, a plan may contain:

- instrument;
- direction;
- position size;
- maximum exposure;
- entry conditions;
- order type;
- proposed price or range;
- stop-loss logic;
- take-profit logic;
- maximum holding period;
- cancellation conditions;
- invalidation conditions;
- monitoring requirements;
- emergency exit conditions;
- estimated costs;
- venue;
- dependencies;
- operational checks.

Other domains may define different fields while preserving the same
architectural role.

## Part VIII — Governance

The Governance Engine answers:

> May this plan be executed under current authority and policy?

Governance is independent of enthusiasm, confidence, and expected
profitability.

A high-confidence opportunity may still be rejected.

Governance may consider:

- Decision Brief;
- Execution Plan;
- risk policy;
- allowed markets and instruments;
- automation level;
- current exposure;
- loss limits;
- strategy permissions;
- schedule;
- system health;
- data quality;
- operational readiness;
- human approval;
- emergency restrictions.

Possible outcomes are:

- approved;
- rejected;
- deferred;
- conditionally approved;
- additional review required.

Every outcome must include a reason.

The Governance Engine has final software authority over execution.

No Strategy, Intelligence Module, Decision Brief, or Planner may override a
governance rejection.

### Authority Modes

#### Human-Governed Operation

A human approves or rejects eligible plans.

#### Hybrid Operation

Policies perform automated checks while designated plans require human
approval.

#### Policy-Governed Operation

The Governance Engine approves plans automatically within explicitly
delegated boundaries.

The architecture remains unchanged as authority evolves.

## Part IX — Execution

The Execution Engine answers:

> What actions were actually carried out?

It does not:

- invent a strategy;
- reinterpret the Decision Brief;
- expand risk limits;
- ignore governance conditions;
- conceal failure.

Before and during execution, it must verify:

- approval remains valid;
- the plan has not expired;
- preconditions still hold;
- systems remain healthy;
- actions remain within approved limits;
- emergency controls remain available.

Material changes require cancellation, safe degradation, or renewed planning
and governance.

An approved Execution Plan should be treated as immutable.

Material changes require a new version and renewed approval.

## Part X — Execution Report

An Execution Report records:

- execution identity;
- linked Decision Brief;
- linked Execution Plan;
- linked Governance Decision;
- timestamps;
- requested actions;
- actual actions;
- orders and fills;
- costs and slippage;
- warnings;
- errors;
- cancellations;
- deviations;
- completion status.

It records facts.

It does not rewrite original reasoning after the outcome is known.

## Part XI — Review

Review compares:

- what was observed;
- what was believed;
- what was recommended;
- what was planned;
- what was approved;
- what was executed;
- what occurred.

Review distinguishes:

### Decision Quality

Was the decision reasonable given the Evidence available at the time?

### Planning Quality

Was the plan appropriate and practical?

### Governance Quality

Were the correct policies applied?

### Execution Quality

Was the approved plan executed accurately and safely?

### Outcome Quality

What result occurred?

### Process Adherence

Did each subsystem remain within its responsibility?

A good decision may produce a bad outcome.

A bad decision may produce a good outcome.

Outcome must not be confused with decision quality.

## Part XII — Review Report

A Review Report should contain:

- linked artifact identifiers;
- expected outcome;
- actual outcome;
- decision-quality assessment;
- planning-quality assessment;
- governance-quality assessment;
- execution-quality assessment;
- errors and deviations;
- unexpected Observations;
- candidate lessons;
- follow-up actions;
- review confidence;
- unresolved questions.

Rejected, deferred, cancelled, and failed processes may also be reviewed.

## Part XIII — Knowledge Formation

An outcome does not create Knowledge automatically.

The Knowledge lifecycle is:

```text
Candidate Lesson
  ↓
Review
  ↓
Validation
  ↓
Knowledge Entry
  ↓
Future Reassessment
```

Knowledge may later be:

- reinforced;
- revised;
- narrowed;
- deprecated;
- invalidated.

The Knowledge Repository must preserve provenance and revision history.

The platform must guard against:

- learning from a single lucky outcome;
- overfitting to recent events;
- confusing correlation with causation;
- hindsight bias;
- survivorship bias;
- rewriting prior reasoning;
- treating repeated data as independent Evidence.

## Part XIV — Confidence and Uncertainty

Confidence expresses how strongly available Evidence supports an Assessment
or Decision Brief.

Confidence is not:

- probability of profit;
- certainty;
- authorization;
- a substitute for risk control.

Uncertainty records what remains unknown, unreliable, conflicting, or
unstable.

High uncertainty may cause:

- reduced confidence;
- reduced position size;
- stricter governance;
- deferral;
- no action.

The platform must not hide uncertainty to produce a decisive output.

## Part XV — Time and Validity

Every time-sensitive Assessment, Decision Brief, Execution Plan, and
Governance Decision should define validity.

An artifact may become invalid because:

- time passed;
- conditions changed;
- assumptions failed;
- contradictory Evidence appeared;
- data quality deteriorated;
- policy changed;
- operational conditions changed.

Expired artifacts must not authorize new execution.

## Part XVI — Traceability

The platform must reconstruct:

- which Observations supported Evidence;
- which Evidence supported each Assessment;
- which Assessments informed a Decision Brief;
- which Decision Brief produced an Execution Plan;
- which policies produced a Governance Decision;
- which plan produced an Execution Report;
- which reports supported a Knowledge Entry.

Traceability requires stable identifiers, timestamps, versioning, and
provenance.

## Part XVII — Artifact Versioning

Material changes require a new version.

Examples include:

- significant new Evidence;
- changed Assessment conclusion;
- altered Recommendation;
- changed position size;
- changed entry or exit conditions;
- changed approval conditions.

Earlier versions must remain available.

Decision history must not be overwritten.

## Part XVIII — Failure and Safe Degradation

Incomplete information and system failure are normal operating conditions.

Examples include:

- unavailable or stale data;
- conflicting data;
- Connector failure;
- model failure;
- Planner failure;
- Governance failure;
- Execution failure;
- repository failure.

When required information or authority is unavailable, the default response
must favor safety.

The platform may:

- continue observing;
- lower confidence;
- defer;
- reject execution;
- cancel an active plan;
- enter a safe state;
- request human review.

Failure must not be converted into false confidence.

## Part XIX — Decision States

A decision process may move through explicit states:

```text
Observed
  ↓
Under Research
  ↓
Assessed
  ↓
Brief Produced
  ↓
Planning
  ↓
Awaiting Governance
  ↓
Approved / Rejected / Deferred
  ↓
Executing
  ↓
Completed / Cancelled / Failed
  ↓
Under Review
  ↓
Reviewed
  ↓
Knowledge Considered
```

Not every process reaches execution.

Rejection, deferral, expiration, and continued observation are legitimate
states.

## Decision Architecture Laws

### Law 1 — Evidence Must Precede Recommendation

No recommendation may exist without traceable supporting Evidence.

### Law 2 — Contradiction Must Be Preserved

Material contradictory Evidence must be recorded.

### Law 3 — Responsibility and Authority Are Separate

The proposer must not be the sole approval authority.

### Law 4 — No Plan Is Permission

An Execution Plan does not authorize execution.

### Law 5 — Governance Has Final Software Authority

Execution requires a valid Governance Decision.

### Law 6 — Approved Plans Do Not Drift Silently

Material change requires a new plan version and renewed approval.

### Law 7 — No Action Is a Valid Outcome

The platform is not required to manufacture an opportunity.

### Law 8 — Outcome Does Not Define Decision Quality

Review must use information available when the decision was made.

### Law 9 — Every Important Decision Leaves an Artifact

The process must preserve enough information for reconstruction.

### Law 10 — Learning Requires Validation

Experience does not become Knowledge automatically.

## Closing Declaration

The platform does not move directly from data to action.

It moves from Observation to Evidence, Evidence to Assessment, Assessment to
decision, decision to planning, planning to Governance, Governance to
Execution, and Execution to learning.

This separation ensures that intelligence can recommend without commanding,
planning can prepare without authorizing, Governance can protect without
distorting analysis, and Execution can act without inventing intent.

## Related Documents

- [Platform Constitution](002_PLATFORM_CONSTITUTION.md)
- [Platform Architecture](003_PLATFORM_ARCHITECTURE.md)
- [Platform Glossary](004_PLATFORM_GLOSSARY.md)
- [Development Roadmap](006_DEVELOPMENT_ROADMAP.md)

## Revision History

| Version | Date | Change |
|---|---|---|
| 0.0.0 | 20 July 2026 | Resolution 005 adopted |

# Platform Glossary

**Resolution:** 004  
**Status:** Adopted  
**Version:** 0.0.0  
**Release:** Constitutional Foundation  
**Adopted:** 20 July 2026  

---

## Purpose

This document defines the official vocabulary of the Intelligent
Decision-Making Platform.

Important terms must have one stable architectural meaning. New architectural
terms should be defined here before they become part of production code or
normative documentation.

## Usage Rule

No important platform concept may exist without an official definition.

An implementation name may be more specific than a glossary term, but it must
not silently redefine the term.

## Definitions

### Assessment

A professional evaluation produced by an Intelligence Module within its
assigned domain.

An Assessment explains what relevant Evidence means in that domain. It records
its conclusion, supporting and contradictory Evidence, assumptions,
uncertainty, confidence, reservations, scope, and validity.

An Assessment does not authorize execution.

### Assumption

A condition treated as true for the purpose of analysis or planning but not
fully established by Evidence.

Assumptions must be explicit when they materially affect a conclusion.

### Capital Preservation

The principle that survival, resilience, and controlled exposure take
priority over aggressive opportunity capture.

In the trading application, capital preservation is the highest operational
priority.

### Confidence

An expression of how strongly available Evidence supports an Assessment or
Decision Brief.

Confidence is not certainty, probability of profit, or permission to execute.

### Connector

An adapter that integrates an external system with the platform.

A Connector translates protocols and data formats but does not own strategic
decisions.

### Decision Brief

The platform's official decision-support artifact.

It explains why an action should, should not, or might be considered. It
includes Evidence, Assessment synthesis, alternatives, assumptions,
uncertainty, reservations, recommendation, confidence, and invalidation
conditions.

A Decision Brief is not an Execution Plan and does not authorize action.

### Decision Intelligence

The responsibility that synthesizes relevant Assessments into a Decision
Brief.

It answers:

> Should action be considered?

### Evidence

One or more Observations selected and organized because they are relevant to
a specific question, hypothesis, Assessment, or decision.

Evidence may be supporting, contradictory, neutral, missing, or unreliable.

### Execution

The performance of actions defined by an approved Execution Plan.

### Execution Engine

The subsystem that performs an approved Execution Plan and records what
actually occurred.

It may not invent strategic intent or exceed approved authority.

### Execution Plan

A structured proposal describing how an eligible Decision Brief could be
implemented.

An Execution Plan is not permission to execute.

### Execution Planner

The responsibility that translates an eligible Decision Brief into a
practical Execution Plan.

It answers:

> If this decision is approved, how should it be carried out?

### Execution Report

The factual record of requested actions, actual actions, timestamps, fills,
costs, warnings, errors, deviations, cancellations, and completion status.

### Explainability

The ability to reconstruct and meaningfully communicate the reasoning,
evidence, authority, and actions behind an important platform outcome.

### Governance

The evaluation of whether an Execution Plan is permitted under current
authority and policy.

### Governance Decision

The formal result of governance evaluation.

Possible outcomes include:

- approved;
- rejected;
- deferred;
- conditionally approved;
- additional review required.

### Governance Engine

The subsystem with final software authority to approve or reject execution
under current policy.

### Governance Policy

An explicit rule defining what the platform may, must, or must not do.

Policies may address risk, markets, instruments, schedules, automation,
operational health, human approval, and emergency restrictions.

### Intelligence Module

A specialized research responsibility assigned to one knowledge domain.

Initial Intelligence Modules include Market, Historical, Strategy, Risk, and
Trader Intelligence.

### Knowledge

Validated information retained for future use after review.

Knowledge is not created automatically by an outcome.

### Knowledge Entry

A versioned, traceable unit of validated Knowledge.

### Knowledge Repository

The platform's institutional memory.

It stores validated lessons together with provenance, scope, confidence,
revision history, and lifecycle status.

### Learning

The process through which reviewed experience produces candidate lessons,
validated Knowledge, revisions, or invalidations.

### Observation

A factual representation of something detected, measured, received, or
recorded.

An Observation should preserve source, timestamp, subject, value, unit,
collection method, provenance, and data-quality information where applicable.

An Observation does not contain a recommendation.

### Planning

The process of determining how an eligible recommendation could be carried
out safely and practically.

### Platform Artifact

A structured domain object that crosses responsibility boundaries and
preserves traceability.

Core Platform Artifacts include Observation, Evidence, Assessment, Decision
Brief, Execution Plan, Governance Decision, Execution Report, Review Report,
and Knowledge Entry.

### Provenance

Information describing where an artifact or claim came from, how it was
produced, and which prior artifacts support it.

### Recommendation

The action, rejection, deferral, comparison, or continued observation proposed
by a Decision Brief.

A Recommendation is not authorization.

### Research

The disciplined process through which Observations are organized as Evidence
and evaluated within a defined domain to produce an Assessment.

### Reservation

A reason for caution that does not necessarily invalidate an Assessment or
Recommendation.

### Review

The structured evaluation of the decision process and its outcome.

Review distinguishes decision quality, planning quality, governance quality,
execution quality, outcome quality, and process adherence.

### Review Report

The artifact produced by Review.

It records expected and actual outcomes, quality assessments, deviations,
candidate lessons, follow-up actions, and unresolved questions.

### Risk

The possibility and consequence of loss, harm, failure, invalidation, or
undesired exposure.

### Traceability

The ability to follow an artifact from its sources through its transformations
and downstream consequences.

### Uncertainty

Known or suspected limitations, missing information, instability, conflict,
or unreliability that affects an Assessment, Decision Brief, plan, or review.

### Validation

The process of determining whether an artifact, lesson, input, or conclusion
meets defined requirements and is suitable for its intended use.

### Validity Period

The time interval or condition set during which a time-sensitive artifact may
be treated as current.

## Naming Guidance

Code should use glossary terminology when representing platform concepts.

Examples:

- `Observation` is preferred to an undefined `DataPoint` when the object has
  the architectural meaning of an Observation.
- `DecisionBrief` must not be used as a name for an order request.
- `GovernanceDecision` must not be reduced to an unexplained Boolean.
- `KnowledgeEntry` should preserve provenance and lifecycle information.

## Related Documents

- [Constitutional Foundation](000_FOUNDATION.md)
- [Platform Architecture](003_PLATFORM_ARCHITECTURE.md)
- [Decision Architecture](005_DECISION_ARCHITECTURE.md)

## Revision History

| Version | Date | Change |
|---|---|---|
| 0.0.0 | 20 July 2026 | Resolution 004 adopted |

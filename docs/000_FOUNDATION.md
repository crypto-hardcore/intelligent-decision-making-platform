# Constitutional Foundation

**Status:** Adopted  
**Version:** 0.0.0  
**Release:** Constitutional Foundation  
**Adopted:** 20 July 2026  

---

## Purpose

The Constitutional Foundation is the governing specification of the
Intelligent Decision-Making Platform.

It establishes why the platform exists, the principles that govern it, the
architecture through which responsibilities are separated, the vocabulary
used throughout the project, the process by which decisions become governed
actions, and the roadmap through which the platform will evolve.

The Constitutional Foundation precedes production implementation. All future
code, documentation, policies, and architectural decisions are expected to
conform to it.

## Scope

This foundation applies to the entire platform, including:

- core domain artifacts;
- intelligence modules;
- planning and governance systems;
- execution systems;
- review and learning systems;
- knowledge repositories;
- external connectors;
- application and infrastructure layers.

It is technology-independent. No programming language, exchange, market,
vendor, model, or deployment environment defines the platform's identity.

## Constitutional Documents

The foundation consists of six adopted resolutions:

1. [Platform Vision](001_PLATFORM_VISION.md)  
   Defines why the platform exists and what long-term purpose it serves.

2. [Platform Constitution](002_PLATFORM_CONSTITUTION.md)  
   Defines the principles and constraints that govern the platform.

3. [Platform Architecture](003_PLATFORM_ARCHITECTURE.md)  
   Defines the platform's organizational structure, responsibilities, layers,
   artifacts, and architectural laws.

4. [Platform Glossary](004_PLATFORM_GLOSSARY.md)  
   Defines the official meaning of important platform concepts.

5. [Decision Architecture](005_DECISION_ARCHITECTURE.md)  
   Defines how observations become evidence, assessments, decisions, governed
   actions, reviews, and validated knowledge.

6. [Development Roadmap](006_DEVELOPMENT_ROADMAP.md)  
   Defines the capability-based sequence through which the platform will be
   implemented and extended.

## Reading Order

New contributors should read the documents in numerical order.

The order is intentional:

```text
Vision
  ↓
Constitution
  ↓
Architecture
  ↓
Glossary
  ↓
Decision Architecture
  ↓
Development Roadmap
```

The Vision establishes purpose.

The Constitution establishes authority.

The Architecture establishes structure.

The Glossary establishes language.

The Decision Architecture establishes process.

The Development Roadmap establishes evolution.

## Authority

These documents are the highest-level technical authority within the
repository.

When implementation and constitutional documentation conflict, the conflict
must be resolved explicitly. Production code must not silently redefine an
approved architectural concept.

A constitutional change requires:

1. identification of the affected resolution;
2. explanation of the reason for change;
3. impact analysis;
4. formal review;
5. an approved revision;
6. an auditable Git commit.

## Architecture-First Principle

> We design before we implement.  
> We define before we optimize.  
> We understand before we automate.

Architecture must not become an excuse for permanent delay. Its purpose is to
make implementation clearer, safer, and easier to test.

## Engineering Resolutions

### Engineering Resolution 001

> Never allow implementation to outrun architecture.

### Engineering Resolution 002

> Every phase must leave the platform in a working, testable, and
> understandable state.

### Engineering Resolution 003

> Every production class must represent an approved platform concept or a
> clearly justified implementation responsibility.

## Relationship to Version 0.1

Version 0.0.0 contains the platform's governing specifications and no required
production behavior.

Version 0.1 begins the Core Domain Foundation by implementing the platform's
official artifacts, beginning with `Observation`.

The implementation must express the Constitution rather than inventing a
different architecture through code.

## Revision History

| Version | Date | Change |
|---|---|---|
| 0.0.0 | 20 July 2026 | Constitutional Foundation adopted |

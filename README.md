# PĀṆINI-LAB

## Counterfactual Analysis of Pāṇinian Rule Dependencies

> **Ancient Rules. Modern Exploration. Measurable Insights.**

PĀṆINI-LAB is a research-oriented computational framework for studying the
operational behaviour of a selected subset of Pāṇinian grammatical rules.

The core idea is to treat a computational representation of the grammatical
rule system as an **experimental object**.

Instead of only executing rules, PĀṆINI-LAB aims to allow controlled
interventions such as:

- Removing rules
- Disabling rules
- Reordering rules
- Modifying rule conditions
- Comparing original and counterfactual derivations
- Measuring rule impact
- Discovering rule dependencies

The project is scoped progressively rather than attempting to implement the
entire Aṣṭādhyāyī at once.

---

# 1. Project Vision

Traditional computational approaches to Sanskrit and Pāṇinian grammar have
focused on modelling, parsing, generation, simulation, and NLP.

PĀṆINI-LAB takes an experimental perspective:

> **Instead of only asking "What derivation does the rule system produce?",
> we ask "What happens to the derivation when the rule system is changed?"**

This enables computational experiments over grammatical rule interactions.

---

# 2. Current Project Status

| Component | Status |
|---|---|
| Project architecture | ✅ Complete |
| Rule schema | ✅ Complete |
| Rule conditions | ✅ Complete |
| Rule operations | ✅ Complete |
| Rule scope metadata | ✅ Complete |
| Dependencies | ✅ Complete |
| Blocking metadata | ✅ Complete |
| Grammar state model | ✅ Complete |
| Derivation records | ✅ Complete |
| Rule registry | ✅ Complete |
| Rule execution | ✅ Complete |
| Counterfactual disabling | ✅ Complete |
| Original vs counterfactual comparison | ✅ Complete |
| Automated tests | ✅ Complete |
| Authentic Pāṇinian rule subset | ⬜ Next |
| Advanced grammatical semantics | ⬜ |
| Dependency graph | ⬜ |
| Rule impact metrics | ⬜ |
| FastAPI API | ⬜ |
| React dashboard | ⬜ |
| Experimental evaluation | ⬜ |
| Research paper | ⬜ |

---

# 3. Phase 1A — Strong Rule Schema

## Status: ✅ COMPLETE

Phase 1A established the computational foundation required to represent
grammatical rules as structured objects instead of simple string
replacements.

### 3.1 Structured Rule Representation

Each rule can contain:

```text
Rule ID
Sūtra reference
Name
Description
Phenomenon
Conditions
Operation
Scope
Priority
Dependencies
Blocking information
Exceptions
Tags
Enabled/disabled state
Source reference
Validation status
````

---

## 3.2 Rule Conditions

The schema currently supports:

### Pattern conditions

```text
Current form contains a specified pattern
```

### Feature conditions

```text
A grammatical feature must have a specified value
```

The schema also reserves explicit representations for:

```text
Context conditions
Custom conditions
```

These will receive formal evaluators as the grammatical engine becomes more
sophisticated.

---

# 4. Rule Operations

The rule schema currently supports:

```text
SUBSTITUTE
INSERT
DELETE
FEATURE_UPDATE
CUSTOM
```

For example:

```text
SUBSTITUTE

अइ → ए
```

or:

```text
FEATURE_UPDATE

category = verb
        ↓
tense = present
```

The operation model is extensible so additional Pāṇinian operations can be
introduced without redesigning the entire rule representation.

---

# 5. Rule Scope

Rules can currently store contextual metadata including:

```text
Adhikāra
Anuvṛtti
Domain
Notes
```

These fields establish the data model required for representing contextual
information associated with grammatical rules.

They should not be interpreted as a complete formal implementation of these
traditional concepts yet.

---

# 6. Rule Interaction Metadata

The schema supports:

```text
Dependencies
Blocking relationships
Exceptions
Priority
```

Example:

```text
R001
  │
  ├── dependency → R002
  │
  ├── blocks → R003
  │
  └── priority → 100
```

This metadata will later feed the rule dependency graph and counterfactual
analysis.

---

# 7. Grammar State

## Status: ✅ INITIAL VERSION COMPLETE

PĀṆINI-LAB no longer represents a derivation only as a string.

A `GrammarState` contains:

```text
Current form
Tokens
Morphemes
Grammatical features
Applied rules
Derivation history
Metadata
```

### State representation

```text
                 GRAMMAR STATE
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
      FORM          TOKENS       MORPHEMES
        │             │             │
        └─────────────┼─────────────┘
                      ↓
                  FEATURES
                      ↓
                 RULE HISTORY
```

The current implementation establishes the data structure. More detailed
linguistic state semantics will be developed in subsequent phases.

---

# 8. Derivation Engine

## Status: ✅ COMPLETE FOR CURRENT SCHEMA

The derivation engine:

1. Creates an initial grammar state.
2. Loads the registered rules.
3. Orders rules according to priority.
4. Evaluates rule conditions.
5. Applies eligible operations.
6. Creates a new grammatical state.
7. Records the transformation.
8. Tracks applied rules.
9. Tracks skipped/disabled rules.
10. Produces a structured derivation result.

A derivation therefore becomes traceable:

```text
INPUT
  ↓
STATE 0
  ↓ R001
STATE 1
  ↓ R007
STATE 2
  ↓ R012
STATE 3
  ↓
OUTPUT
```

---

# 9. Counterfactual Experimentation

## Status: 🟡 BASIC IMPLEMENTATION COMPLETE

The first counterfactual capability is implemented:

```text
Disable selected rule
        ↓
Re-run derivation
        ↓
Compare with original
```

Example:

```text
ORIGINAL

अइ
 ↓
R001
 ↓
ए


COUNTERFACTUAL

अइ
 ↓
R001 disabled
 ↓
अइ
```

The experiment engine currently records:

```text
Original output
Counterfactual output
Disabled rules
Whether output changed
Original derivation steps
Counterfactual derivation steps
Changed derivation steps
```

### Still to be implemented

```text
Rule removal
Rule reordering
Rule modification
Batch rule experiments
Multi-rule interventions
```

---

# 10. Current Rule Dataset

The current dataset contains prototype/test rules used to validate the
computational architecture.

These rules are explicitly marked with validation statuses such as:

```text
illustrative
synthetic
```

They are **not yet the project's final linguistically validated Pāṇinian
rule set**.

This distinction is intentional.

The next milestone is to construct a carefully selected and academically
validated subset of authentic Pāṇinian rules.

---

# 11. Testing

## Status: ✅ COMPLETE

Automated tests currently validate:

```text
✓ Rule schema
✓ Grammar state
✓ Rule loading
✓ Rule execution
✓ Feature conditions
✓ Rule disabling
✓ Rule reset
✓ Counterfactual comparison
✓ Invalid condition detection
✓ Invalid operation detection
✓ Self-dependency validation
```

Run:

```bash
cd backend
pytest -v
```

---

# 12. Technology Stack

| Component            | Technology     |
| -------------------- | -------------- |
| Programming Language | Python         |
| Data Validation      | Pydantic       |
| Rule Engine          | Custom Python  |
| Database             | SQLite         |
| Graph Analysis       | NetworkX       |
| Data Analysis        | Pandas + NumPy |
| Backend API          | FastAPI        |
| Frontend             | React + Vite   |
| Graph Visualization  | React Flow     |
| Charts               | Plotly         |
| Testing              | Pytest         |
| Version Control      | Git + GitHub   |
| Development          | VS Code        |
| Containerization     | Not used       |

---

# 13. Architecture

Current architecture:

```text
                    rules.json
                        │
                        ▼
                ┌───────────────┐
                │ Rule Registry │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Rule Schema   │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Rule Engine   │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Grammar State │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Derivation    │
                │ Trace         │
                └───────┬───────┘
                        │
                 ┌──────┴──────┐
                 ▼             ▼
             ORIGINAL    COUNTERFACTUAL
                 │             │
                 └──────┬──────┘
                        ▼
                    COMPARISON
```

---

# 14. Development Roadmap

## Phase 1A — Strong Rule Schema

**✅ COMPLETE**

Structured representation of rules, conditions, operations, scope,
dependencies, blocking metadata, and grammatical state.

---

## Phase 1B — Advanced Grammar State

**⬜ NEXT**

Improve the state representation with:

* Token-level provenance
* Morpheme relationships
* Transformation locations
* Phonological features
* Morphological features
* State identifiers
* Parent/child state relationships
* Formal transition metadata

---

## Phase 2 — Validated Pāṇinian Rule Set

**⬜**

Select and implement a limited set of authentic rules.

Initial target:

```text
10–15 validated rules
        ↓
validated derivations
        ↓
20–30 rules
        ↓
additional phenomena
```

Each rule should have:

```text
Source
Sūtra
Interpretation
Formal condition
Operation
Expected derivations
Validation examples
```

---

## Phase 3 — Rule Dependency Graph

**⬜**

Construct a graph representing:

```text
Rule → Rule dependencies
Rule → Rule interactions
Rule → downstream effects
```

Technology:

```text
NetworkX
```

---

## Phase 4 — Counterfactual Engine

**🟡 BASIC VERSION COMPLETE**

Extend experimentation to:

```text
Remove
Disable
Reorder
Modify
```

and support automated batch experiments.

---

## Phase 5 — Impact Analysis

**⬜**

Develop quantitative measures including:

### Rule Criticality

How strongly a rule affects successful derivations.

### Rule Influence

How many downstream states/rules are affected.

### Rule Dependency

Direct and indirect dependency relationships.

### Rule Redundancy

Whether removing a rule leaves selected derivations unchanged.

Metrics will be formally defined and evaluated rather than arbitrarily
assigned.

---

## Phase 6 — FastAPI

**⬜**

Expose the engine through APIs:

```text
GET  /rules
GET  /rules/{id}

POST /derive
POST /experiment

POST /rules/{id}/enable
POST /rules/{id}/disable

GET /dependencies
GET /analysis
```

---

## Phase 7 — Interactive Dashboard

**⬜**

Planned interface:

```text
Sanskrit Input
      ↓
Original Derivation
      ↓
Select Rule
      ↓
Remove / Reorder / Modify
      ↓
Counterfactual Derivation
      ↓
Comparison
      ↓
Dependency Graph
      ↓
Impact Metrics
```

---

## Phase 8 — Experimental Evaluation

**⬜**

Conduct reproducible experiments over the validated rule subset.

Evaluation will include:

* Baseline derivations
* Counterfactual experiments
* Rule ablations
* Dependency analysis
* Impact measurements
* Error analysis
* Qualitative analysis
* Comparison with relevant existing systems

---

## Phase 9 — Research Paper

**⬜**

The research paper will cover:

1. Introduction
2. Background
3. Related Work
4. Research Gap
5. Rule Representation
6. Derivation Architecture
7. Counterfactual Methodology
8. Dependency Analysis
9. Experimental Design
10. Results
11. Discussion
12. Limitations
13. Conclusion

---

# 15. Definition of Done

PĀṆINI-LAB will be considered a successful research prototype when a user
can:

```text
Enter/select a Sanskrit derivation
            ↓
View the original derivation
            ↓
Inspect every rule application
            ↓
Select a grammatical rule
            ↓
Remove / disable / reorder / modify it
            ↓
Re-run the derivation
            ↓
Compare original vs altered derivation
            ↓
Identify downstream effects
            ↓
Inspect rule dependencies
            ↓
Measure rule impact
            ↓
Visualize the results
```

---

# 16. Current Milestone

```text
╔══════════════════════════════════════╗
║       PĀṆINI-LAB DEVELOPMENT         ║
╠══════════════════════════════════════╣
║                                      ║
║ Phase 1A  Strong Rule Schema     ✅  ║
║                                      ║
║ Phase 1B  Advanced Grammar State ⬜  ║
║ Phase 2   Validated Rule Set     ⬜  ║
║ Phase 3   Dependency Graph       ⬜  ║
║ Phase 4   Counterfactual Engine  🟡  ║
║ Phase 5   Impact Analysis        ⬜  ║
║ Phase 6   FastAPI                ⬜  ║
║ Phase 7   React Dashboard        ⬜  ║
║ Phase 8   Evaluation             ⬜  ║
║ Phase 9   Research Paper         ⬜  ║
║                                      ║
╚══════════════════════════════════════╝
```

## Immediate next milestone

> **Phase 1B — Advanced Grammar State and derivational semantics.**

The next implementation should build on the completed Phase 1A schema rather
than replacing it.

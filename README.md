# PĀṆINI-LAB

## Counterfactual Analysis of Pāṇinian Rule Dependencies

> Ancient Rules. Modern Exploration. Measurable Insights.

PĀṆINI-LAB is a research-oriented computational framework for studying the operational behaviour of a selected subset of Pāṇinian grammatical rules.

The central idea is to treat the computational grammar itself as an **experimental object**. Instead of only executing grammatical rules, the system will allow controlled interventions such as removing, disabling, reordering, or modifying rules and then measuring how those interventions affect derivations.

---

## 1. Project Objective

The project aims to build an experimental platform that can:

- Represent selected Pāṇinian grammatical rules computationally.
- Execute rules to produce traceable derivations.
- Record every transformation in a derivation trace.
- Run counterfactual experiments on the rule set.
- Compare original and altered derivations.
- Discover rule dependencies and interactions.
- Quantify rule influence, criticality, and redundancy.
- Visualize rule relationships and experimental results.

The project is **not intended to implement the entire Aṣṭādhyāyī initially**. The first prototype will use a carefully selected subset of rules and phenomena that can be implemented and evaluated rigorously.

---

# 2. Current Status

## Phase 1 — Core Computational Prototype

**Status: IN PROGRESS**

### Completed

#### Project structure

```text
panini-lab/
├── README.md
├── .gitignore
└── backend/
    ├── requirements.txt
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── rule_engine.py
    │   │   ├── derivation.py
    │   │   ├── registry.py
    │   │   └── experiment.py
    │   └── data/
    │       └── rules.json
    └── tests/
        ├── __init__.py
        └── test_engine.py
```

#### Rule representation

A first version of the `Rule` model has been implemented with fields for:

- Rule ID
- Sūtra reference
- Rule name
- Description
- Grammatical phenomenon
- Priority
- Input pattern
- Replacement operation
- Dependencies
- Enabled/disabled state

#### Rule registry

Implemented functionality to:

- Load rules from JSON.
- Retrieve individual rules.
- Retrieve all rules.
- Enable rules.
- Disable rules.
- Reset the rule set.

#### Rule engine

A basic executable rule engine has been implemented.

Current behaviour:

```text
input pattern → replacement
```

#### Derivation engine

The derivation engine currently:

- Loads registered rules.
- Orders rules using priority.
- Applies enabled rules.
- Records each step.
- Tracks applied rules.
- Tracks skipped/disabled rules.
- Produces the final output.
- Returns a structured derivation result.

#### Derivation trace

Each derivation step records:

```text
Step number
Rule ID
Sūtra
Before state
After state
Whether a change occurred
Explanation
```

#### Rule intervention

Rules can currently be disabled before a derivation.

This provides the first implementation of the counterfactual idea:

```text
ORIGINAL
Input → Rule → Output

COUNTERFACTUAL
Input → Rule disabled → Altered output
```

#### Counterfactual experiment abstraction

An initial `CounterfactualExperiment` class has been created to:

1. Run the original rule set.
2. Disable selected rules.
3. Run the altered rule set.
4. Return both derivations.
5. Reset the rule registry.

#### Testing

Initial automated tests cover:

- Normal rule application.
- Rule removal/disablement.

Expected initial test result:

```text
2 passed
```

---

# 3. Current Example

The current prototype contains an **illustrative computational rule representation** for a guṇa transformation.

Example:

```text
Input:
अइ

Rule:
R001
Sūtra reference: 6.1.87

Transformation:
अइ → ए
```

Counterfactual experiment:

```text
Original:
अइ → ए

R001 disabled:
अइ → अइ
```

This is currently a **prototype demonstration of the experimental mechanism**, not a claim that the present implementation completely captures the grammatical scope and conditions of the cited sūtra.

---

# 4. What Is NOT Done Yet

The current implementation is only the foundation.

## Phase 1A — Strong Pāṇinian Rule Schema

**Status: NOT STARTED**

The current `input_pattern → replacement` representation must be expanded to represent:

- Conditions
- Context
- Adhikāra
- Anuvṛtti
- Technical grammatical terms
- Exceptions
- Rule precedence
- Blocking
- Substitution operations
- Morphological features
- Phonological environment
- Rule interaction
- Asiddhatva/asiddhavat behaviour where relevant

This is one of the most important research components.

---

## Phase 1B — Grammar State Representation

**Status: NOT STARTED**

The current engine works primarily with strings.

We need a richer `GrammarState` containing information such as:

```text
surface form
morphemes
phonological representation
grammatical features
active conditions
previous transformations
applied rules
metadata
```

---

## Phase 2 — Real Pāṇinian Rule Interactions

**Status: NOT STARTED**

Implement a carefully selected set of authentic Pāṇinian rules and grammatical phenomena.

Initial target:

```text
10–15 validated rules
        ↓
20–30 rules
        ↓
additional phenomena
```

The priority is **correctness and experimental validity**, not maximum rule count.

---

## Phase 3 — Rule Dependency Graph

**Status: NOT STARTED**

Build a graph representing relationships such as:

```text
        R001
       /         R002   R003
       \    /
        R004
          |
        R007
```

Relationships may include:

- Explicit dependencies.
- Actual derivation interactions.
- Upstream/downstream effects.
- Shared grammatical states.
- Counterfactual effects.

Planned technology: **NetworkX**.

---

## Phase 4 — Counterfactual Experiment Engine

**Status: BASIC VERSION COMPLETE**

Currently supported:

- Disable a rule.

Still required:

### Remove

```text
Remove R007
→ recompute derivation
→ compare
```

### Reorder

```text
R001 → R002 → R003

vs.

R002 → R001 → R003
```

### Modify

Change a rule condition or operation and observe the resulting derivation.

### Batch experimentation

```text
For each rule R:
    disable R
    derive
    compare
    record impact
```

---

## Phase 5 — Comparison & Impact Analysis

**Status: NOT STARTED**

The system should compare:

```text
Original derivation
        vs
Counterfactual derivation
```

Potential measurements:

- **Rule Criticality:** How often disabling a rule changes or invalidates a target derivation.
- **Rule Influence:** How many downstream derivation steps are affected.
- **Dependency:** How many rules depend directly or indirectly on a rule.
- **Redundancy:** Whether a rule can be removed without changing selected derivations under the experimental conditions.

These metrics must be formally defined and validated during the research phase.

---

## Phase 6 — FastAPI Backend

**Status: NOT STARTED**

Planned API endpoints:

```text
GET    /rules
GET    /rules/{rule_id}

POST   /derive
POST   /experiment

POST   /rules/{rule_id}/disable
POST   /rules/{rule_id}/enable

GET    /dependencies
GET    /analysis
```

Technology:

```text
FastAPI
Pydantic
```

---

## Phase 7 — Web Interface

**Status: NOT STARTED**

Build an interactive research dashboard for:

- Sanskrit input.
- Original derivation.
- Rule-by-rule trace.
- Rule intervention.
- Counterfactual derivation.
- Original vs altered comparison.
- Dependency graph.
- Impact metrics.

Planned technology:

```text
React
Vite
React Flow
Plotly
```

---

## Phase 8 — Experimental Evaluation

**Status: NOT STARTED**

Required:

- Curated rule subset.
- Validated derivation examples.
- Baseline experiments.
- Counterfactual experiments.
- Quantitative metrics.
- Error analysis.
- Ablation studies.
- Comparison with existing computational approaches where appropriate.
- Reproducible experiments.

---

## Phase 9 — Research Paper

**Status: NOT STARTED**

The paper will document:

1. Introduction
2. Related Work
3. Research Gap
4. Methodology
5. Rule Representation
6. Derivation Engine
7. Counterfactual Experiments
8. Dependency and Impact Analysis
9. Experimental Results
10. Discussion
11. Limitations
12. Conclusion

Potential publication venues will be evaluated after experimental results are available.

---

# 5. Technology Stack

| Component | Technology |
|---|---|
| Programming | Python |
| Backend | FastAPI |
| Data Models | Pydantic |
| Rule Engine | Custom Python |
| Database | SQLite |
| Graph Analysis | NetworkX |
| Data Analysis | Pandas + NumPy |
| Sanskrit Utilities | Indic NLP tools + custom components |
| Frontend | React + Vite |
| Graph Visualization | React Flow |
| Charts | Plotly |
| Testing | Pytest |
| Version Control | Git + GitHub |
| IDE | VS Code |
| Containerization | **Not used** |

---

# 6. Development Roadmap

```text
PHASE 1    Core Prototype              🟡 IN PROGRESS
    ↓
PHASE 1A   Strong Rule Schema         ⬜
    ↓
PHASE 1B   Grammar State              ⬜
    ↓
PHASE 2    Real Rule Set              ⬜
    ↓
PHASE 3    Dependency Graph           ⬜
    ↓
PHASE 4    Counterfactual Engine      🟡 BASIC
    ↓
PHASE 5    Impact Analysis            ⬜
    ↓
PHASE 6    FastAPI                    ⬜
    ↓
PHASE 7    React Dashboard            ⬜
    ↓
PHASE 8    Experiments & Evaluation   ⬜
    ↓
PHASE 9    Research Paper             ⬜
```

---

# 7. Definition of Done

The project will be considered a successful prototype when a researcher can:

```text
1. Select a Sanskrit derivation
             ↓
2. View the original derivation
             ↓
3. Inspect every rule application
             ↓
4. Disable/remove a rule
             ↓
5. Re-run the derivation
             ↓
6. Compare both derivations
             ↓
7. Identify downstream changes
             ↓
8. View affected rule dependencies
             ↓
9. Obtain quantitative impact measurements
             ↓
10. Visualize the results
```

## Final Deliverables

### ① Working Model

A functional PĀṆINI-LAB prototype capable of controlled computational experiments over a validated subset of Pāṇinian grammar.

### ② Research Contribution

An experimental methodology and quantitative analysis of rule dependencies/interactions, documented in a research paper.

---

# 8. Immediate Next Task

> **PHASE 1A — Design a rigorous machine-readable representation for Pāṇinian rules and grammatical states.**

Do **not** build the React dashboard yet.

The quality of the rule and state representation will determine the reliability of every later component of PĀṆINI-LAB.

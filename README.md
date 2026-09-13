# PĀṆINI-LAB
## A Counterfactual Computational Framework for Rule-Dependency Analysis of Pāṇinian Grammar
PĀṆINI-LAB is a research-oriented computational framework for studying Pāṇinian grammar as an executable rule system.
The project does **not** attempt to claim that Pāṇini has never been computationalized. Existing research has already explored computational modelling, parsing, generation, rule interaction, and formalization of Pāṇinian grammar.
The distinctive goal of PĀṆINI-LAB is to treat the computational grammar itself as an object of controlled experimentation. The framework is designed to support rule tracing, dependency analysis, counterfactual interventions, rule-impact measurement, and eventually minimal-rule discovery.
---
## Project Vision
The central research question is:
> **What can we learn about the structure and importance of a grammatical rule system by systematically intervening in its rules and observing the resulting derivations?**
Instead of only asking:
```text
Input → What is the output?

PĀṆINI-LAB asks:

Input
  ↓
Which rules fired?
  ↓
What state did each rule receive?
  ↓
What state did it produce?
  ↓
What depends on what?
  ↓
What happens if a rule is removed?
  ↓
How does the derivation change?

This makes the system conceptually similar to a debugger for a formal grammar.

⸻

Current Project Status

Phase	Component	Status
Phase 1A	Rule schema and rule representation	✅ Complete
Phase 1B	Computational derivational state	✅ Complete
Phase 1B	Rule conditions and state transitions	✅ Complete
Phase 1B	Derivation history and trace	✅ Complete
Phase 1B	Counterfactual rule disabling	✅ Complete
Phase 1B	Automated tests	✅ Complete
Phase 2	Authentic validated Pāṇinian rule subset	🔜 Next
Phase 3	Rule-dependency graph	⏳ Planned
Phase 4	Advanced counterfactual engine	⏳ Planned
Phase 5	Rule-impact and redundancy analysis	⏳ Planned
Phase 6	FastAPI research API	⏳ Planned / basic structure exists
Phase 7	React interactive interface	⏳ Planned
Phase 8	Experimental evaluation	⏳ Planned
Phase 9	Research paper and final evaluation	⏳ Planned

⸻

Phase 1A — Rule Representation

Phase 1A established the structured representation of a grammatical rule.

Each rule can contain:

* Rule ID
* Sūtra reference
* Name
* Conditions
* Operations
* Priority
* Scope
* Dependencies
* Blocking metadata
* Enabled/disabled state
* Repeatability policy
* Status
* Description
* Additional metadata

The rule representation is deliberately designed to be extensible so that later phases can represent more complex grammatical behaviour without redesigning the complete architecture.

⸻

Phase 1B — Computational Derivational State

Phase 1B extends the rule schema into an executable state-transition system.

The key abstraction is:

Grammar State
      ↓
Rule Condition Evaluation
      ↓
Rule Application
      ↓
New Grammar State
      ↓
Derivation Record

Every successful rule application produces a new state and a trace record.

⸻

1. StateToken

A StateToken represents an individual computational token in the current derivational state.

A token contains:

Token ID
Surface form
Source / provenance
Features
Markers
Position
Active / inactive status

Example:

StateToken(
    token_id="t1",
    surface="ग",
    source="input",
    features={"category": "root"},
    markers=[],
    position=0,
    active=True
)

Stable token IDs allow future versions of the system to track how individual elements move through a derivation.

⸻

2. GrammarState

GrammarState represents the complete computational state at a particular point in a derivation.

It contains:

* Current tokens
* Global grammatical features
* Active rules
* Derivation step number
* History identifier
* Additional metadata

The current surface representation is generated from active tokens.

Example:

Tokens:
[t1 = अ, t2 = इ]
Surface:
अइ
Step:
0

After a transformation:

Tokens:
[t1 = ए]
Surface:
ए
Step:
1

⸻

Rule Conditions

Phase 1B currently supports the following condition types:

Pattern condition

Checks whether a pattern occurs in the current active surface sequence.

{
  "condition_type": "pattern",
  "pattern": "अइ"
}

Feature condition

Checks token-level grammatical features.

{
  "condition_type": "feature",
  "feature_key": "category",
  "feature_value": "verb"
}

Context condition

Allows a pattern to be evaluated together with left and/or right contextual constraints.

Marker condition

Checks whether a token carries a particular computational marker.

Custom condition

Reserved for future specialized linguistic evaluators.

Conditions can also be negated using:

"negate": true

⸻

Rule Operations

Phase 1B supports the following operation types:

Substitute

Target → Replacement

Insert

Adds a new token at a specified position.

Delete

Marks a target token as inactive rather than destroying its identity. This preserves derivational information for future analysis.

Feature update

Updates a grammatical feature attached to a token.

Marker add

Adds a computational marker to a token.

Marker remove

Removes a computational marker.

Custom

Reserved for future operations requiring specialized linguistic logic.

⸻

Rule Scope

Rules can specify where they are allowed to operate through:

* Domains
* Categories
* Required global features
* Excluded global features

This provides the foundation for more precise grammatical environments in later phases.

⸻

Rule Interaction Metadata

The rule model contains explicit fields for:

Dependencies
Blocking type
Blocks
Blocked by
Priority

These fields are currently part of the computational representation and validation layer.

The full linguistic interpretation of rule precedence, blocking, and interaction will be developed using the validated Pāṇinian rule subset in later phases.

⸻

Derivation Engine

The DerivationEngine executes a collection of enabled rules against an input state.

Rules are currently ordered deterministically using:

Priority descending
Rule ID ascending

A successful rule application produces:

Before State
      ↓
Rule
      ↓
After State

Each successful transformation is stored as a DerivationRecord.

The record contains:

* Step number
* Rule ID
* Sūtra reference
* Rule name
* Before surface
* After surface
* Complete before-state snapshot
* Complete after-state snapshot
* Explanation
* Metadata

This trace is essential for the future dependency graph and counterfactual analysis.

⸻

Rule Repeatability

Rules have an explicit repeatable property.

By default:

"repeatable": false

A non-repeatable rule can fire only once during a single derivation.

This prevents rules such as synthetic insertion rules from repeatedly modifying the same state indefinitely.

Example:

Input
  ↓
ग
  ↓ R003
गअ
  ↓
R003 already fired
  ↓
Stop

Repeatable rules can be enabled later when the linguistic semantics of repeated application are explicitly defined.

⸻

Counterfactual Experimentation

One of the central concepts of PĀṆINI-LAB is counterfactual analysis.

For an input and a rule set, the system can execute two derivations:

                 SAME INPUT
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
      BASELINE            COUNTERFACTUAL
          │                     │
     All rules            Selected rules
       enabled                disabled
          │                     │
          ↓                     ↓
     Derivation A          Derivation B
          │                     │
          └──────────┬──────────┘
                     ↓
                COMPARISON

The experiment records:

* Baseline output
* Counterfactual output
* Whether the output changed
* Number of derivation steps
* Changed derivation steps
* Rules involved in the changed steps

Example:

Baseline:
अइ → ए
Counterfactual:
R001 disabled
अइ → अइ
Output changed:
TRUE

This is the foundation for future rule-impact metrics.

⸻

Current Rule Dataset

The current Phase 1B dataset intentionally contains illustrative and synthetic rules for testing the framework.

Rule	Purpose	Status
R001	Illustrative vowel transformation	Illustrative
R002	Feature-state transition	Synthetic
R003	Positional insertion	Synthetic
R004	Token deletion	Synthetic
R005	Marker assignment	Synthetic

Important research note

R001 references Pāṇinian material for architectural testing, but it is not claimed to be a complete formal encoding of the referenced sūtra.

The synthetic rules are deliberately separated from the authentic grammatical rule set.

The next phase will introduce a small, carefully verified subset of actual Pāṇinian rules and validated derivation examples.

⸻

Testing

Automated tests are maintained under:

backend/tests/

Run the complete test suite using:

python -m pytest -q

Phase 1B tests cover areas including:

* Token features
* Token markers
* Grammar-state construction
* State snapshots
* Substitution
* Insertion
* Deletion
* Feature updates
* Counterfactual experiments
* Rule registry loading
* Rule enabling/disabling

The test suite is intended to ensure that architectural changes do not silently break existing derivation behaviour.

⸻

Technology Stack

Backend

* Python 3.11+
* FastAPI
* Pydantic
* Custom Python rule engine
* SQLite — planned for persistent experiment data
* NetworkX — planned for dependency graphs
* NumPy
* Pandas

Frontend

Planned:

* React
* Vite
* React Flow
* Plotly

Development

* Git
* GitHub
* Visual Studio Code

Deployment

Docker is not used in this project.

⸻

Project Architecture

Current conceptual architecture:

                 Sanskrit / Grammar Input
                           │
                           ▼
                  ┌─────────────────┐
                  │ Derivation      │
                  │ Engine          │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Grammar State   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Rule Evaluation │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ State Transition│
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Rule Trace      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Counterfactual  │
                  │ Experiment      │
                  └────────┬────────┘
                           │
                           ▼
                    Comparative Data

Future architecture:

Input
  ↓
Derivation Engine
  ↓
Rule Trace + State History
  ↓
Dependency Analyzer
  ↓
Counterfactual Engine
  ↓
Impact / Redundancy Analysis
  ↓
Interactive Visualization

⸻

Development Roadmap

Phase 1A — Rule Schema

Completed.

Goal:

Define a flexible machine-readable representation for grammatical rules.

⸻

Phase 1B — Derivational State

Completed.

Goal:

Make grammatical rules operate on explicit computational states and produce traceable state transitions.

Deliverables completed:

* Token model
* Features
* Markers
* State snapshots
* Conditions
* Operations
* Derivation history
* Rule repeatability control
* Counterfactual baseline comparison
* Automated tests

⸻

Phase 2 — Authentic Pāṇinian Rule Subset

Next.

The project will encode a deliberately limited and academically defensible subset of actual Pāṇinian rules.

Each selected rule should have:

1. Verified sūtra reference
2. Clearly defined grammatical environment
3. Computational representation
4. Explicit operation
5. Interaction/precedence information where applicable
6. At least one validated derivation example
7. Tests covering expected behaviour

The initial goal is correctness over quantity.

A small validated rule set is preferable to a large collection of uncertain encodings.

⸻

Phase 3 — Rule Dependency Graph

Build a graph where:

Rule A → Rule B

means that Rule B’s successful application depends on a state produced or modified by Rule A.

Potential graph properties:

* Incoming dependencies
* Outgoing dependencies
* Rule centrality
* Dependency chains
* Blocking relationships
* Derivation-path structure

NetworkX will be used for the initial implementation.

⸻

Phase 4 — Advanced Counterfactual Engine

Extend counterfactual experiments beyond simple disabling.

Planned interventions:

Remove rule
Disable rule
Reorder rules
Modify rule condition
Modify rule operation
Change priority

The system will compare baseline and altered derivations automatically.

⸻

Phase 5 — Rule Impact Analysis

Develop quantitative measurements such as:

* Number of derivations affected
* Output-change rate
* Number of downstream rules affected
* Average derivation distance affected
* Dependency centrality
* Rule sensitivity
* Potential redundancy indicators

These measurements will form the basis for experimental research.

⸻

Phase 6 — API Layer

Expose the computational engine through FastAPI.

Planned endpoints include:

GET  /rules
GET  /rules/{rule_id}
POST /derive
POST /experiment

The API will eventually support graph queries and experiment management.

⸻

Phase 7 — Interactive Interface

The frontend will allow users to:

1. Enter an input.
2. Run a derivation.
3. Inspect every rule application.
4. View intermediate states.
5. Inspect rule dependencies.
6. Disable or modify rules.
7. Re-run the derivation.
8. Compare baseline and counterfactual results.
9. Visualize impact.

⸻

Phase 8 — Experimental Evaluation

Experiments will evaluate questions such as:

* Which rules have the largest downstream influence?
* Which rules are repeatedly involved in successful derivations?
* Which rules produce the largest state changes?
* Which interventions cause derivation failure?
* Are there rules whose removal does not affect selected derivations?
* How strongly are rules connected through derivational dependencies?

Results will be stored in a reproducible experimental format.

⸻

Phase 9 — Research Output

Expected outputs include:

1. Working software prototype

An interactive computational environment for controlled analysis of a selected Pāṇinian rule system.

2. Research paper

The paper will document:

* Computational representation
* Rule encoding methodology
* Dependency modelling
* Counterfactual methodology
* Experimental setup
* Quantitative results
* Limitations
* Future work

3. Software copyright / research artifact

Copyright protection and publication are realistic potential outputs for the software artifact.

Patent feasibility, if considered, will require a separate prior-art and patentability assessment rather than being assumed in advance.

⸻

Definition of Done for Phase 1B

Phase 1B is considered complete when:

* [x]	Rules can be represented structurally.
* [x]	Tokens have stable identities.
* [x]	Tokens can carry features.
* [x]	Tokens can carry markers.
* [x]	Tokens maintain positions.
* [x]	Grammar state can be snapshotted.
* [x]	Conditions can be evaluated.
* [x]	State-transforming operations can be executed.
* [x]	Derivation steps are recorded.
* [x]	Rule applications are deterministic.
* [x]	Non-repeatable rules cannot fire indefinitely.
* [x]	Rules can be disabled for counterfactual experiments.
* [x]	Baseline and counterfactual derivations can be compared.
* [x]	Automated tests cover the core behaviour.

⸻

Repository Structure

panini-lab/
│
├── README.md
├── .gitignore
│
└── backend/
    │
    ├── requirements.txt
    │
    ├── app/
    │   ├── __init__.py
    │   │
    │   ├── main.py
    │   │
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── rule_engine.py
    │   │   ├── derivation.py
    │   │   ├── registry.py
    │   │   └── experiment.py
    │   │
    │   └── data/
    │       └── rules.json
    │
    └── tests/
        ├── __init__.py
        ├── test_engine.py
        ├── test_phase1a.py
        └── test_phase1b.py

⸻

Running the Project

Create and activate the virtual environment:

cd backend
python3 -m venv venv
source venv/bin/activate

Install dependencies:

python -m pip install -r requirements.txt

Run tests:

python -m pytest -q

Run the application:

python -m app.main

For the FastAPI development server:

uvicorn app.main:app --reload

API documentation will be available at:

http://127.0.0.1:8000/docs

⸻

Research Positioning

PĀṆINI-LAB is positioned at the intersection of:

* Indian Knowledge Systems
* Sanskrit computational linguistics
* Formal grammar
* Rule-based systems
* Program analysis
* Dependency graphs
* Counterfactual analysis
* Interactive visualization

The project’s contribution is intended to be methodological: using controlled computational interventions to study the behaviour and structural dependencies of a formal grammatical rule system.

The project therefore focuses on experimentally analysing the rule system rather than merely implementing a Sanskrit parser or generator.

⸻

Current Milestone

Phase 1B — COMPLETE ✅

The computational foundation is now ready for the next research milestone:

Phase 2 — Build and validate the first authentic Pāṇinian rule subset.

At that stage, synthetic rules will no longer be sufficient for the main experiments. Every rule included in the research dataset should be traceable to a documented grammatical source and tested against known derivational behaviour.

⸻

Status

Current version: 0.2 — Phase 1B

Project: PĀṆINI-LAB

Primary goal: Counterfactual computational analysis of Pāṇinian rule dependencies
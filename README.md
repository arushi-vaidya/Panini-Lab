

# PĀṆINI-LAB
## A Counterfactual Computational Framework for Rule-Dependency Analysis of Pāṇinian Grammar
PĀṆINI-LAB is a research-oriented computational framework for modeling selected rules of Pāṇinian grammar as an executable rule system and experimentally analyzing their interactions.
The central idea is to treat a computationalized subset of the Aṣṭādhyāyī not merely as a grammar implementation, but as an experimental system that can be inspected, traced, modified, and tested under controlled counterfactual conditions.
The long-term objective is to build a computational "debugger for grammar" that allows researchers to:
- Execute selected Pāṇinian rules.
- Inspect derivations step-by-step.
- Construct rule-dependency graphs.
- Mine rule interactions from actual derivations.
- Remove, reorder, or modify rules.
- Compare original and counterfactual derivations.
- Quantify rule impact.
- Investigate possible redundancy and conflicts.
- Search for minimal rule subsets.
- Visualize grammatical rule interactions.
---
# 1. Project Motivation
Pāṇini's Aṣṭādhyāyī is a highly structured grammatical system in which rules interact through ordering, contextual conditions, blocking relationships, technical terminology, and other mechanisms.
Existing computational work has demonstrated that Pāṇinian grammar can be computationally modeled and applied to Sanskrit processing.
PĀṆINI-LAB focuses on a complementary question:
> What can we discover about the behavior of a computationalized grammatical system by experimentally intervening in its rules?
Instead of only asking:
    Input → Correct Output
PĀṆINI-LAB investigates:
    Input
      ↓
    Which rules fired?
      ↓
    In what order?
      ↓
    Which rules interacted?
      ↓
    What changes if a rule is removed?
      ↓
    What changes if rule ordering is modified?
      ↓
    How important was the rule?
This makes the computational grammar itself the object of experimentation.
---
# 2. Research Objective
The primary research objective is:
> To develop a computational framework for controlled analysis of rule dependencies and interactions in a selected subset of Pāṇinian grammar using executable derivations and counterfactual interventions.
The framework is intended to investigate:
1. Rule applicability.
2. Rule execution order.
3. Rule dependencies.
4. Rule blocking.
5. Empirically observed rule interactions.
6. Effects of rule removal.
7. Effects of rule reordering.
8. Effects of rule modification.
9. Rule-level impact.
10. Potentially redundant or conflicting rules.
11. Minimal rule subsets capable of reproducing observed outputs.
---
# 3. Research Novelty
PĀṆINI-LAB does not claim that Pāṇinian grammar has never been computationalized.
Prior research has explored computational modeling, formalization, finite-state representations, and Sanskrit NLP based on Pāṇinian principles.
The proposed contribution is instead:
> An integrated experimental framework that treats a computational representation of selected Pāṇinian rules as an object of controlled intervention, enabling derivation tracing, empirical interaction mining, counterfactual rule analysis, rule-impact measurement, and minimal-rule discovery.
The novelty therefore lies in combining:
- Executable rule representation
- Derivation tracing
- Dependency graphs
- Empirical interaction mining
- Counterfactual experimentation
- Rule-impact analysis
- Interactive visualization
into one experimental framework.
---
# 4. Scope
PĀṆINI-LAB is currently scoped as a research prototype.
It does NOT attempt to computationally implement the entire Aṣṭādhyāyī.
The current validated linguistic scope consists of a small subset of Pāṇinian vowel-sandhi rules.
The project prioritizes:
> Correctness and experimental validity over the number of rules implemented.
The initial validated subset contains five sūtras:
1. 6.1.77 — इको यणचि
2. 6.1.78 — एचोऽयवायावः
3. 6.1.87 — आद्गुणः
4. 6.1.88 — वृद्धिरेचि
5. 6.1.101 — अकः सवर्णे दीर्घः
The rule set can be expanded after the computational representation and experiments are validated.
---
# 5. System Architecture
Current architecture:
    Sanskrit Input
          ↓
    Sanskrit Tokenization
          ↓
    Rule Registry
          ↓
    Rule Engine
          ↓
    Derivation Engine
          ↓
    Derivation Trace
          ↓
    Interaction Miner
          ↓
    Dependency Graph
          ↓
    Counterfactual Engine
          ↓
    Comparative Analysis
          ↓
    Visualization
          ↓
    Research Experiments
The Counterfactual Engine, Comparative Analysis, and Visualization components are planned future stages.
---
# 6. Development Status
| Phase | Component | Status |
|---|---|---|
| Phase 1A | Rule representation | ✅ Complete |
| Phase 1B | Executable rule engine | ✅ Complete |
| Phase 2 | Validated Pāṇinian vowel-sandhi subset | ✅ Complete |
| Phase 3A | Static dependency graph | ✅ Complete |
| Phase 3B | Derivation-aware interaction mining | ✅ Complete |
| Phase 4 | Counterfactual engine | ⏳ Planned |
| Phase 5 | Rule-impact analysis | ⏳ Planned |
| Phase 6 | Backend/API integration | ⏳ Planned |
| Phase 7 | Interactive visualization | ⏳ Planned |
| Phase 8 | Experimental evaluation | ⏳ Planned |
| Phase 9 | Research output | ⏳ Planned |
---
# 7. Phase 1A — Rule Representation
## Status: COMPLETE
Phase 1A established the structured representation of grammatical rules and grammar states.
Each rule is represented using structured data rather than being hard-coded directly into the execution engine.
A rule contains information including:
- Rule ID
- Sūtra number
- Sanskrit sūtra
- Name
- Description
- Conditions
- Operations
- Priority
- Scope
- Dependencies
- Blocking relationships
- Examples
- Status
- Repeatability
- Metadata
---
## Rule Conditions
The rule representation supports:
- `pattern`
- `feature`
- `marker`
- `context_pair`
These provide the foundation for expressing increasingly complex rule applicability conditions.
---
## Rule Operations
The current rule model supports:
- `substitute`
- `contextual_substitute`
- `contextual_pair_substitute`
- `insert`
- `delete`
- `feature_update`
- `marker_add`
- `marker_remove`
---
# 8. Phase 1B — Executable Rule Engine
## Status: COMPLETE
Phase 1B converted the structured rule representation into an executable rule system.
The RuleEngine provides:
    evaluate(rule, state)
    apply(rule, state)
The engine determines whether a rule is applicable to the current grammar state and applies the corresponding operation.
---
## Derivation Engine
The DerivationEngine repeatedly evaluates enabled rules according to their configured priorities.
A derivation produces:
- Initial grammar state
- Final grammar state
- Applied rules
- Derivation steps
- Rule metadata
- Skipped rules
- Disabled rules
- Termination reason
---
## Repeatability
Rules contain a `repeatable` property.
This prevents rules that are intended to fire once from being repeatedly applied during the same derivation.
This also prevents uncontrolled transformations and infinite derivation loops in the simplified computational model.
---
# 9. Derivation Trace
Each applied rule generates a derivation step containing:
- Step number
- Rule ID
- Sūtra
- Rule name
- Surface form before application
- Surface form after application
- Complete state before application
- Complete state after application
- Whether the state changed
- Explanation
- Rule metadata
A derivation therefore becomes inspectable rather than being represented only by its final output.
Example conceptual trace:
    Input
      ↓
    Rule A
      ↓
    Intermediate State
      ↓
    Rule B
      ↓
    Final State
This trace becomes the primary evidence source for Phase 3B interaction mining and future counterfactual experiments.
---
# 10. Phase 2 — Pāṇinian Vowel Sandhi
## Status: COMPLETE
Phase 2 replaced the initial synthetic rule demonstrations with a validated computational subset of five Pāṇinian vowel-sandhi sūtras.
---
## 10.1 — 6.1.77 — इको यणचि
Rule ID:
    P60177
Representative tests include:
    इअ → यअ
    उअ → वअ
    ऋअ → रअ
---
## 10.2 — 6.1.78 — एचोऽयवायावः
Rule ID:
    P60178
Representative tests include:
    एअ → अयअ
    ओअ → अवअ
---
## 10.3 — 6.1.87 — आद्गुणः
Rule ID:
    P60187
Representative tests include:
    अइ → ए
    अउ → ओ
---
## 10.4 — 6.1.88 — वृद्धिरेचि
Rule ID:
    P60188
Representative tests include:
    अए → ऐ
    अओ → औ
---
## 10.5 — 6.1.101 — अकः सवर्णे दीर्घः
Rule ID:
    P601101
Representative tests include:
    अअ → आ
    इइ → ई
    उउ → ऊ
The test suite also checks the modeled interaction in which the homogeneous-vowel case takes precedence over the relevant `yaṇ` transformation.
---
# 11. Sanskrit Tokenization
A lightweight Sanskrit tokenizer is currently implemented.
Input is converted into grammar-state tokens containing:
- Token ID
- Surface form
- Source
- Features
- Markers
- Position
- Active state
Example:
    इअ
is represented as a sequence of grammar-state tokens.
The tokenizer is intentionally lightweight at the current prototype stage.
---
## Current limitation
The current representation operates at a character/token level and should not be interpreted as a complete Sanskrit phonological or morphological representation.
A future version can introduce richer linguistic units and phonological representations.
---
# 12. Phase 3A — Static Dependency Graph
## Status: COMPLETE
Phase 3A introduced the `DependencyGraph` abstraction using NetworkX.
Each grammatical rule becomes a graph node.
Current rule nodes include:
    P60177
    P60178
    P60187
    P60188
    P601101
---
## Node Metadata
Nodes contain information including:
- Rule ID
- Sūtra number
- Sanskrit sūtra
- Rule name
- Status
- Priority
- Enabled state
---
## Graph Relationships
The graph supports relationships such as:
### depends_on
Represents an explicitly declared dependency.
### blocks
Represents a blocking relationship between rules.
### blocked_by
Represents the inverse blocking relationship and is normalized into graph edges.
---
## Dependency Graph API
The current graph supports:
    get_nodes()
    get_edges()
    get_dependencies(rule_id)
    get_blocked_rules(rule_id)
    get_blocking_rules(rule_id)
    to_dict()
    has_cycle()
    topological_order()
The graph can therefore be inspected, serialized, checked for cycles, and topologically ordered when possible.
---
# 13. Phase 3B — Derivation-Aware Interaction Mining
## Status: COMPLETE
Phase 3B extends the static dependency representation by analyzing actual derivation traces.
The central idea is:
    Rule Metadata
          +
    Actual Derivation Traces
          ↓
    Observed Rule Interactions
The implementation is contained in:
    app/core/interaction_miner.py
---
# 14. Interaction Miner
The InteractionMiner analyzes the rules that actually fired during a derivation.
For example, if a derivation produces:
    P60101
    P60177
    P60187
the miner can record pairwise observations such as:
    P60101 → P60177
    P60101 → P60187
    P60177 → P60187
---
## Current Empirical Interaction Types
### observed_before
Records that Rule A was observed executing before Rule B in a derivation.
### co_fired
Records that Rule A and Rule B participated in the same derivation.
These relationships are empirical observations.
They are NOT automatically treated as formal grammatical dependencies.
---
# 15. Empirical Evidence
Each observed interaction stores:
- Source rule
- Target rule
- Relationship type
- Observation count
- Example inputs
Conceptually:
```json
{
  "source": "P60101",
  "target": "P60177",
  "relation": "observed_before",
  "count": 7,
  "examples": [
    "example1",
    "example2"
  ]
}

This makes interactions traceable to actual derivation evidence.

⸻

16. Declared vs Observed Relationships

PĀṆINI-LAB deliberately distinguishes between different levels of evidence.

Relationship	Meaning
depends_on	Explicitly declared relationship
blocks	Explicitly modeled blocking relationship
observed_before	Observed execution ordering
co_fired	Rules observed in the same derivation

An observed ordering is not automatically considered a formal grammatical dependency.

For example:

A happened before B

does not necessarily prove:

A is a formal dependency of B

because the observed ordering could be caused by the particular input or rule configuration.

This distinction is important for the later counterfactual experiments.

⸻

17. Interaction-Based Graph Construction

The dependency graph can also be constructed from empirical interactions.

The system supports the conceptual flow:

Derivation
    ↓
Interaction Miner
    ↓
Observed Interactions
    ↓
Empirical Dependency Graph

Empirical graph edges can retain:

* Relationship type
* Observation count
* Example inputs
* Source type

This allows the system to preserve evidence for graph relationships.

⸻

18. Testing

Testing is integrated throughout the project.

Run all tests:

python -m pytest -q

Run Phase 2:

python -m pytest tests/test_phase2_sandhi.py -q

Run dependency graph tests:

python -m pytest tests/test_dependency_graph.py -q

Run interaction-mining tests:

python -m pytest tests/test_interaction_miner.py -q

⸻

Current Test Coverage

Tests currently cover:

Phase 1B

* Rule loading
* Rule evaluation
* Rule application
* Derivation behavior
* Repeatability

Phase 2

* 6.1.77
* 6.1.78
* 6.1.87
* 6.1.88
* 6.1.101
* Representative sandhi transformations
* Rule metadata

Phase 3A

* Graph node creation
* Rule IDs
* Dependency edges
* Graph serialization
* Blocking relationships
* Cycle detection

Phase 3B

* Interaction mining
* Ordered rule interactions
* Co-firing observations
* Interaction serialization
* Miner reset/clear behavior

All currently implemented phases have passing tests.

⸻

19. Phase 4 — Counterfactual Engine

Status: PLANNED

Phase 4 is the next major development stage.

The Counterfactual Engine will allow controlled interventions in the rule system.

The primary intervention types will be:

1. Rule removal
2. Rule reordering
3. Rule modification
4. Batch experimentation

⸻

19.1 Rule Removal

Given:

Input
  ↓
Rule A
  ↓
Rule B
  ↓
Output X

the counterfactual system will disable Rule A:

Input
  ↓
Rule B
  ↓
Output Y

The system will then compare:

X vs Y

⸻

19.2 Rule Reordering

The system will modify execution order:

A → B

to:

B → A

and determine whether the resulting derivation changes.

⸻

19.3 Rule Modification

A rule can eventually be experimentally modified by changing:

* Conditions
* Operations
* Priority
* Scope
* Mappings

The resulting derivation can then be compared against the baseline.

⸻

19.4 Batch Counterfactual Experiments

For a set of rules:

R1
R2
R3
R4

the system can automatically execute:

Baseline
Remove R1
Remove R2
Remove R3
Remove R4

and collect the resulting differences.

⸻

20. Counterfactual Comparison

Each experiment should retain:

* Input
* Baseline output
* Counterfactual output
* Baseline fired rules
* Counterfactual fired rules
* Changed rules
* Changed derivation steps
* Removed rules
* Newly activated rules
* Experiment configuration

Conceptually:

Baseline
   ↓
Derivation A
   ↓
Output A
Counterfactual
   ↓
Derivation B
   ↓
Output B

The comparison layer then identifies the differences.

⸻

21. Phase 5 — Rule Impact Analysis

Status: PLANNED

Phase 5 will quantify the effect of rules using counterfactual results.

Potential metrics include:

Output Impact

Percentage of evaluation inputs for which disabling a rule changes the final output.

output_impact =
    changed_outputs / total_inputs

⸻

Derivation Impact

Measures how many derivation steps change after an intervention.

⸻

Rule-Firing Impact

Measures how disabling a rule changes downstream rule firing.

⸻

Dependency Impact

Measures how many observed interactions disappear after intervention.

⸻

Impact Ranking

Rules can eventually be ranked by their measured effect.

Example:

Rule       Output Impact
------------------------
R1         72%
R2         41%
R3         12%
R4          0%

These values are examples only; actual values will come from experiments.

⸻

22. Redundancy Analysis

The system will investigate potential rule redundancy experimentally.

For a rule R:

Run baseline
     ↓
Disable R
     ↓
Run same dataset
     ↓
Compare outputs

If no output changes occur on the evaluation dataset, the system should report:

No observed output impact

rather than making the universal claim:

Rule R is redundant

because the conclusion is limited to the selected rule set and evaluation corpus.

⸻

23. Conflict Analysis

The system will eventually identify cases where multiple rules are simultaneously applicable.

For example:

Input
  ↓
Rule A applicable
Rule B applicable

The system can investigate:

* Priority
* Execution order
* Blocking
* Final output
* Counterfactual ordering
* Resulting derivation traces

This provides a computational basis for investigating rule conflicts and competition.

⸻

24. Minimal Rule-Set Discovery

A longer-term experiment will search for the smallest rule subset that reproduces the desired outputs over a defined evaluation dataset.

Conceptually:

Full Rule Set
      ↓
Remove Candidate Rules
      ↓
Re-run Dataset
      ↓
Compare Outputs
      ↓
Find Smallest Valid Subset

This could provide quantitative evidence about the contribution of individual rules to a defined computational task.

⸻

25. Phase 6 — Backend/API

Status: PLANNED

A FastAPI backend will expose the computational framework through REST endpoints.

Planned stack:

* Python
* FastAPI
* Pydantic
* NetworkX
* Pandas
* NumPy
* SQLite

⸻

Planned API

Derivation

POST /derive

Example request:

{
  "input": "अइ"
}

Example conceptual response:

{
  "input": "अइ",
  "output": "ए",
  "steps": []
}

⸻

Rules

GET /rules
GET /rules/{rule_id}

⸻

Dependency Graph

GET /graph

⸻

Counterfactual

POST /counterfactual

⸻

Experiments

POST /experiments
GET /experiments/{experiment_id}

⸻

26. Phase 7 — Interactive Visualization

Status: PLANNED

The planned frontend stack is:

* React
* Vite
* React Flow / D3
* Plotly

The UI will provide three primary views.

⸻

26.1 Derivation Viewer

Users will be able to inspect:

Input
  ↓
Step 1 — Rule
  ↓
Intermediate State
  ↓
Step 2 — Rule
  ↓
Final Output

Each rule can expose its metadata.

⸻

26.2 Dependency Graph Viewer

The graph will display:

Rule A
  ↓
Rule B
  ↓
Rule C

with different relationship types represented visually.

⸻

26.3 Counterfactual Viewer

The UI will eventually show:

ORIGINAL                 COUNTERFACTUAL
Input                    Input
  ↓                        ↓
Rule A                   Rule B
  ↓                        ↓
Rule B                   Output
  ↓
Output

with differences highlighted.

⸻

27. Phase 8 — Experimental Evaluation

Status: PLANNED

Once the counterfactual system is complete, a controlled evaluation dataset will be constructed.

The initial target is a carefully validated rule subset, potentially expanding from approximately:

10–15 rules

toward:

20–30 rules

depending on implementation correctness and project scope.

⸻

Planned Experiments

Experiment 1 — Baseline Derivations

Measure:

Input → Output

and collect complete traces.

⸻

Experiment 2 — Rule Removal

Remove each rule individually and measure:

* Output changes
* Derivation changes
* Downstream rule changes

⸻

Experiment 3 — Rule Reordering

Modify rule ordering and measure:

* Output differences
* Trace differences
* Interaction differences

⸻

Experiment 4 — Interaction Frequency

Measure how frequently relationships such as:

A → B

are observed across the dataset.

⸻

Experiment 5 — Rule Impact Ranking

Rank rules according to experimentally measured impact.

⸻

Experiment 6 — Minimal Rule Set

Search for a smaller subset capable of reproducing the required outputs over the evaluation set.

⸻

28. Experimental Methodology

The experimental methodology will follow:

1. Define rule subset
       ↓
2. Define evaluation inputs
       ↓
3. Run baseline derivations
       ↓
4. Record traces
       ↓
5. Mine interactions
       ↓
6. Perform counterfactual intervention
       ↓
7. Re-run derivations
       ↓
8. Compare results
       ↓
9. Calculate metrics
       ↓
10. Analyze findings

The system should preserve enough information to make every reported result traceable to an input and derivation.

⸻

29. Phase 9 — Research Output

Status: PLANNED

The final project is intended to produce:

Working Software Prototype

A functioning PĀṆINI-LAB implementation.

Rule Dataset

Structured computational representations of the selected Pāṇinian rules.

Derivation Dataset

Inputs, outputs, and complete rule traces.

Dependency Graph

A graph containing declared and empirically observed relationships.

Counterfactual Results

Experiments involving:

* Rule removal
* Rule reordering
* Rule modification

Quantitative Analysis

Including:

* Rule impact
* Interaction frequency
* Potential redundancy
* Conflicts
* Minimal rule subsets

Research Paper

Potential areas include:

* Computational linguistics
* Sanskrit computational linguistics
* Formal grammar
* Indian Knowledge Systems
* Explainable rule systems
* Rule dependency analysis

Software Copyright

The software implementation may be considered for copyright registration/documentation.

Patent Assessment

Patentability should not be assumed.

A formal prior-art and patentability assessment would be required before pursuing a patent.

⸻

30. Technology Stack

Backend

Python 3.11+
FastAPI
Pydantic
NetworkX
Pandas
NumPy
SQLite

Frontend

React
Vite
React Flow
D3
Plotly

Development

Git
GitHub
Visual Studio Code
pytest

Docker is currently not used.

⸻

31. Repository Structure

Panini-Lab/
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
    │   ├── main.py
    │   │
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── rule_engine.py
    │   │   ├── derivation.py
    │   │   ├── registry.py
    │   │   ├── experiment.py
    │   │   ├── sanskrit.py
    │   │   ├── dependency_graph.py
    │   │   └── interaction_miner.py
    │   │
    │   └── data/
    │       └── rules.json
    │
    └── tests/
        ├── __init__.py
        ├── test_phase1b.py
        ├── test_phase2_sandhi.py
        ├── test_dependency_graph.py
        └── test_interaction_miner.py

⸻

32. Current Limitations

PĀṆINI-LAB is currently a research prototype rather than a complete implementation of the Aṣṭādhyāyī.

Limited Rule Coverage

Only five Pāṇinian vowel-sandhi rules are currently included in the validated subset.

⸻

Simplified Tokenization

The Sanskrit representation currently uses a lightweight token-level representation.

⸻

Simplified Contextual Reasoning

The rule engine currently models only the contexts required for the selected subset.

⸻

Simplified Rule Ordering

Priority currently provides the primary execution ordering mechanism.

A broader implementation may require more detailed modeling of:

* Rule precedence
* Blocking
* Contextual applicability
* Anuvṛtti
* Adhikāra
* Paribhāṣā
* Technical grammatical categories

where relevant to the selected rule scope.

⸻

Empirical Interaction Is Not Formal Dependency

An observed relationship is treated as evidence of interaction, not automatically as proof of a formal grammatical dependency.

This is why Phase 4 counterfactual experimentation is important.

⸻

33. Design Principles

PĀṆINI-LAB follows several principles.

1. Traceability

Every computational result should be traceable to the rules and states that produced it.

2. Reproducibility

Experiments should be repeatable with the same rule configuration and input set.

3. Controlled Intervention

Counterfactual changes should modify one clearly defined aspect of the rule system at a time where possible.

4. Conservative Interpretation

Observed computational behavior should not automatically be generalized into universal grammatical claims.

5. Modular Architecture

Rules, derivations, graph analysis, counterfactual experiments, and visualization should remain separable components.

6. Test-Driven Development

Every major computational component should have automated tests.

⸻

34. Research Interpretation

The system should distinguish carefully between:

Computational Observation

and:

Linguistic Conclusion

For example:

"Rule A fired before Rule B in 15/20 derivations"

is a computational observation.

It does not automatically establish:

"Rule A is formally dependent on Rule B."

Similarly:

"Removing Rule A changed 40% of outputs"

is an experimental result.

It should not automatically be interpreted as:

"Rule A is universally more important than Rule B."

All conclusions should be qualified by:

* Rule subset
* Evaluation dataset
* Computational representation
* Experimental configuration

⸻

35. Roadmap

PHASE 1A
Rule Representation
       ↓
PHASE 1B
Executable Rule Engine
       ↓
PHASE 2
Validated Pāṇinian Vowel-Sandhi Subset
       ↓
PHASE 3A
Static Dependency Graph
       ↓
PHASE 3B
Derivation-Aware Interaction Mining
       ↓
PHASE 4
Counterfactual Engine
       ↓
PHASE 5
Impact / Redundancy / Conflict Analysis
       ↓
PHASE 6
FastAPI Backend
       ↓
PHASE 7
Interactive Visualization
       ↓
PHASE 8
Experimental Evaluation
       ↓
PHASE 9
Research Output

⸻

36. Completed Milestones

Current completed milestones:

* [x]	Project repository initialized
* [x]	Initial rule schema
* [x]	Grammar state representation
* [x]	Rule condition framework
* [x]	Rule operation framework
* [x]	Rule registry
* [x]	Executable RuleEngine
* [x]	DerivationEngine
* [x]	Derivation traces
* [x]	Rule repeatability handling
* [x]	Sanskrit tokenization
* [x]	Five validated Pāṇinian vowel-sandhi rules
* [x]	Phase 2 automated tests
* [x]	Static dependency graph
* [x]	Dependency graph tests
* [x]	Derivation-aware interaction miner
* [x]	Empirical interaction representation
* [x]	Interaction-mining tests
* [x]	Full test suite passing

⸻

37. Current Milestone

PĀṆINI-LAB has progressed from a structured rule representation to an executable and traceable computational model of a validated five-rule Pāṇinian vowel-sandhi subset. Phase 3 extends this system with static dependency modeling and derivation-aware empirical interaction mining, providing the foundation for controlled counterfactual experiments.

⸻

38. Immediate Next Step

The next development stage is:

PHASE 4 — COUNTERFACTUAL ENGINE

The first implementation target is controlled rule removal:

Baseline
    ↓
Run derivation
    ↓
Record output + trace
    ↓
Disable Rule R
    ↓
Run identical derivation
    ↓
Compare
    ↓
Record differences

This will establish the core experimental capability of PĀṆINI-LAB.

⸻

39. Long-Term Vision

The final PĀṆINI-LAB system should allow a researcher to enter a Sanskrit input and inspect not only its output, but the behavior of the computational grammar that produced it.

The intended workflow is:

                     Sanskrit Input
                           │
                           ▼
                  ┌─────────────────┐
                  │ Derivation      │
                  │ Engine          │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Rule Trace      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Interaction     │
                  │ Miner           │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Dependency      │
                  │ Graph           │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Counterfactual  │
                  │ Engine          │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Impact Analysis │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Research        │
                  │ Results         │
                  └─────────────────┘

The ultimate objective is not simply to build a Sanskrit grammar program.

It is to develop an experimental computational laboratory for studying the behavior, dependencies, interactions, and causal importance of a formally represented subset of Pāṇinian grammatical rules.

⸻

40. Project Status

Completed

Phase 1A  ✅
Phase 1B  ✅
Phase 2   ✅
Phase 3A  ✅
Phase 3B  ✅

Next

Phase 4   ⏳ Counterfactual Engine

Remaining

Phase 5   ⏳ Impact Analysis
Phase 6   ⏳ Backend/API
Phase 7   ⏳ Visualization
Phase 8   ⏳ Experimental Evaluation
Phase 9   ⏳ Research Output

⸻

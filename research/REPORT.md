# PĀṆINI-LAB Research Report

## Title

**An Executable Experimental Framework for Pāṇinian Sandhi Rule Analysis**

## Abstract

PĀṆINI-LAB models a selected subset of Aṣṭādhyāyī sandhi rules as executable, inspectable transformations. The system combines deterministic derivation traces, counterfactual rule removal, rule-order intervention, dependency graphs, empirical interaction mining, and rule-impact analysis in one research interface.

The Phase 8 evaluation protocol tested 16 curated Sanskrit sequences against the current 11-rule executable subset. All 16 cases matched their expected outputs, and all 11 registered rules fired in at least one evaluation case. These results validate the internal consistency of the current prototype corpus; they do not establish coverage or correctness for the complete Aṣṭādhyāyī.

## Research Question

Can a computational grammar be treated as an experimental object whose rules can be traced, removed, reordered, and measured to reveal dependencies and output impact?

## System Scope

The implementation currently contains 11 executable rules:

- Eight validated-subset rules covering vowel sandhi and core consonant transformations.
- Three explicitly marked experimental-subset rules for simplified visarga, devoicing, and anusvāra environments.

The tokenizer is character-level and the grammar state is a sequence of active tokens. This is a deliberately constrained research prototype, not a complete Sanskrit parser or complete implementation of the Aṣṭādhyāyī.

## Evaluation Protocol

The evaluation corpus is stored in `backend/app/data/evaluation_cases.json` and is executed by `backend/app/core/evaluation.py`.

For each case, the evaluator records:

1. Input surface.
2. Expected output.
3. Actual deterministic output.
4. Exact-match pass/fail status.
5. Rules fired.
6. Number of derivation steps.
7. Termination reason.

The evaluator also disables each rule once across the full corpus and records how often the final output changes. This is a sensitivity measure, not a causal claim about Sanskrit outside the implemented model.

## Results

| Measure | Result |
|---|---:|
| Evaluation cases | 16 |
| Exact matches | 16 |
| Failed cases | 0 |
| Exact-match accuracy | 1.000 |
| Registered rules | 11 |
| Rules observed in corpus | 11 |
| Rule coverage | 1.000 |

### Corpus Coverage

| Area | Representative inputs |
|---|---|
| Vowel transformations | `अइ`, `इअ`, `उअ`, `एअ`, `ओअ`, `अउ`, `आउ`, `ऋअ` |
| Pararūpa and vṛddhi environments | `अए`, `अऐ`, `अअ` |
| Palatalization | `तश` |
| Retroflexion | `तष` |
| Devoicing | `दक` |
| Anusvāra | `मक` |
| Visarga | `नमसत` |

### Counterfactual Sensitivity

The value is the fraction of the 16 corpus cases whose final output changed when the rule was disabled.

| Rule | Changed outputs | Sensitivity |
|---|---:|---:|
| P60177 | 3 | 18.8% |
| P60187 | 3 | 18.8% |
| P60178 | 2 | 12.5% |
| P601101 | 1 | 6.2% |
| P60188 | 1 | 6.2% |
| P60194 | 1 | 6.2% |
| P80315 | 1 | 6.2% |
| P8040 | 1 | 6.2% |
| P8041 | 1 | 6.2% |
| P80455 | 1 | 6.2% |
| P823 | 1 | 6.2% |

The highest measured sensitivity belongs to `P60177` and `P60187` in this corpus. This ranking is corpus-relative and should change as the evaluation set expands.

## Reproduction

Start the backend, then run:

```bash
cd backend
./venv/bin/python -m pytest -q
./venv/bin/python -c 'from app import main; import json; print(json.dumps(main.evaluation(), ensure_ascii=False, indent=2))'
```

The same evaluation is available while the API is running at:

```text
GET http://127.0.0.1:8000/evaluation
```

## Interpretation

The results demonstrate that the current executable subset is internally reproducible: every curated case has a deterministic expected output, every registered rule is exercised, and counterfactual interventions produce measurable differences. The graph and interaction views provide two complementary descriptions: declared relationships in the rule registry and relationships observed in actual derivations.

## Limitations

- Sixteen cases are not a statistically representative Sanskrit corpus.
- Several rules are marked `experimental_subset` and use simplified contexts.
- Character-level tokenization does not model morphology, word boundaries, accents, or grammatical domains fully.
- Exact-match accuracy here measures agreement with the curated project corpus, not external linguistic validity.
- Sensitivity is not proof of historical or theoretical rule dependency.
- The current report does not compare against an external Sanskrit grammar implementation.

## Next Research Steps

1. Expand the corpus with independently verified examples and negative cases.
2. Add word-boundary, morphological, and contextual features to the grammar state.
3. Compare outputs against a reference Sanskrit sandhi implementation.
4. Study rule-order permutations across a larger intervention matrix.
5. Publish the corpus, configuration, and generated result artifact alongside a literature review.

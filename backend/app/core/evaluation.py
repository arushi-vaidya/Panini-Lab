from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, List

from .derivation import DerivationEngine
from .models import Rule
from .sanskrit import tokenize_sanskrit


class EvaluationRunner:
    """Run the reproducible corpus used for the project's evaluation phase."""

    def __init__(self, rules: List[Rule], cases: Iterable[dict[str, Any]]):
        self.rules = rules
        self.cases = list(cases)

    @classmethod
    def from_json(cls, rules: List[Rule], path: str | Path) -> "EvaluationRunner":
        with Path(path).open("r", encoding="utf-8") as file:
            data = json.load(file)
        return cls(rules, data["cases"])

    def run(self) -> dict[str, Any]:
        engine = DerivationEngine(self.rules)
        results = []
        observed_rules: set[str] = set()
        rule_stats = {
            rule.rule_id: {
                "rule_id": rule.rule_id,
                "sutra": rule.sutra,
                "name": rule.name,
                "firings": 0,
                "passing_cases": 0,
            }
            for rule in self.rules
        }

        for case in self.cases:
            result = engine.derive(tokenize_sanskrit(case["input"]))
            passed = result.output == case["expected_output"]
            observed_rules.update(result.fired_rules)
            for rule_id in result.fired_rules:
                rule_stats[rule_id]["firings"] += 1
                if passed:
                    rule_stats[rule_id]["passing_cases"] += 1
            results.append({
                "id": case["id"],
                "input": case["input"],
                "expected_output": case["expected_output"],
                "actual_output": result.output,
                "passed": passed,
                "fired_rules": result.fired_rules,
                "steps": len(result.steps),
                "termination": result.terminated_reason,
            })

        sensitivity = []
        for rule in self.rules:
            changed_outputs = 0
            for case in self.cases:
                baseline = engine.derive(tokenize_sanskrit(case["input"]))
                counterfactual = engine.derive(
                    tokenize_sanskrit(case["input"]),
                    disabled_rules={rule.rule_id},
                )
                changed_outputs += int(baseline.output != counterfactual.output)
            sensitivity.append({
                "rule_id": rule.rule_id,
                "sutra": rule.sutra,
                "name": rule.name,
                "changed_outputs": changed_outputs,
                "sensitivity_rate": round(changed_outputs / len(self.cases), 3) if self.cases else 0,
            })

        sensitivity.sort(key=lambda row: (-row["sensitivity_rate"], row["rule_id"]))
        return {
            "corpus_name": "panini_sandhi_evaluation_v1",
            "total_cases": len(self.cases),
            "passed_cases": sum(int(result["passed"]) for result in results),
            "failed_cases": sum(int(not result["passed"]) for result in results),
            "exact_match_accuracy": round(
                sum(int(result["passed"]) for result in results) / len(results), 3
            ) if results else 0,
            "rule_count": len(self.rules),
            "rules_observed": len(observed_rules),
            "rule_coverage": round(len(observed_rules) / len(self.rules), 3) if self.rules else 0,
            "rule_statistics": list(rule_stats.values()),
            "counterfactual_sensitivity": sensitivity,
            "cases": results,
        }
from __future__ import annotations

from typing import Any, Iterable, List

from .experiment import CounterfactualExperiment
from .models import Rule


class RuleImpactAnalyzer:
    """Evaluate each rule's output impact over a deterministic input corpus."""

    def __init__(self, rules: List[Rule], inputs: Iterable[str]):
        self.rules = rules
        self.inputs = list(dict.fromkeys(inputs))
        self.experiment = CounterfactualExperiment(rules=rules)

    def analyze(self) -> dict[str, Any]:
        rows = []
        for rule in self.rules:
            changed_outputs = 0
            changed_steps = 0
            fired_baseline = 0
            fired_counterfactual = 0
            for input_surface in self.inputs:
                result = self.experiment.run(input_surface, disabled_rules=[rule.rule_id])
                changed_outputs += int(result.output_changed)
                changed_steps += result.impact_summary["changed_steps"]
                fired_baseline += int(rule.rule_id in result.impact_summary["baseline_fired_rules"])
                fired_counterfactual += int(rule.rule_id in result.impact_summary["counterfactual_fired_rules"])
            sample_count = len(self.inputs)
            rows.append({
                "rule_id": rule.rule_id,
                "sutra": rule.sutra,
                "name": rule.name,
                "sample_count": sample_count,
                "output_changes": changed_outputs,
                "output_change_rate": round(changed_outputs / sample_count, 3) if sample_count else 0,
                "average_changed_steps": round(changed_steps / sample_count, 3) if sample_count else 0,
                "baseline_firings": fired_baseline,
                "counterfactual_firings": fired_counterfactual,
            })
        rows.sort(key=lambda row: (-row["output_change_rate"], -row["average_changed_steps"], row["rule_id"]))
        for rank, row in enumerate(rows, start=1):
            row["impact_rank"] = rank
        return {"inputs": self.inputs, "sample_count": len(self.inputs), "rules": rows}
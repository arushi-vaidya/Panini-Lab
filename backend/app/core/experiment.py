from __future__ import annotations

from typing import List, Sequence

from .derivation import DerivationEngine
from .models import (
    ExperimentResult,
    Rule,
)
from .sanskrit import tokenize_sanskrit


class CounterfactualExperiment:

    def __init__(
        self,
        derivation_engine: DerivationEngine | None = None,
        rules: Sequence[Rule] | None = None,
    ):
        self.rules = list(rules or (derivation_engine.rules if derivation_engine else []))
        self.derivation_engine = derivation_engine or DerivationEngine(self.rules)

    def run(
        self,
        input_surface: str,
        rules: List[Rule] | None = None,
        disabled_rules: List[str] | None = None,
        rule_order: List[str] | None = None,
    ) -> ExperimentResult:
        active_rules = list(rules or self.rules or self.derivation_engine.rules)
        disabled = sorted(set(disabled_rules or []))

        if rule_order:
            by_id = {rule.rule_id: rule for rule in active_rules}
            if set(rule_order) != set(by_id):
                raise ValueError("rule_order must contain every active rule exactly once")
            active_rules = [by_id[rule_id] for rule_id in rule_order]

        def run(disabled_rules_for_run: set[str]):
            engine = DerivationEngine(active_rules)
            return engine.derive(
                initial_state=tokenize_sanskrit(input_surface),
                disabled_rules=disabled_rules_for_run,
            )

        baseline = run(set())
        counterfactual = run(set(disabled))

        changed_steps = []

        max_steps = max(len(baseline.steps), len(counterfactual.steps))

        for index in range(max_steps):

            baseline_record = (
                baseline.steps[index]
                if index < len(baseline.steps)
                else None
            )

            counter_record = (
                counterfactual.steps[index]
                if index < len(counterfactual.steps)
                else None
            )

            baseline_surface = (
                baseline_record.after_surface
                if baseline_record
                else None
            )

            counter_surface = (
                counter_record.after_surface
                if counter_record
                else None
            )

            if (
                baseline_surface != counter_surface
                or (baseline_record and counter_record and baseline_record.rule_id != counter_record.rule_id)
            ):

                changed_steps.append(
                    {
                        "step": index + 1,
                        "baseline_rule": (
                            baseline_record.rule_id
                            if baseline_record
                            else None
                        ),
                        "counterfactual_rule": (
                            counter_record.rule_id
                            if counter_record
                            else None
                        ),
                        "baseline_surface": baseline_surface,
                        "counterfactual_surface": counter_surface,
                    }
                )

        output_changed = (
            baseline.output
            != counterfactual.output
        )

        impact_summary = {
            "disabled_rule_count": len(disabled),
            "baseline_steps": len(baseline.steps),
            "counterfactual_steps": len(counterfactual.steps),
            "changed_steps": len(changed_steps),
            "baseline_output": baseline.output,
            "counterfactual_output": counterfactual.output,
            "baseline_fired_rules": baseline.fired_rules,
            "counterfactual_fired_rules": counterfactual.fired_rules,
            "removed_rules": sorted(set(baseline.fired_rules) - set(counterfactual.fired_rules)),
            "newly_fired_rules": sorted(set(counterfactual.fired_rules) - set(baseline.fired_rules)),
            "rule_order": [rule.rule_id for rule in active_rules],
        }

        return ExperimentResult(
            baseline=baseline,
            counterfactual=counterfactual,
            disabled_rules=disabled,
            output_changed=output_changed,
            baseline_output=baseline.output,
            counterfactual_output=counterfactual.output,
            changed_steps=changed_steps,
            impact_summary=impact_summary,
        )
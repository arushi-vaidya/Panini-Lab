from __future__ import annotations

from typing import List

from .derivation import DerivationEngine
from .models import (
    ExperimentResult,
    Rule,
)


class CounterfactualExperiment:

    def __init__(
        self,
        derivation_engine: DerivationEngine | None = None,
    ):
        self.derivation_engine = (
            derivation_engine
            if derivation_engine
            else DerivationEngine()
        )

    def run(
        self,
        input_surface: str,
        rules: List[Rule],
        disabled_rules: List[str],
    ) -> ExperimentResult:

        baseline = self.derivation_engine.derive(
            input_surface=input_surface,
            rules=rules,
            disabled_rules=[],
        )

        counterfactual = (
            self.derivation_engine.derive(
                input_surface=input_surface,
                rules=rules,
                disabled_rules=disabled_rules,
            )
        )

        changed_steps = []

        max_steps = max(
            len(baseline.records),
            len(counterfactual.records),
        )

        for index in range(max_steps):

            baseline_record = (
                baseline.records[index]
                if index < len(baseline.records)
                else None
            )

            counter_record = (
                counterfactual.records[index]
                if index < len(counterfactual.records)
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

            if baseline_surface != counter_surface:

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
            baseline.output_surface
            != counterfactual.output_surface
        )

        impact_summary = {
            "disabled_rule_count": len(
                disabled_rules
            ),
            "baseline_steps": len(
                baseline.records
            ),
            "counterfactual_steps": len(
                counterfactual.records
            ),
            "changed_steps": len(
                changed_steps
            ),
            "baseline_output": (
                baseline.output_surface
            ),
            "counterfactual_output": (
                counterfactual.output_surface
            ),
        }

        return ExperimentResult(
            baseline=baseline,
            counterfactual=counterfactual,
            disabled_rules=disabled_rules,
            output_changed=output_changed,
            baseline_output=baseline.output_surface,
            counterfactual_output=counterfactual.output_surface,
            changed_steps=changed_steps,
            impact_summary=impact_summary,
        )
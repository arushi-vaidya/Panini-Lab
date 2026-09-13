from __future__ import annotations

from .derivation import DerivationEngine

from .models import (
    ExperimentResult
)


class CounterfactualExperiment:

    def __init__(
        self,
        engine: DerivationEngine
    ):

        self.engine = engine

    # ========================================================
    # RUN EXPERIMENT
    # ========================================================

    def run(
        self,
        input_form: str,
        *,
        disabled_rules: list[str] | None = None,
        initial_features: dict | None = None,
    ) -> ExperimentResult:

        disabled_rules = (
            disabled_rules
            or []
        )

        # ----------------------------------------------------
        # ORIGINAL
        # ----------------------------------------------------

        self.engine.registry.reset_rules()

        original = self.engine.derive(
            input_form,
            initial_features=initial_features
        )

        # ----------------------------------------------------
        # COUNTERFACTUAL
        # ----------------------------------------------------

        self.engine.registry.reset_rules()

        for rule_id in disabled_rules:

            self.engine.registry.disable_rule(
                rule_id
            )

        counterfactual = (
            self.engine.derive(
                input_form,
                initial_features=initial_features
            )
        )

        # ----------------------------------------------------
        # COMPARE STEPS
        # ----------------------------------------------------

        changed_steps = []

        max_steps = max(
            len(original.steps),
            len(counterfactual.steps)
        )

        for index in range(
            max_steps
        ):

            original_form = (
                original.steps[index].after_form
                if index < len(original.steps)
                else None
            )

            counterfactual_form = (
                counterfactual.steps[index].after_form
                if index < len(counterfactual.steps)
                else None
            )

            if original_form != counterfactual_form:

                changed_steps.append(
                    index + 1
                )

        # ----------------------------------------------------
        # RESET
        # ----------------------------------------------------

        self.engine.registry.reset_rules()

        # ----------------------------------------------------
        # RETURN
        # ----------------------------------------------------

        return ExperimentResult(
            input_form=input_form,

            original_output=(
                original.output_form
            ),

            counterfactual_output=(
                counterfactual.output_form
            ),

            disabled_rules=disabled_rules,

            output_changed=(
                original.output_form
                != counterfactual.output_form
            ),

            original_steps=(
                original.steps
            ),

            counterfactual_steps=(
                counterfactual.steps
            ),

            changed_steps=changed_steps,
        )
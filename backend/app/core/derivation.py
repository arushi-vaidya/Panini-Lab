from __future__ import annotations

from typing import Optional

from .models import (
    DerivationRecord,
    DerivationResult,
    GrammarState,
)

from .registry import RuleRegistry

from .rule_engine import RuleEngine


class DerivationEngine:

    def __init__(
        self,
        registry: RuleRegistry
    ):

        self.registry = registry

        self.rule_engine = RuleEngine()

    # ========================================================
    # DERIVE
    # ========================================================

    def derive(
        self,
        input_form: str,
        *,
        initial_features: Optional[dict] = None,
    ) -> DerivationResult:

        # ----------------------------------------------------
        # INITIAL STATE
        # ----------------------------------------------------

        initial_state = GrammarState(
            form=input_form,
            features=(
                initial_features
                or {}
            )
        )

        current_state = (
            initial_state.snapshot()
        )

        steps = []

        rules_applied = []

        rules_skipped = []

        # ----------------------------------------------------
        # RULE ORDER
        # ----------------------------------------------------

        ordered_rules = sorted(
            self.registry.get_all_rules(),
            key=lambda rule: (
                -rule.priority,
                rule.id
            )
        )

        # ----------------------------------------------------
        # APPLY RULES
        # ----------------------------------------------------

        for (
            step_number,
            rule
        ) in enumerate(
            ordered_rules,
            start=1
        ):

            before_state = (
                current_state.snapshot()
            )

            # ================================================
            # DISABLED RULE
            # ================================================

            if not rule.enabled:

                rules_skipped.append(
                    rule.id
                )

                record = DerivationRecord(
                    step_number=step_number,
                    rule_id=rule.id,
                    sutra=rule.sutra,
                    before_form=(
                        before_state.form
                    ),
                    after_form=(
                        before_state.form
                    ),
                    changed=False,
                    explanation=(
                        "Rule is disabled."
                    ),
                    before_features=(
                        before_state.features
                    ),
                    after_features=(
                        before_state.features
                    ),
                )

                steps.append(record)

                continue

            # ================================================
            # APPLY
            # ================================================

            (
                after_state,
                changed,
                explanation
            ) = self.rule_engine.apply(
                before_state,
                rule
            )

            # ================================================
            # RECORD APPLICATION
            # ================================================

            if changed:

                after_state.applied_rules.append(
                    rule.id
                )

                rules_applied.append(
                    rule.id
                )

            # ================================================
            # RECORD STEP
            # ================================================

            record = DerivationRecord(
                step_number=step_number,
                rule_id=rule.id,
                sutra=rule.sutra,
                before_form=(
                    before_state.form
                ),
                after_form=(
                    after_state.form
                ),
                changed=changed,
                explanation=explanation,
                before_features=(
                    before_state.features
                ),
                after_features=(
                    after_state.features
                ),
            )

            after_state.history.append(
                record
            )

            current_state = after_state

            steps.append(record)

        # ----------------------------------------------------
        # FINAL RESULT
        # ----------------------------------------------------

        return DerivationResult(
            input_form=input_form,

            output_form=current_state.form,

            initial_state=initial_state,

            final_state=current_state,

            steps=steps,

            rules_applied=rules_applied,

            rules_skipped=rules_skipped,

            success=True,
        )
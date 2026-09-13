from typing import List

from .models import (
    DerivationResult,
    DerivationStep
)

from .rule_engine import RuleEngine
from .registry import RuleRegistry


class DerivationEngine:

    def __init__(self, registry: RuleRegistry):

        self.registry = registry
        self.rule_engine = RuleEngine()

    def derive(self, input_form: str) -> DerivationResult:

        current_form = input_form

        steps: List[DerivationStep] = []

        rules_applied = []
        rules_skipped = []

        step_number = 1

        rules = sorted(
            self.registry.get_all_rules(),
            key=lambda rule: rule.priority,
            reverse=True
        )

        for rule in rules:

            before = current_form

            if not rule.enabled:

                rules_skipped.append(rule.id)

                steps.append(
                    DerivationStep(
                        step_number=step_number,
                        rule_id=rule.id,
                        sutra=rule.sutra,
                        before=before,
                        after=before,
                        changed=False,
                        explanation="Rule disabled."
                    )
                )

                step_number += 1
                continue

            after, changed = self.rule_engine.apply_rule(
                current_form,
                rule
            )

            if changed:

                current_form = after

                rules_applied.append(rule.id)

                explanation = (
                    f"Applied {rule.sutra}: "
                    f"{before} → {after}"
                )

            else:

                explanation = (
                    f"Rule {rule.sutra} "
                    f"did not match the current state."
                )

            steps.append(
                DerivationStep(
                    step_number=step_number,
                    rule_id=rule.id,
                    sutra=rule.sutra,
                    before=before,
                    after=after,
                    changed=changed,
                    explanation=explanation
                )
            )

            step_number += 1

        return DerivationResult(
            input_form=input_form,
            output_form=current_form,
            steps=steps,
            rules_applied=rules_applied,
            rules_skipped=rules_skipped,
            success=True
        )
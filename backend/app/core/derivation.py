from __future__ import annotations

from typing import List, Optional

from .models import (
    DerivationRecord,
    DerivationResult,
    GrammarState,
    Rule,
    StateToken,
)
from .rule_engine import RuleEngine


class DerivationEngine:

    def __init__(
        self,
        rule_engine: Optional[RuleEngine] = None,
        max_steps: int = 100,
    ):
        self.rule_engine = (
            rule_engine
            if rule_engine
            else RuleEngine()
        )

        self.max_steps = max_steps

    def create_initial_state(
        self,
        input_surface: str,
    ) -> GrammarState:

        tokens = []

        for index, char in enumerate(input_surface):

            tokens.append(
                StateToken(
                    token_id=f"t{index + 1}",
                    surface=char,
                    source="input",
                    position=index,
                )
            )

        return GrammarState(
            tokens=tokens,
            features={
                "input": input_surface
            },
            history_id="initial",
        )

    def derive(
        self,
        input_surface: str,
        rules: List[Rule],
        disabled_rules: Optional[List[str]] = None,
    ) -> DerivationResult:

        disabled_rules = disabled_rules or []

        state = self.create_initial_state(
            input_surface
        )

        active_rules = [
            rule
            for rule in rules
            if rule.enabled
            and rule.rule_id not in disabled_rules
        ]

        active_rules.sort(
            key=lambda rule: (
                -rule.priority,
                rule.rule_id,
            )
        )

        state.active_rules = [
            rule.rule_id
            for rule in active_rules
        ]

        records: List[DerivationRecord] = []

        applied_rules: List[str] = []

        # Rules that have already fired once.
        fired_once = set()

        halted = False
        halt_reason = None

        for _ in range(self.max_steps):

            changed_this_round = False

            for rule in active_rules:

                # -------------------------------------------------
                # IMPORTANT:
                # Non-repeatable rules are allowed to fire only once
                # during a single derivation.
                # -------------------------------------------------

                if (
                    not rule.repeatable
                    and rule.rule_id in fired_once
                ):
                    continue

                before_state = state.snapshot()

                new_state, changed, explanation = (
                    self.rule_engine.apply(
                        rule,
                        state,
                    )
                )

                if not changed:
                    continue

                after_state = new_state.snapshot()

                records.append(
                    DerivationRecord(
                        step=len(records) + 1,
                        rule_id=rule.rule_id,
                        sutra=rule.sutra,
                        rule_name=rule.name,
                        before_surface=(
                            before_state["surface"]
                        ),
                        after_surface=(
                            after_state["surface"]
                        ),
                        before_state=before_state,
                        after_state=after_state,
                        changed=True,
                        explanation=explanation,
                    )
                )

                state = new_state

                applied_rules.append(
                    rule.rule_id
                )

                changed_this_round = True

                if not rule.repeatable:
                    fired_once.add(
                        rule.rule_id
                    )

            if not changed_this_round:
                break

        else:

            halted = True

            halt_reason = (
                "Maximum derivation steps exceeded."
            )

        return DerivationResult(
            input_surface=input_surface,
            output_surface=state.surface,
            final_state=state,
            records=records,
            halted=halted,
            halt_reason=halt_reason,
            applied_rules=applied_rules,
            metadata={
                "rule_count": len(active_rules),
                "disabled_rules": disabled_rules,
                "steps": len(records),
                "max_steps": self.max_steps,
            },
        )
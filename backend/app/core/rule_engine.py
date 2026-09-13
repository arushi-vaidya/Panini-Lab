from __future__ import annotations

from typing import Tuple

from .models import (
    ConditionType,
    GrammarState,
    OperationType,
    Rule,
)


class RuleEngine:
    """
    Executes structured computational rules.
    """

    # ========================================================
    # CONDITION EVALUATION
    # ========================================================

    def conditions_match(
        self,
        state: GrammarState,
        rule: Rule
    ) -> bool:

        for condition in rule.conditions:

            # ----------------------------------------------
            # PATTERN CONDITION
            # ----------------------------------------------

            if condition.type == ConditionType.PATTERN:

                if condition.pattern not in state.form:

                    return False

            # ----------------------------------------------
            # FEATURE CONDITION
            # ----------------------------------------------

            elif condition.type == ConditionType.FEATURE:

                for (
                    key,
                    expected_value
                ) in condition.features.items():

                    actual_value = (
                        state.features.get(key)
                    )

                    if actual_value != expected_value:

                        return False

            # ----------------------------------------------
            # CONTEXT / CUSTOM
            # ----------------------------------------------

            elif condition.type in (
                ConditionType.CONTEXT,
                ConditionType.CUSTOM,
            ):

                # These are intentionally not silently
                # evaluated in Phase 1A.
                #
                # A later formal evaluator will implement
                # their semantics.

                return False

        return True

    # ========================================================
    # APPLY RULE
    # ========================================================

    def apply(
        self,
        state: GrammarState,
        rule: Rule
    ) -> Tuple[
        GrammarState,
        bool,
        str
    ]:

        # ----------------------------------------------------
        # RULE DISABLED
        # ----------------------------------------------------

        if not rule.enabled:

            return (
                state.snapshot(),
                False,
                "Rule is disabled."
            )

        # ----------------------------------------------------
        # CHECK CONDITIONS
        # ----------------------------------------------------

        if not self.conditions_match(
            state,
            rule
        ):

            return (
                state.snapshot(),
                False,
                "Rule conditions did not match."
            )

        new_state = state.snapshot()

        before_form = new_state.form

        operation = rule.operation

        # ====================================================
        # SUBSTITUTE
        # ====================================================

        if operation.type == OperationType.SUBSTITUTE:

            target = operation.target

            replacement = operation.replacement

            if target not in new_state.form:

                return (
                    state.snapshot(),
                    False,
                    "Rule target was not found."
                )

            new_state.form = (
                new_state.form.replace(
                    target,
                    replacement,
                    1
                )
            )

        # ====================================================
        # INSERT
        # ====================================================

        elif operation.type == OperationType.INSERT:

            replacement = (
                operation.replacement or ""
            )

            target = operation.target

            if target:

                index = new_state.form.find(
                    target
                )

                if index == -1:

                    return (
                        state.snapshot(),
                        False,
                        "Insertion anchor was not found."
                    )

                index += len(target)

                new_state.form = (
                    new_state.form[:index]
                    + replacement
                    + new_state.form[index:]
                )

            else:

                new_state.form += replacement

        # ====================================================
        # DELETE
        # ====================================================

        elif operation.type == OperationType.DELETE:

            target = operation.target

            if (
                not target
                or target not in new_state.form
            ):

                return (
                    state.snapshot(),
                    False,
                    "Deletion target was not found."
                )

            new_state.form = (
                new_state.form.replace(
                    target,
                    "",
                    1
                )
            )

        # ====================================================
        # FEATURE UPDATE
        # ====================================================

        elif operation.type == OperationType.FEATURE_UPDATE:

            new_state.features.update(
                operation.feature_updates
            )

        # ====================================================
        # CUSTOM
        # ====================================================

        elif operation.type == OperationType.CUSTOM:

            return (
                state.snapshot(),
                False,
                "Custom operations require "
                "a dedicated evaluator."
            )

        changed = (
            before_form != new_state.form
            or operation.type
            == OperationType.FEATURE_UPDATE
        )

        return (
            new_state,
            changed,
            f"Applied {rule.sutra} ({rule.name})."
        )
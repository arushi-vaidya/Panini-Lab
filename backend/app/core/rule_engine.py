from __future__ import annotations

import re
from typing import List, Tuple

from .models import (
    ConditionType,
    GrammarState,
    OperationType,
    Rule,
    RuleCondition,
    RuleOperation,
    StateToken,
)


class RuleEngine:

    def evaluate(
        self,
        rule: Rule,
        state: GrammarState,
    ) -> bool:

        if not rule.enabled:
            return False

        if not self._scope_matches(rule, state):
            return False

        for condition in rule.conditions:

            result = self.evaluate_condition(
                condition,
                state,
            )

            if condition.negate:
                result = not result

            if not result:
                return False

        return True

    def evaluate_condition(
        self,
        condition: RuleCondition,
        state: GrammarState,
    ) -> bool:

        active_tokens = state.get_active_tokens()

        if condition.condition_type == ConditionType.PATTERN:

            if not condition.pattern:
                return False

            return self._pattern_exists(
                active_tokens,
                condition.pattern,
            )

        if condition.condition_type == ConditionType.FEATURE:

            if not condition.feature_key:
                return False

            return any(
                token.has_feature(
                    condition.feature_key,
                    condition.feature_value,
                )
                for token in active_tokens
            )

        if condition.condition_type == ConditionType.MARKER:

            if not condition.marker:
                return False

            return any(
                condition.marker in token.markers
                for token in active_tokens
            )

        if condition.condition_type == ConditionType.CONTEXT:

            return self._context_matches(
                active_tokens,
                condition,
            )

        if condition.condition_type == ConditionType.CUSTOM:
            return False

        return False

    def apply(
        self,
        rule: Rule,
        state: GrammarState,
    ) -> Tuple[GrammarState, bool, str]:

        if not self.evaluate(rule, state):
            return state, False, "Conditions not satisfied."

        new_state = state.clone()

        changed = False
        explanations = []

        for operation in rule.operations:

            operation_changed, explanation = self.apply_operation(
                operation,
                new_state,
            )

            if operation_changed:
                changed = True
                explanations.append(explanation)

        if changed:
            new_state.step += 1
            new_state.history_id = (
                f"{state.history_id}->{rule.rule_id}"
            )

            new_state.refresh_positions()

        return (
            new_state,
            changed,
            " ".join(explanations),
        )

    def apply_operation(
        self,
        operation: RuleOperation,
        state: GrammarState,
    ) -> Tuple[bool, str]:

        if operation.operation_type == OperationType.SUBSTITUTE:

            return self._substitute(
                operation,
                state,
            )

        if operation.operation_type == OperationType.INSERT:

            return self._insert(
                operation,
                state,
            )

        if operation.operation_type == OperationType.DELETE:

            return self._delete(
                operation,
                state,
            )

        if operation.operation_type == OperationType.FEATURE_UPDATE:

            return self._feature_update(
                operation,
                state,
            )

        if operation.operation_type == OperationType.MARKER_ADD:

            return self._marker_add(
                operation,
                state,
            )

        if operation.operation_type == OperationType.MARKER_REMOVE:

            return self._marker_remove(
                operation,
                state,
            )

        return False, "Custom operation not implemented."

    def _scope_matches(
        self,
        rule: Rule,
        state: GrammarState,
    ) -> bool:

        scope = rule.scope

        if scope.required_features:

            for key, value in scope.required_features.items():

                if state.features.get(key) != value:
                    return False

        if scope.excluded_features:

            for key, value in scope.excluded_features.items():

                if state.features.get(key) == value:
                    return False

        if scope.categories:

            categories = {
                token.features.get("category")
                for token in state.get_active_tokens()
            }

            if not categories.intersection(scope.categories):
                return False

        return True

    def _pattern_exists(
        self,
        tokens: List[StateToken],
        pattern: str,
    ) -> bool:

        surface = "".join(
            token.surface
            for token in tokens
        )

        if pattern.startswith("regex:"):

            regex = pattern[len("regex:"):]

            return re.search(
                regex,
                surface,
            ) is not None

        return pattern in surface

    def _context_matches(
        self,
        tokens: List[StateToken],
        condition: RuleCondition,
    ) -> bool:

        surface = "".join(
            token.surface
            for token in tokens
        )

        if condition.pattern:

            matches = list(
                re.finditer(
                    condition.pattern,
                    surface,
                )
            )

            if not matches:
                return False

            for match in matches:

                left = surface[:match.start()]
                right = surface[match.end():]

                left_ok = True
                right_ok = True

                if condition.left_pattern:
                    left_ok = re.search(
                        condition.left_pattern + "$",
                        left,
                    ) is not None

                if condition.right_pattern:
                    right_ok = re.search(
                        "^" + condition.right_pattern,
                        right,
                    ) is not None

                if left_ok and right_ok:
                    return True

            return False

        return False

    def _substitute(
        self,
        operation: RuleOperation,
        state: GrammarState,
    ) -> Tuple[bool, str]:

        if (
            not operation.target_pattern
            or operation.replacement is None
        ):
            return False, "Invalid substitution operation."

        changed = False

        target = operation.target_pattern

        for token in state.tokens:

            if not token.active:
                continue

            if token.surface == target:

                old = token.surface

                token.surface = operation.replacement

                changed = True

                return (
                    True,
                    f"Substituted '{old}' with "
                    f"'{operation.replacement}'.",
                )

        surface = state.surface

        if target in surface:

            new_surface = surface.replace(
                target,
                operation.replacement,
                1,
            )

            self._replace_surface(
                state,
                new_surface,
            )

            changed = True

            return (
                True,
                f"Substituted pattern '{target}' "
                f"with '{operation.replacement}'.",
            )

        return False, "Target pattern not found."

    def _insert(
        self,
        operation: RuleOperation,
        state: GrammarState,
    ) -> Tuple[bool, str]:

        if operation.replacement is None:
            return False, "Invalid insertion operation."

        position = (
            operation.position
            if operation.position is not None
            else len(state.tokens)
        )

        new_token = StateToken(
            token_id=self._next_token_id(state),
            surface=operation.replacement,
            source="rule_insert",
            position=position,
        )

        state.tokens.insert(
            position,
            new_token,
        )

        state.refresh_positions()

        return (
            True,
            f"Inserted '{operation.replacement}' "
            f"at position {position}.",
        )

    def _delete(
        self,
        operation: RuleOperation,
        state: GrammarState,
    ) -> Tuple[bool, str]:

        if not operation.target_pattern:
            return False, "Invalid delete operation."

        for token in state.tokens:

            if (
                token.active
                and token.surface == operation.target_pattern
            ):

                token.active = False

                return (
                    True,
                    f"Deleted '{operation.target_pattern}'.",
                )

        return False, "Target token not found."

    def _feature_update(
        self,
        operation: RuleOperation,
        state: GrammarState,
    ) -> Tuple[bool, str]:

        if not operation.feature_key:
            return False, "Feature key missing."

        changed = False

        for token in state.get_active_tokens():

            if (
                operation.target_pattern
                and token.surface != operation.target_pattern
            ):
                continue

            old_value = token.features.get(
                operation.feature_key
            )

            if old_value != operation.feature_value:

                token.features[
                    operation.feature_key
                ] = operation.feature_value

                changed = True

        if changed:

            return (
                True,
                f"Updated feature "
                f"'{operation.feature_key}' "
                f"to '{operation.feature_value}'.",
            )

        return False, "Feature already has requested value."

    def _marker_add(
        self,
        operation: RuleOperation,
        state: GrammarState,
    ) -> Tuple[bool, str]:

        if not operation.marker:
            return False, "Marker missing."

        changed = False

        for token in state.get_active_tokens():

            if (
                operation.target_pattern
                and token.surface != operation.target_pattern
            ):
                continue

            if operation.marker not in token.markers:

                token.markers.append(
                    operation.marker
                )

                changed = True

        return (
            changed,
            (
                f"Added marker '{operation.marker}'."
                if changed
                else "Marker already exists."
            ),
        )

    def _marker_remove(
        self,
        operation: RuleOperation,
        state: GrammarState,
    ) -> Tuple[bool, str]:

        if not operation.marker:
            return False, "Marker missing."

        changed = False

        for token in state.get_active_tokens():

            if (
                operation.target_pattern
                and token.surface != operation.target_pattern
            ):
                continue

            if operation.marker in token.markers:

                token.markers.remove(
                    operation.marker
                )

                changed = True

        return (
            changed,
            (
                f"Removed marker '{operation.marker}'."
                if changed
                else "Marker not present."
            ),
        )

    def _replace_surface(
        self,
        state: GrammarState,
        new_surface: str,
    ) -> None:

        active_tokens = state.get_active_tokens()

        if not active_tokens:
            return

        active_tokens[0].surface = new_surface

        for token in active_tokens[1:]:
            token.active = False

        state.refresh_positions()

    def _next_token_id(
        self,
        state: GrammarState,
    ) -> str:

        existing = []

        for token in state.tokens:

            if token.token_id.startswith("t"):

                try:
                    existing.append(
                        int(token.token_id[1:])
                    )
                except ValueError:
                    pass

        next_id = max(existing, default=0) + 1

        return f"t{next_id}"
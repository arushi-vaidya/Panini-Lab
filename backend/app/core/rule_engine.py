from __future__ import annotations

from copy import deepcopy
from typing import Dict, List, Optional, Tuple

from .models import (
    ConditionType,
    GrammarState,
    OperationType,
    Rule,
    RuleCondition,
    RuleOperation,
)


VOWEL_CLASSES: Dict[str, str] = {
    "अ": "a_vowel",
    "आ": "a_vowel",

    "इ": "ik",
    "ई": "ik",
    "उ": "ik",
    "ऊ": "ik",
    "ऋ": "ik",
    "ॠ": "ik",
    "ऌ": "ik",

    "ए": "ec",
    "ओ": "ec",
    "ऐ": "ec",
    "औ": "ec",

    "अ": "aK",
    "आ": "aK",
    "इ": "aK",
    "ई": "aK",
    "उ": "aK",
    "ऊ": "aK",
    "ऋ": "aK",
    "ॠ": "aK",
    "ऌ": "aK",

    "ए": "ac",
    "ओ": "ac",
    "ऐ": "ac",
    "औ": "ac",

    "अ": "savarṇa_vowel",
    "आ": "savarṇa_vowel",
    "इ": "savarṇa_vowel",
    "ई": "savarṇa_vowel",
    "उ": "savarṇa_vowel",
    "ऊ": "savarṇa_vowel",
    "ऋ": "savarṇa_vowel",
    "ॠ": "savarṇa_vowel",
    "ऌ": "savarṇa_vowel",
    "ए": "savarṇa_vowel",
    "ओ": "savarṇa_vowel",
    "ऐ": "savarṇa_vowel",
    "औ": "savarṇa_vowel",
}


class RuleEngine:

    def __init__(self):
        self.last_match: Optional[Tuple[int, int]] = None

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def evaluate(
        self,
        rule: Rule,
        state: GrammarState,
    ) -> bool:

        if not rule.enabled:
            return False

        for condition in rule.conditions:
            if not self._evaluate_condition(condition, state):
                return False

        return True

    def apply(
        self,
        rule: Rule,
        state: GrammarState,
    ) -> GrammarState:

        new_state = deepcopy(state)

        for operation in rule.operations:
            new_state = self._apply_operation(
                operation,
                new_state,
            )

        new_state.step += 1

        return new_state

    # ---------------------------------------------------------
    # Conditions
    # ---------------------------------------------------------

    def _evaluate_condition(
        self,
        condition: RuleCondition,
        state: GrammarState,
    ) -> bool:

        if condition.condition_type == ConditionType.PATTERN:
            result = self._has_pattern(
                state,
                condition.pattern or "",
            )

        elif condition.condition_type == ConditionType.FEATURE:
            result = self._has_feature(
                state,
                condition.feature_key,
                condition.feature_value,
            )

        elif condition.condition_type == ConditionType.MARKER:
            result = self._has_marker(
                state,
                condition.marker,
            )

        elif condition.condition_type == ConditionType.CONTEXT_PAIR:
            result = self._has_context_pair(
                state,
                condition.left_class,
                condition.right_class,
            )

        else:
            result = False

        return not result if condition.negate else result

    def _has_pattern(
        self,
        state: GrammarState,
        pattern: str,
    ) -> bool:

        return pattern in state.surface

    def _has_feature(
        self,
        state: GrammarState,
        key: Optional[str],
        value,
    ) -> bool:

        if key is None:
            return False

        return any(
            token.active
            and token.features.get(key) == value
            for token in state.tokens
        )

    def _has_marker(
        self,
        state: GrammarState,
        marker: Optional[str],
    ) -> bool:

        if marker is None:
            return False

        return any(
            token.active
            and marker in token.markers
            for token in state.tokens
        )

    def _has_context_pair(
        self,
        state: GrammarState,
        left_class: Optional[str],
        right_class: Optional[str],
    ) -> bool:

        active_tokens = [
            token
            for token in state.tokens
            if token.active
        ]

        for i in range(len(active_tokens) - 1):

            left = active_tokens[i]
            right = active_tokens[i + 1]

            if (
                self._belongs_to_class(
                    left.surface,
                    left_class,
                )
                and
                self._belongs_to_class(
                    right.surface,
                    right_class,
                )
            ):
                return True

        return False

    # ---------------------------------------------------------
    # Class membership
    # ---------------------------------------------------------

    def _belongs_to_class(
        self,
        symbol: str,
        class_name: Optional[str],
    ) -> bool:

        if class_name is None:
            return False

        if class_name == "ik":
            return symbol in {
                "इ", "ई",
                "उ", "ऊ",
                "ऋ", "ॠ",
                "ऌ",
            }

        if class_name == "ec":
            return symbol in {
                "ए", "ओ", "ऐ", "औ"
            }

        if class_name == "ac":
            return symbol in {
                "अ", "आ",
                "इ", "ई",
                "उ", "ऊ",
                "ऋ", "ॠ",
                "ऌ",
                "ए", "ओ",
                "ऐ", "औ",
            }

        if class_name == "a_vowel":
            return symbol in {
                "अ",
                "आ",
            }

        if class_name == "aK":
            return symbol in {
                "अ", "आ",
                "इ", "ई",
                "उ", "ऊ",
                "ऋ", "ॠ",
                "ऌ",
            }

        if class_name == "savarṇa_vowel":
            return symbol in {
                "अ", "आ",
                "इ", "ई",
                "उ", "ऊ",
                "ऋ", "ॠ",
                "ऌ",
            }

        if class_name == "consonant":
            return symbol in {
                "क", "ख", "ग", "घ", "ङ", "च", "छ", "ज", "झ", "ञ",
                "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध", "न",
                "प", "फ", "ब", "भ", "म", "य", "र", "ल", "व", "श", "ष", "स", "ह",
            }

        if class_name == "ścu":
            return symbol in {"च", "छ", "ज", "झ", "ञ", "श"}

        if class_name == "ṣṭu":
            return symbol in {"ट", "ठ", "ड", "ढ", "ण", "ष"}

        if class_name == "khar":
            return symbol in {"क", "ख", "च", "छ", "ट", "ठ", "त", "थ", "प", "फ", "श", "ष", "स"}

        if class_name == "sibilant":
            return symbol in {"श", "ष", "स"}

        if class_name == "dental_stop":
            return symbol in {"त", "थ", "द", "ध", "न", "स"}

        if class_name == "voiced_stop":
            return symbol in {"ग", "घ", "ज", "झ", "ड", "ढ", "द", "ध", "ब", "भ"}

        if class_name == "m_sound":
            return symbol == "म"

        return False

    # ---------------------------------------------------------
    # Operations
    # ---------------------------------------------------------

    def _apply_operation(
        self,
        operation: RuleOperation,
        state: GrammarState,
    ) -> GrammarState:

        if operation.operation_type == OperationType.SUBSTITUTE:
            return self._substitute(
                state,
                operation.target_pattern or "",
                operation.replacement or "",
            )

        if operation.operation_type == OperationType.CONTEXTUAL_SUBSTITUTE:
            return self._contextual_substitute(
                state,
                operation.mapping,
                operation.metadata.get("right_class"),
            )

        if operation.operation_type == OperationType.CONTEXTUAL_PAIR_SUBSTITUTE:
            return self._contextual_pair_substitute(
                state,
                operation.mapping,
            )

        if operation.operation_type == OperationType.INSERT:
            return self._insert(
                state,
                operation.replacement or "",
                operation.position,
            )

        if operation.operation_type == OperationType.DELETE:
            return self._delete(
                state,
                operation.target_pattern or "",
            )

        if operation.operation_type == OperationType.FEATURE_UPDATE:
            return self._feature_update(
                state,
                operation.feature_key,
                operation.feature_value,
            )

        if operation.operation_type == OperationType.MARKER_ADD:
            return self._marker_add(
                state,
                operation.target_pattern,
                operation.marker,
            )

        if operation.operation_type == OperationType.MARKER_REMOVE:
            return self._marker_remove(
                state,
                operation.target_pattern,
                operation.marker,
            )

        raise ValueError(
            f"Unsupported operation: {operation.operation_type}"
        )

    # ---------------------------------------------------------
    # Contextual substitution
    # ---------------------------------------------------------

    def _contextual_substitute(
        self,
        state: GrammarState,
        mapping: Dict[str, str],
        right_class: Optional[str] = None,
    ) -> GrammarState:

        tokens = [
            token
            for token in state.tokens
            if token.active
        ]

        for i in range(len(tokens) - 1):

            left = tokens[i]
            right = tokens[i + 1]

            replacement = mapping.get(
                left.surface
            )

            if replacement is None:
                continue

            if right_class:
                if not self._belongs_to_class(right.surface, right_class):
                    continue
            elif not self._is_vowel(right.surface):
                continue

            left.surface = replacement

            return state

        return state

    def _contextual_pair_substitute(
        self,
        state: GrammarState,
        mapping: Dict[str, str],
    ) -> GrammarState:

        tokens = [
            token
            for token in state.tokens
            if token.active
        ]

        for i in range(len(tokens) - 1):

            left = tokens[i]
            right = tokens[i + 1]

            key = f"{left.surface}+{right.surface}"

            replacement = mapping.get(key)

            if replacement is None:
                continue

            left.surface = replacement
            right.active = False

            return state

        return state

    # ---------------------------------------------------------
    # Basic operations
    # ---------------------------------------------------------

    def _substitute(
        self,
        state: GrammarState,
        target: str,
        replacement: str,
    ) -> GrammarState:

        for token in state.tokens:

            if token.active and token.surface == target:
                token.surface = replacement
                return state

        return state

    def _insert(
        self,
        state: GrammarState,
        value: str,
        position: Optional[int],
    ) -> GrammarState:

        if position is None:
            position = len(state.tokens)

        from .models import StateToken

        token = StateToken(
            token_id=f"generated_{state.step}",
            surface=value,
            source="rule",
            position=position,
            active=True,
        )

        state.tokens.insert(
            position,
            token,
        )

        self._reindex(state)

        return state

    def _delete(
        self,
        state: GrammarState,
        target: str,
    ) -> GrammarState:

        for token in state.tokens:

            if token.active and token.surface == target:
                token.active = False
                return state

        return state

    def _feature_update(
        self,
        state: GrammarState,
        key: Optional[str],
        value,
    ) -> GrammarState:

        if key is None:
            return state

        for token in state.tokens:
            if token.active:
                token.features[key] = value

        return state

    def _marker_add(
        self,
        state: GrammarState,
        target: Optional[str],
        marker: Optional[str],
    ) -> GrammarState:

        if marker is None:
            return state

        for token in state.tokens:

            if (
                token.active
                and
                (
                    target is None
                    or token.surface == target
                )
            ):
                if marker not in token.markers:
                    token.markers.append(marker)

        return state

    def _marker_remove(
        self,
        state: GrammarState,
        target: Optional[str],
        marker: Optional[str],
    ) -> GrammarState:

        if marker is None:
            return state

        for token in state.tokens:

            if (
                token.active
                and
                (
                    target is None
                    or token.surface == target
                )
            ):
                if marker in token.markers:
                    token.markers.remove(marker)

        return state

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _is_vowel(
        self,
        symbol: str,
    ) -> bool:

        return symbol in {
            "अ", "आ",
            "इ", "ई",
            "उ", "ऊ",
            "ऋ", "ॠ",
            "ऌ",
            "ए", "ओ",
            "ऐ", "औ",
        }

    def _reindex(
        self,
        state: GrammarState,
    ) -> None:

        for index, token in enumerate(state.tokens):
            token.position = index
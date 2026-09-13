from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import copy


class OperationType(str, Enum):
    SUBSTITUTE = "substitute"
    INSERT = "insert"
    DELETE = "delete"
    FEATURE_UPDATE = "feature_update"
    MARKER_ADD = "marker_add"
    MARKER_REMOVE = "marker_remove"
    CUSTOM = "custom"


class ConditionType(str, Enum):
    PATTERN = "pattern"
    FEATURE = "feature"
    CONTEXT = "context"
    MARKER = "marker"
    CUSTOM = "custom"


class BlockingType(str, Enum):
    NONE = "none"
    BLOCKS = "blocks"
    BLOCKED_BY = "blocked_by"
    MUTUAL = "mutual"


@dataclass
class StateToken:
    """
    A token is the smallest computational unit in a derivational state.

    Example:
        token_id = t3
        surface = "अ"
        source = "धातु"
        features = {"category": "root"}
    """

    token_id: str
    surface: str

    source: Optional[str] = None

    features: Dict[str, Any] = field(default_factory=dict)

    markers: List[str] = field(default_factory=list)

    position: int = 0

    active: bool = True

    def clone(self) -> "StateToken":
        return copy.deepcopy(self)

    def has_feature(self, key: str, value: Any) -> bool:
        return self.features.get(key) == value

    def add_marker(self, marker: str) -> None:
        if marker not in self.markers:
            self.markers.append(marker)

    def remove_marker(self, marker: str) -> None:
        if marker in self.markers:
            self.markers.remove(marker)


@dataclass
class Morpheme:
    """
    Groups one or more StateTokens into a grammatical unit.
    """

    morpheme_id: str

    form: str

    category: Optional[str] = None

    features: Dict[str, Any] = field(default_factory=dict)

    token_ids: List[str] = field(default_factory=list)


@dataclass
class RuleCondition:
    condition_type: ConditionType

    pattern: Optional[str] = None

    feature_key: Optional[str] = None

    feature_value: Any = None

    left_pattern: Optional[str] = None

    right_pattern: Optional[str] = None

    marker: Optional[str] = None

    negate: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RuleOperation:
    operation_type: OperationType

    target_pattern: Optional[str] = None

    replacement: Optional[str] = None

    position: Optional[int] = None

    feature_key: Optional[str] = None

    feature_value: Any = None

    marker: Optional[str] = None

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RuleScope:
    """
    Describes where a rule is allowed to operate.
    """

    domains: List[str] = field(default_factory=list)

    categories: List[str] = field(default_factory=list)

    required_features: Dict[str, Any] = field(default_factory=dict)

    excluded_features: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Rule:
    rule_id: str

    sutra: str

    name: str

    conditions: List[RuleCondition]

    operations: List[RuleOperation]

    priority: int = 0

    scope: RuleScope = field(default_factory=RuleScope)

    dependencies: List[str] = field(default_factory=list)

    blocking_type: BlockingType = BlockingType.NONE

    blocks: List[str] = field(default_factory=list)

    blocked_by: List[str] = field(default_factory=list)

    enabled: bool = True

    # Whether this rule is allowed to fire repeatedly
    # during a single derivation.
    repeatable: bool = False

    status: str = "experimental"

    description: str = ""

    metadata: Dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.rule_id:
            raise ValueError("rule_id cannot be empty")

        if not self.sutra:
            raise ValueError(f"{self.rule_id}: sutra cannot be empty")

        if self.priority < 0:
            raise ValueError(f"{self.rule_id}: priority cannot be negative")

        if self.rule_id in self.dependencies:
            raise ValueError(
                f"{self.rule_id}: rule cannot depend on itself"
            )


@dataclass
class GrammarState:
    """
    Complete computational state of a derivation.

    tokens:
        Current sequence being transformed.

    features:
        Global grammar-state features.

    active_rules:
        Rules currently enabled.

    step:
        Derivation step number.
    """

    tokens: List[StateToken] = field(default_factory=list)

    features: Dict[str, Any] = field(default_factory=dict)

    active_rules: List[str] = field(default_factory=list)

    step: int = 0

    history_id: str = "initial"

    metadata: Dict[str, Any] = field(default_factory=dict)

    def clone(self) -> "GrammarState":
        return copy.deepcopy(self)

    @property
    def surface(self) -> str:
        return "".join(
            token.surface
            for token in self.tokens
            if token.active
        )

    def refresh_positions(self) -> None:
        position = 0

        for token in self.tokens:
            if token.active:
                token.position = position
                position += 1

    def get_active_tokens(self) -> List[StateToken]:
        return [
            token
            for token in self.tokens
            if token.active
        ]

    def get_token(self, token_id: str) -> Optional[StateToken]:
        for token in self.tokens:
            if token.token_id == token_id:
                return token

        return None

    def snapshot(self) -> Dict[str, Any]:
        self.refresh_positions()

        return {
            "step": self.step,
            "surface": self.surface,
            "tokens": [
                {
                    "token_id": token.token_id,
                    "surface": token.surface,
                    "source": token.source,
                    "features": copy.deepcopy(token.features),
                    "markers": list(token.markers),
                    "position": token.position,
                    "active": token.active,
                }
                for token in self.tokens
            ],
            "features": copy.deepcopy(self.features),
            "active_rules": list(self.active_rules),
            "history_id": self.history_id,
            "metadata": copy.deepcopy(self.metadata),
        }


@dataclass
class DerivationRecord:
    step: int

    rule_id: str

    sutra: str

    rule_name: str

    before_surface: str

    after_surface: str

    before_state: Dict[str, Any]

    after_state: Dict[str, Any]

    changed: bool

    explanation: str = ""

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DerivationResult:
    input_surface: str

    output_surface: str

    final_state: GrammarState

    records: List[DerivationRecord]

    halted: bool = False

    halt_reason: Optional[str] = None

    applied_rules: List[str] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExperimentResult:
    baseline: DerivationResult

    counterfactual: DerivationResult

    disabled_rules: List[str]

    output_changed: bool

    baseline_output: str

    counterfactual_output: str

    changed_steps: List[Dict[str, Any]]

    impact_summary: Dict[str, Any] = field(default_factory=dict)
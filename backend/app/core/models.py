from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ConditionType(str, Enum):
    PATTERN = "pattern"
    FEATURE = "feature"
    MARKER = "marker"
    CONTEXT_PAIR = "context_pair"


class OperationType(str, Enum):
    SUBSTITUTE = "substitute"
    CONTEXTUAL_SUBSTITUTE = "contextual_substitute"
    CONTEXTUAL_PAIR_SUBSTITUTE = "contextual_pair_substitute"
    INSERT = "insert"
    DELETE = "delete"
    FEATURE_UPDATE = "feature_update"
    MARKER_ADD = "marker_add"
    MARKER_REMOVE = "marker_remove"


class BlockingType(str, Enum):
    NONE = "none"
    OPTIONAL = "optional"
    MANDATORY = "mandatory"
    BLOCKED_BY = "blocked_by"
    BLOCKS = "blocks"


class RuleCondition(BaseModel):
    condition_type: ConditionType

    pattern: Optional[str] = None

    feature_key: Optional[str] = None
    feature_value: Optional[Any] = None

    marker: Optional[str] = None

    left_class: Optional[str] = None
    right_class: Optional[str] = None

    negate: bool = False

    metadata: Dict[str, Any] = Field(default_factory=dict)


class RuleOperation(BaseModel):
    operation_type: OperationType

    target_pattern: Optional[str] = None
    replacement: Optional[str] = None

    mapping: Dict[str, str] = Field(default_factory=dict)

    target: Optional[str] = None
    position: Optional[int] = None

    feature_key: Optional[str] = None
    feature_value: Optional[Any] = None

    marker: Optional[str] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)


class RuleScope(BaseModel):
    domains: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)

    required_features: Dict[str, Any] = Field(default_factory=dict)
    excluded_features: Dict[str, Any] = Field(default_factory=dict)


class Rule(BaseModel):
    rule_id: str

    # Numerical sutra identifier
    sutra: str

    # Sanskrit text of the sutra
    sutra_devanagari: Optional[str] = None

    name: str
    description: str = ""

    priority: int = 0

    status: str = "experimental"

    enabled: bool = True

    # Prevents accidental infinite reapplication for rules
    # that should fire only once in the current simplified engine.
    repeatable: bool = False

    conditions: List[RuleCondition] = Field(default_factory=list)

    operations: List[RuleOperation] = Field(default_factory=list)

    scope: RuleScope = Field(default_factory=RuleScope)

    dependencies: List[str] = Field(default_factory=list)

    blocking_type: BlockingType = BlockingType.NONE

    blocks: List[str] = Field(default_factory=list)

    blocked_by: List[str] = Field(default_factory=list)

    examples: List[Dict[str, Any]] = Field(default_factory=list)

    metadata: Dict[str, Any] = Field(default_factory=dict)


class StateToken(BaseModel):
    token_id: str

    surface: str

    source: str = "input"

    features: Dict[str, Any] = Field(default_factory=dict)

    markers: List[str] = Field(default_factory=list)

    position: int = 0

    active: bool = True


class GrammarState(BaseModel):
    tokens: List[StateToken] = Field(default_factory=list)

    features: Dict[str, Any] = Field(default_factory=dict)

    step: int = 0

    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def surface(self) -> str:
        return "".join(
            token.surface
            for token in self.tokens
            if token.active
        )


class ExperimentResult(BaseModel):
    baseline: Any
    counterfactual: Any
    disabled_rules: List[str] = Field(default_factory=list)
    output_changed: bool
    baseline_output: str
    counterfactual_output: str
    changed_steps: List[Dict[str, Any]] = Field(default_factory=list)
    impact_summary: Dict[str, Any] = Field(default_factory=dict)
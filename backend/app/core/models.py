from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ============================================================
# ENUMS
# ============================================================

class OperationType(str, Enum):
    SUBSTITUTE = "substitute"
    INSERT = "insert"
    DELETE = "delete"
    FEATURE_UPDATE = "feature_update"
    CUSTOM = "custom"


class ConditionType(str, Enum):
    PATTERN = "pattern"
    FEATURE = "feature"
    CONTEXT = "context"
    CUSTOM = "custom"


class BlockingType(str, Enum):
    NONE = "none"
    BLOCKS = "blocks"
    BLOCKED_BY = "blocked_by"
    MUTUAL = "mutual"


# ============================================================
# TOKEN
# ============================================================

class StateToken(BaseModel):
    """
    Represents a token/segment inside a grammatical state.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str

    surface: str

    underlying: Optional[str] = None

    token_type: str = "segment"

    features: Dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# MORPHEME
# ============================================================

class Morpheme(BaseModel):
    """
    Represents a morphological unit.
    """

    id: str

    form: str

    category: Optional[str] = None

    features: Dict[str, Any] = Field(
        default_factory=dict
    )

    token_ids: List[str] = Field(
        default_factory=list
    )


# ============================================================
# RULE CONDITION
# ============================================================

class RuleCondition(BaseModel):
    """
    Represents a condition under which a rule may apply.
    """

    type: ConditionType

    description: str = ""

    # Pattern-based condition
    pattern: Optional[str] = None

    # Feature-based condition
    features: Dict[str, Any] = Field(
        default_factory=dict
    )

    # Context information
    left_context: Optional[str] = None

    right_context: Optional[str] = None

    # Extensible parameters
    parameters: Dict[str, Any] = Field(
        default_factory=dict
    )

    @model_validator(mode="after")
    def validate_condition(self):

        if self.type == ConditionType.PATTERN:

            if not self.pattern:
                raise ValueError(
                    "Pattern conditions require 'pattern'."
                )

        if self.type == ConditionType.FEATURE:

            if not self.features:
                raise ValueError(
                    "Feature conditions require 'features'."
                )

        return self


# ============================================================
# RULE OPERATION
# ============================================================

class RuleOperation(BaseModel):
    """
    Represents the transformation performed by a rule.
    """

    type: OperationType

    target: Optional[str] = None

    replacement: Optional[str] = None

    feature_updates: Dict[str, Any] = Field(
        default_factory=dict
    )

    parameters: Dict[str, Any] = Field(
        default_factory=dict
    )

    @model_validator(mode="after")
    def validate_operation(self):

        if self.type == OperationType.SUBSTITUTE:

            if self.target is None:
                raise ValueError(
                    "SUBSTITUTE requires target."
                )

            if self.replacement is None:
                raise ValueError(
                    "SUBSTITUTE requires replacement."
                )

        if self.type == OperationType.INSERT:

            if self.replacement is None:
                raise ValueError(
                    "INSERT requires replacement."
                )

        if self.type == OperationType.DELETE:

            if self.target is None:
                raise ValueError(
                    "DELETE requires target."
                )

        if self.type == OperationType.FEATURE_UPDATE:

            if not self.feature_updates:

                raise ValueError(
                    "FEATURE_UPDATE requires feature_updates."
                )

        return self


# ============================================================
# RULE SCOPE
# ============================================================

class RuleScope(BaseModel):
    """
    Represents contextual scope associated with a rule.
    """

    adhikara: Optional[str] = None

    anuvritti: List[str] = Field(
        default_factory=list
    )

    domain: Optional[str] = None

    notes: str = ""


# ============================================================
# RULE
# ============================================================

class Rule(BaseModel):
    """
    Structured computational representation
    of a Pāṇinian grammatical rule.
    """

    model_config = ConfigDict(
        validate_assignment=True
    )

    id: str

    sutra: str

    name: str

    description: str = ""

    phenomenon: str = ""

    conditions: List[RuleCondition] = Field(
        default_factory=list
    )

    operation: RuleOperation

    scope: RuleScope = Field(
        default_factory=RuleScope
    )

    priority: int = 0

    dependencies: List[str] = Field(
        default_factory=list
    )

    blocking_type: BlockingType = (
        BlockingType.NONE
    )

    blocks: List[str] = Field(
        default_factory=list
    )

    blocked_by: List[str] = Field(
        default_factory=list
    )

    exceptions: List[str] = Field(
        default_factory=list
    )

    tags: List[str] = Field(
        default_factory=list
    )

    enabled: bool = True

    source_reference: Optional[str] = None

    validation_status: str = "unvalidated"

    @model_validator(mode="after")
    def validate_rule(self):

        if self.priority < 0:

            raise ValueError(
                "Rule priority cannot be negative."
            )

        if self.id in self.dependencies:

            raise ValueError(
                "A rule cannot depend on itself."
            )

        if (
            self.blocking_type
            == BlockingType.BLOCKS
            and not self.blocks
        ):

            raise ValueError(
                "A BLOCKS rule must specify blocked rules."
            )

        if (
            self.blocking_type
            == BlockingType.BLOCKED_BY
            and not self.blocked_by
        ):

            raise ValueError(
                "A BLOCKED_BY rule must specify blocking rules."
            )

        return self


# ============================================================
# DERIVATION RECORD
# ============================================================

class DerivationRecord(BaseModel):
    """
    One transition in a derivation.
    """

    step_number: int

    rule_id: str

    sutra: str

    before_form: str

    after_form: str

    changed: bool

    explanation: str = ""

    before_features: Dict[str, Any] = Field(
        default_factory=dict
    )

    after_features: Dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# GRAMMAR STATE
# ============================================================

class GrammarState(BaseModel):
    """
    Complete representation of the current grammatical state.
    """

    model_config = ConfigDict(
        validate_assignment=True
    )

    form: str

    tokens: List[StateToken] = Field(
        default_factory=list
    )

    morphemes: List[Morpheme] = Field(
        default_factory=list
    )

    features: Dict[str, Any] = Field(
        default_factory=dict
    )

    applied_rules: List[str] = Field(
        default_factory=list
    )

    history: List[DerivationRecord] = Field(
        default_factory=list
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict
    )

    def snapshot(self) -> "GrammarState":

        return self.model_copy(
            deep=True
        )


# ============================================================
# DERIVATION RESULT
# ============================================================

class DerivationResult(BaseModel):

    input_form: str

    output_form: str

    initial_state: GrammarState

    final_state: GrammarState

    steps: List[DerivationRecord] = Field(
        default_factory=list
    )

    rules_applied: List[str] = Field(
        default_factory=list
    )

    rules_skipped: List[str] = Field(
        default_factory=list
    )

    success: bool = True

    errors: List[str] = Field(
        default_factory=list
    )


# ============================================================
# EXPERIMENT RESULT
# ============================================================

class ExperimentResult(BaseModel):

    input_form: str

    original_output: str

    counterfactual_output: str

    disabled_rules: List[str]

    output_changed: bool

    original_steps: List[DerivationRecord]

    counterfactual_steps: List[DerivationRecord]

    changed_steps: List[int] = Field(
        default_factory=list
    )
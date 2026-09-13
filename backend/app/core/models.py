from typing import List, Optional
from pydantic import BaseModel, Field


class Rule(BaseModel):
    """
    Represents a computationally executable Pāṇinian rule.

    This is intentionally modular so that the rule representation
    can become more sophisticated as the project develops.
    """

    id: str
    sutra: str
    name: str

    description: str = ""

    phenomenon: str = ""

    priority: int = 0

    input_pattern: str
    replacement: str

    dependencies: List[str] = Field(default_factory=list)

    enabled: bool = True


class DerivationStep(BaseModel):
    """
    Represents one step in a grammatical derivation.
    """

    step_number: int

    rule_id: Optional[str] = None
    sutra: Optional[str] = None

    before: str
    after: str

    changed: bool

    explanation: str = ""


class DerivationResult(BaseModel):
    """
    Complete result of one derivation.
    """

    input_form: str
    output_form: str

    steps: List[DerivationStep]

    rules_applied: List[str]

    rules_skipped: List[str]

    success: bool

class ExperimentResult(BaseModel):

    input_form: str

    original_output: str
    counterfactual_output: str

    disabled_rules: List[str]

    output_changed: bool
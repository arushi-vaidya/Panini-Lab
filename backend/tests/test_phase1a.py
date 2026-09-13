from pathlib import Path

import pytest

from pydantic import ValidationError

from app.core.models import (
    ConditionType,
    OperationType,
    Rule,
    RuleCondition,
    RuleOperation,
    GrammarState,
)

from app.core.registry import RuleRegistry

from app.core.derivation import (
    DerivationEngine
)

from app.core.experiment import (
    CounterfactualExperiment
)


RULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "app"
    / "data"
    / "rules.json"
)


def create_engine():

    registry = RuleRegistry(
        RULE_PATH
    )

    engine = DerivationEngine(
        registry
    )

    return registry, engine


# ============================================================
# RULE SCHEMA
# ============================================================

def test_rule_schema():

    registry, _ = create_engine()

    rule = registry.get_rule(
        "R001"
    )

    assert rule.id == "R001"

    assert rule.sutra == "6.1.87"

    assert (
        rule.conditions[0].type
        == ConditionType.PATTERN
    )

    assert (
        rule.operation.type
        == OperationType.SUBSTITUTE
    )

    assert (
        rule.operation.target
        == "अइ"
    )

    assert (
        rule.operation.replacement
        == "ए"
    )


# ============================================================
# GRAMMAR STATE
# ============================================================

def test_grammar_state():

    state = GrammarState(
        form="अइ",
        features={
            "category": "noun"
        }
    )

    assert state.form == "अइ"

    assert (
        state.features["category"]
        == "noun"
    )

    snapshot = state.snapshot()

    assert snapshot.form == "अइ"

    assert snapshot is not state


# ============================================================
# DERIVATION
# ============================================================

def test_derivation():

    _, engine = create_engine()

    result = engine.derive(
        "अइ"
    )

    assert (
        result.output_form
        == "ए"
    )

    assert (
        "R001"
        in result.rules_applied
    )

    assert len(
        result.steps
    ) > 0


# ============================================================
# COUNTERFACTUAL
# ============================================================

def test_counterfactual():

    _, engine = create_engine()

    experiment = CounterfactualExperiment(
        engine
    )

    result = experiment.run(
        "अइ",
        disabled_rules=[
            "R001"
        ]
    )

    assert (
        result.original_output
        == "ए"
    )

    assert (
        result.counterfactual_output
        == "अइ"
    )

    assert (
        result.output_changed
        is True
    )

    assert (
        1 in result.changed_steps
    )


# ============================================================
# FEATURE CONDITION
# ============================================================

def test_feature_condition():

    registry, engine = create_engine()

    result = engine.derive(
        "क",
        initial_features={
            "category": "verb"
        }
    )

    assert (
        result.final_state.features[
            "tense"
        ]
        == "present"
    )

    assert (
        "R002"
        in result.rules_applied
    )


# ============================================================
# DISABLE RULE
# ============================================================

def test_disable_rule():

    registry, engine = create_engine()

    registry.disable_rule(
        "R001"
    )

    result = engine.derive(
        "अइ"
    )

    assert (
        result.output_form
        == "अइ"
    )

    assert (
        "R001"
        in result.rules_skipped
    )


# ============================================================
# RESET RULE
# ============================================================

def test_reset_rule():

    registry, engine = create_engine()

    registry.disable_rule(
        "R001"
    )

    registry.reset_rules()

    result = engine.derive(
        "अइ"
    )

    assert (
        result.output_form
        == "ए"
    )


# ============================================================
# INVALID CONDITION
# ============================================================

def test_invalid_pattern_condition():

    with pytest.raises(
        ValidationError
    ):

        RuleCondition(
            type=ConditionType.PATTERN
        )


# ============================================================
# INVALID OPERATION
# ============================================================

def test_invalid_substitution():

    with pytest.raises(
        ValidationError
    ):

        RuleOperation(
            type=OperationType.SUBSTITUTE,
            target="अइ"
        )


# ============================================================
# INVALID SELF DEPENDENCY
# ============================================================

def test_self_dependency():

    with pytest.raises(
        ValidationError
    ):

        Rule(
            id="R999",

            sutra="TEST",

            name="Invalid",

            dependencies=[
                "R999"
            ],

            operation=RuleOperation(
                type=OperationType.SUBSTITUTE,
                target="a",
                replacement="b"
            )
        )
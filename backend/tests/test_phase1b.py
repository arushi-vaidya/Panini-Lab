from pathlib import Path

from app.core.derivation import DerivationEngine
from app.core.experiment import CounterfactualExperiment
from app.core.models import (
    ConditionType,
    GrammarState,
    OperationType,
    Rule,
    RuleCondition,
    RuleOperation,
    StateToken,
)
from app.core.registry import RuleRegistry


def make_substitution_rule():

    return Rule(
        rule_id="TEST.SUB",
        sutra="TEST.1",
        name="Test substitution",
        priority=100,
        conditions=[
            RuleCondition(
                condition_type=ConditionType.PATTERN,
                pattern="अइ",
            )
        ],
        operations=[
            RuleOperation(
                operation_type=OperationType.SUBSTITUTE,
                target_pattern="अइ",
                replacement="ए",
            )
        ],
    )


def test_token_features():

    token = StateToken(
        token_id="t1",
        surface="ग",
        features={
            "category": "root"
        },
    )

    assert token.has_feature(
        "category",
        "root",
    )

    assert not token.has_feature(
        "category",
        "verb",
    )


def test_marker_operations():

    token = StateToken(
        token_id="t1",
        surface="ग",
    )

    token.add_marker("processed")

    assert "processed" in token.markers

    token.remove_marker("processed")

    assert "processed" not in token.markers


def test_grammar_state_surface():

    state = GrammarState(
        tokens=[
            StateToken(
                token_id="t1",
                surface="अ",
            ),
            StateToken(
                token_id="t2",
                surface="इ",
            ),
        ]
    )

    assert state.surface == "अइ"


def test_state_snapshot():

    state = GrammarState(
        tokens=[
            StateToken(
                token_id="t1",
                surface="ग",
                features={
                    "category": "root"
                },
            )
        ]
    )

    snapshot = state.snapshot()

    assert snapshot["surface"] == "ग"

    assert snapshot["tokens"][0]["features"][
        "category"
    ] == "root"


def test_substitution():

    engine = DerivationEngine()

    rule = make_substitution_rule()

    result = engine.derive(
        "अइ",
        [rule],
    )

    assert result.output_surface == "ए"

    assert len(result.records) == 1

    assert (
        result.records[0].before_surface
        == "अइ"
    )

    assert (
        result.records[0].after_surface
        == "ए"
    )


def test_insertion():

    rule = Rule(
        rule_id="TEST.INSERT",
        sutra="TEST.2",
        name="Insertion",
        priority=100,
        conditions=[
            RuleCondition(
                condition_type=ConditionType.PATTERN,
                pattern="ग",
            )
        ],
        operations=[
            RuleOperation(
                operation_type=OperationType.INSERT,
                replacement="अ",
                position=1,
            )
        ],
    )

    engine = DerivationEngine()

    result = engine.derive(
        "ग",
        [rule],
    )

    assert result.output_surface == "गअ"


def test_feature_update():

    rule = Rule(
        rule_id="TEST.FEATURE",
        sutra="TEST.3",
        name="Feature update",
        priority=100,
        conditions=[
            RuleCondition(
                condition_type=ConditionType.FEATURE,
                feature_key="category",
                feature_value="verb",
            )
        ],
        operations=[
            RuleOperation(
                operation_type=OperationType.FEATURE_UPDATE,
                feature_key="tense",
                feature_value="present",
            )
        ],
    )

    engine = DerivationEngine()

    state = GrammarState(
        tokens=[
            StateToken(
                token_id="t1",
                surface="ग",
                features={
                    "category": "verb"
                },
            )
        ]
    )

    new_state, changed, _ = (
        engine.rule_engine.apply(
            rule,
            state,
        )
    )

    assert changed

    assert (
        new_state.tokens[0].features[
            "tense"
        ]
        == "present"
    )


def test_delete():

    rule = Rule(
        rule_id="TEST.DELETE",
        sutra="TEST.4",
        name="Delete",
        priority=100,
        conditions=[
            RuleCondition(
                condition_type=ConditionType.PATTERN,
                pattern="X",
            )
        ],
        operations=[
            RuleOperation(
                operation_type=OperationType.DELETE,
                target_pattern="X",
            )
        ],
    )

    engine = DerivationEngine()

    result = engine.derive(
        "aXb",
        [rule],
    )

    assert result.output_surface == "ab"


def test_counterfactual():

    rule = make_substitution_rule()

    experiment = CounterfactualExperiment()

    result = experiment.run(
        input_surface="अइ",
        rules=[rule],
        disabled_rules=["TEST.SUB"],
    )

    assert result.baseline_output == "ए"

    assert (
        result.counterfactual_output
        == "अइ"
    )

    assert result.output_changed is True


def test_registry_loading():

    registry = RuleRegistry()

    path = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "data"
        / "rules.json"
    )

    registry.load_json(path)

    assert len(
        registry.all_rules()
    ) == 5

    assert registry.get(
        "R001"
    ).sutra == "6.1.87"


def test_disable_and_enable():

    registry = RuleRegistry()

    rule = make_substitution_rule()

    registry.register(rule)

    registry.disable(
        "TEST.SUB"
    )

    assert (
        registry.get(
            "TEST.SUB"
        ).enabled
        is False
    )

    registry.enable(
        "TEST.SUB"
    )

    assert (
        registry.get(
            "TEST.SUB"
        ).enabled
        is True
    )
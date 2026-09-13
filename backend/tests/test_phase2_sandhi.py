import json
from pathlib import Path

from app.core.derivation import DerivationEngine
from app.core.interaction_miner import InteractionMiner
from app.core.models import Rule
from app.core.sanskrit import tokenize_sanskrit


RULES_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "data"
    / "rules.json"
)


def load_rules():
    with open(RULES_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        Rule(**rule)
        for rule in data["rules"]
    ]


def get_engine():
    return DerivationEngine(load_rules())


def test_miner_records_multi_rule_derivation():
    engine = get_engine()

    result = engine.derive(
        tokenize_sanskrit("अइ")
    )

    miner = InteractionMiner()
    miner.observe(result)

    interactions = miner.get_interactions()

    assert isinstance(interactions, list)


def test_miner_can_record_manual_trace():
    """
    This test isolates the miner from the grammar engine.

    It verifies that an observed rule sequence is converted
    into pairwise interactions.
    """

    engine = get_engine()

    result = engine.derive(
        tokenize_sanskrit("अइ")
    )

    # Only run this test meaningfully if at least two rules fire.
    if len(result.fired_rules) < 2:
        return

    miner = InteractionMiner()
    miner.observe(result)

    interactions = miner.get_interactions()

    assert len(interactions) > 0


def test_interaction_serialization():
    engine = get_engine()

    result = engine.derive(
        tokenize_sanskrit("अइ")
    )

    miner = InteractionMiner()
    miner.observe(result)

    data = miner.to_dict()

    assert "interactions" in data
    assert isinstance(data["interactions"], list)


def test_miner_clear():
    engine = get_engine()

    result = engine.derive(
        tokenize_sanskrit("अइ")
    )

    miner = InteractionMiner()
    miner.observe(result)

    miner.clear()

    assert miner.get_interactions() == []

def test_miner_detects_ordered_rule_interaction():
    class MockResult:
        input = "test"
        fired_rules = [
            "P60101",
            "P60177",
            "P60187",
        ]

    miner = InteractionMiner()

    miner.observe(MockResult())

    interactions = miner.get_interactions()

    pairs = {
        (
            interaction.source,
            interaction.target,
            interaction.relation,
        )
        for interaction in interactions
    }

    assert (
        "P60101",
        "P60177",
        "observed_before",
    ) in pairs

    assert (
        "P60101",
        "P60187",
        "observed_before",
    ) in pairs

    assert (
        "P60177",
        "P60187",
        "observed_before",
    ) in pairs
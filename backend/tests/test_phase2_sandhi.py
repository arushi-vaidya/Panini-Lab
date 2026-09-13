import json
from pathlib import Path

from app.core.sanskrit import tokenize_sanskrit
from app.core.derivation import DerivationEngine
from app.core.models import Rule


RULES_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "data"
    / "rules.json"
)


def load_rules():

    with open(
        RULES_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    return [
        Rule(**rule)
        for rule in data["rules"]
    ]


def get_engine():

    return DerivationEngine(
        load_rules()
    )


def test_iko_yanaci():

    engine = get_engine()

    state = tokenize_sanskrit("इअ")

    result = engine.derive(state)

    assert result.output == "यअ"


def test_iko_yanaci_u():

    engine = get_engine()

    state = tokenize_sanskrit("उअ")

    result = engine.derive(state)

    assert result.output == "वअ"


def test_iko_yanaci_r():

    engine = get_engine()

    state = tokenize_sanskrit("ऋअ")

    result = engine.derive(state)

    assert result.output == "रअ"


def test_eco_yavayavah():

    engine = get_engine()

    state = tokenize_sanskrit("एअ")

    result = engine.derive(state)

    assert result.output == "अयअ"


def test_eco_yavayavah_o():

    engine = get_engine()

    state = tokenize_sanskrit("ओअ")

    result = engine.derive(state)

    assert result.output == "अवअ"


def test_guna_i():

    engine = get_engine()

    state = tokenize_sanskrit("अइ")

    result = engine.derive(state)

    assert result.output == "ए"


def test_guna_u():

    engine = get_engine()

    state = tokenize_sanskrit("अउ")

    result = engine.derive(state)

    assert result.output == "ओ"


def test_vrddhi_e():

    engine = get_engine()

    state = tokenize_sanskrit("अए")

    result = engine.derive(state)

    assert result.output == "ऐ"


def test_vrddhi_o():

    engine = get_engine()

    state = tokenize_sanskrit("अओ")

    result = engine.derive(state)

    assert result.output == "औ"


def test_savarna_dirgha_a():

    engine = get_engine()

    state = tokenize_sanskrit("अअ")

    result = engine.derive(state)

    assert result.output == "आ"


def test_savarna_dirgha_i():

    engine = get_engine()

    state = tokenize_sanskrit("इइ")

    result = engine.derive(state)

    assert result.output == "ई"


def test_savarna_dirgha_u():

    engine = get_engine()

    state = tokenize_sanskrit("उउ")

    result = engine.derive(state)

    assert result.output == "ऊ"


def test_savarna_dirgha_overrides_yan():

    engine = get_engine()

    state = tokenize_sanskrit("इइ")

    result = engine.derive(state)

    assert result.output == "ई"


def test_rule_metadata():

    rules = load_rules()

    assert len(rules) == 5

    assert all(
        rule.status == "validated_subset"
        for rule in rules
    )

    assert {
        rule.sutra
        for rule in rules
    } == {
        "6.1.77",
        "6.1.78",
        "6.1.87",
        "6.1.88",
        "6.1.101",
    }
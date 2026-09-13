from pathlib import Path

from app.core.registry import RuleRegistry
from app.core.derivation import DerivationEngine


RULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "app"
    / "data"
    / "rules.json"
)


def create_engine():

    registry = RuleRegistry(str(RULE_PATH))

    return registry, DerivationEngine(registry)


def test_rule_application():

    registry, engine = create_engine()

    result = engine.derive("अइ")

    assert result.output_form == "ए"

    assert "R001" in result.rules_applied


def test_rule_removal():

    registry, engine = create_engine()

    registry.disable_rule("R001")

    result = engine.derive("अइ")

    assert result.output_form == "अइ"

    assert "R001" in result.rules_skipped
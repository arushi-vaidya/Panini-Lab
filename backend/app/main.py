from pathlib import Path

from app.core.registry import RuleRegistry
from app.core.derivation import DerivationEngine


RULE_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "rules.json"
)


def print_derivation(result):

    print("\n==============================")
    print("       PĀṆINI-LAB")
    print("==============================")

    print(f"\nInput : {result.input_form}")
    print(f"Output: {result.output_form}")

    print("\nDerivation:")
    print("------------------------------")

    for step in result.steps:

        print(
            f"{step.step_number}. "
            f"[{step.rule_id}] "
            f"{step.before} → {step.after}"
        )

        print(
            f"   {step.explanation}"
        )

    print("\nRules Applied:")
    print(result.rules_applied)

    print("\nRules Skipped:")
    print(result.rules_skipped)

    print("==============================\n")


def main():

    registry = RuleRegistry(str(RULE_PATH))

    engine = DerivationEngine(registry)

    print("\n===== ORIGINAL =====")

    original = engine.derive("अइ")

    print_derivation(original)

    print("\n===== COUNTERFACTUAL =====")

    registry.disable_rule("R001")

    counterfactual = engine.derive("अइ")

    print_derivation(counterfactual)


if __name__ == "__main__":
    main()
from pathlib import Path

from app.core.registry import RuleRegistry
from app.core.derivation import DerivationEngine
from app.core.experiment import CounterfactualExperiment


RULE_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "rules.json"
)


def print_derivation(result):

    print("\n================================")
    print("         PĀṆINI-LAB")
    print("================================")

    print(
        f"\nInput  : {result.input_form}"
    )

    print(
        f"Output : {result.output_form}"
    )

    print("\nDerivation")
    print("--------------------------------")

    for step in result.steps:

        print(
            f"{step.step_number:02d}. "
            f"[{step.rule_id}] "
            f"{step.before_form} "
            f"→ "
            f"{step.after_form}"
        )

        print(
            f"    {step.explanation}"
        )

    print("\nApplied rules:")

    print(
        result.rules_applied
    )

    print("\nSkipped rules:")

    print(
        result.rules_skipped
    )


def main():

    registry = RuleRegistry(
        RULE_PATH
    )

    engine = DerivationEngine(
        registry
    )

    experiment = CounterfactualExperiment(
        engine
    )

    # ========================================================
    # ORIGINAL
    # ========================================================

    print("\n\n========== ORIGINAL ==========")

    original = engine.derive(
        "अइ"
    )

    print_derivation(
        original
    )

    # ========================================================
    # COUNTERFACTUAL
    # ========================================================

    print("\n\n====== COUNTERFACTUAL ======")

    result = experiment.run(
        "अइ",
        disabled_rules=[
            "R001"
        ]
    )

    print(
        f"\nInput: {result.input_form}"
    )

    print(
        f"Original output: "
        f"{result.original_output}"
    )

    print(
        f"Counterfactual output: "
        f"{result.counterfactual_output}"
    )

    print(
        f"\nOutput changed: "
        f"{result.output_changed}"
    )

    print(
        f"Changed steps: "
        f"{result.changed_steps}"
    )


if __name__ == "__main__":
    main()
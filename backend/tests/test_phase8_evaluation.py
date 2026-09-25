from app import main
from app.core.evaluation import EvaluationRunner


def test_evaluation_corpus_is_exact_and_covers_all_rules():
    result = main.evaluation()

    assert result["corpus_name"] == "panini_sandhi_evaluation_v1"
    assert result["total_cases"] == 16
    assert result["passed_cases"] == 16
    assert result["exact_match_accuracy"] == 1.0
    assert result["rule_count"] == 11
    assert result["rules_observed"] == 11
    assert result["rule_coverage"] == 1.0


def test_evaluation_exposes_counterfactual_sensitivity():
    result = main.evaluation()

    assert len(result["counterfactual_sensitivity"]) == 11
    assert all("sensitivity_rate" in row for row in result["counterfactual_sensitivity"])


def test_evaluation_runner_accepts_custom_cases():
    runner = EvaluationRunner(
        main.registry.all_rules(),
        [{"id": "custom", "input": "अइ", "expected_output": "ए"}],
    )

    result = runner.run()

    assert result["passed_cases"] == 1
    assert result["failed_cases"] == 0
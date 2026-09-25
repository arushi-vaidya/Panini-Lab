from app import main
from app.core.experiment import CounterfactualExperiment
from app.core.impact import RuleImpactAnalyzer
from app.core.sanskrit import tokenize_sanskrit


def test_counterfactual_reports_rule_and_trace_impact():
    result = main.experiment(
        main.ExperimentRequest(
            input_surface="अइ",
            disabled_rules=["P60187"],
        )
    )

    assert result["baseline_output"] == "ए"
    assert result["counterfactual_output"] == "अइ"
    assert result["impact_summary"]["removed_rules"] == ["P60187"]
    assert result["baseline_trace"]
    assert result["counterfactual_trace"] == []


def test_counterfactual_accepts_custom_rule_order():
    order = list(reversed(main.derivation_engine.get_rule_order()))
    result = CounterfactualExperiment(rules=main.registry.all_rules()).run(
        "अइ",
        rule_order=order,
    )

    assert result.impact_summary["rule_order"] == order


def test_impact_analysis_ranks_every_rule():
    result = RuleImpactAnalyzer(
        main.registry.all_rules(),
        ["अइ", "इअ"],
    ).analyze()

    assert result["sample_count"] == 2
    assert len(result["rules"]) == 11
    assert [row["impact_rank"] for row in result["rules"]] == list(range(1, 12))


def test_graph_preserves_relation_edges():
    result = main.graph()

    assert len(result["nodes"]) == 11
    assert {edge["relation"] for edge in result["edges"]} >= {"depends_on", "blocks"}


def test_expanded_consonant_rules_are_executable():
    expected = {
        "अए": ("ए", "P60194"),
        "तश": ("चश", "P8040"),
        "तष": ("टष", "P8041"),
        "दक": ("तक", "P80455"),
        "मक": ("ंक", "P823"),
    }

    for input_surface, (output, rule_id) in expected.items():
        result = main.derive(main.DerivationRequest(input_surface=input_surface))
        assert result["output"] == output
        assert rule_id in result["applied_rules"]
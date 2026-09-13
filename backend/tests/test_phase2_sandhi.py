import json
from pathlib import Path

from app.core.models import Rule
from app.core.dependency_graph import DependencyGraph


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


def test_graph_contains_all_rules():
    rules = load_rules()

    graph = DependencyGraph(rules)

    assert len(graph.get_nodes()) == 5


def test_graph_contains_expected_rule_ids():
    rules = load_rules()

    graph = DependencyGraph(rules)

    assert set(graph.get_nodes()) == {
        "P60177",
        "P60178",
        "P60187",
        "P60188",
        "P601101",
    }


def test_dependency_edges_exist():
    rules = load_rules()

    graph = DependencyGraph(rules)

    edges = graph.get_edges()

    assert len(edges) > 0


def test_graph_serialization():
    rules = load_rules()

    graph = DependencyGraph(rules)

    data = graph.to_dict()

    assert "nodes" in data
    assert "edges" in data

    assert len(data["nodes"]) == 5


def test_blocking_relationships():
    rules = load_rules()

    graph = DependencyGraph(rules)

    # 6.1.101 should block 6.1.77
    blocking_rules = graph.get_blocking_rules("P60177")

    assert "P601101" in blocking_rules


def test_graph_cycle_detection():
    rules = load_rules()

    graph = DependencyGraph(rules)

    assert isinstance(graph.has_cycle(), bool)
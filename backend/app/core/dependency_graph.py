from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

import networkx as nx

from .models import Rule


@dataclass
class DependencyEdge:
    source: str
    target: str
    relation: str
    metadata: Dict[str, Any]


class DependencyGraph:
    """
    Builds a directed dependency graph from the relationships
    encoded in the Pāṇinian rule registry.

    Nodes:
        Rules

    Edges:
        depends_on
        blocks
        blocked_by
    """

    def __init__(self, rules: List[Rule]):
        self.rules = rules
        self.graph = nx.MultiDiGraph()

        self._add_rule_nodes()
        self._add_dependency_edges()
        self._add_blocking_edges()

    def _add_rule_nodes(self) -> None:
        for rule in self.rules:
            self.graph.add_node(
                rule.rule_id,
                sutra=rule.sutra,
                sutra_devanagari=rule.sutra_devanagari,
                name=rule.name,
                status=rule.status,
                priority=rule.priority,
                enabled=rule.enabled,
            )

    def _add_dependency_edges(self) -> None:
        for rule in self.rules:
            for dependency in rule.dependencies:
                if dependency not in self.graph:
                    continue

                self.graph.add_edge(
                    rule.rule_id,
                    dependency,
                    relation="depends_on",
                )

    def _add_blocking_edges(self) -> None:
        for rule in self.rules:

            for blocked_rule in rule.blocks:
                if blocked_rule not in self.graph:
                    continue

                self.graph.add_edge(
                    rule.rule_id,
                    blocked_rule,
                    relation="blocks",
                )

            for blocking_rule in rule.blocked_by:
                if blocking_rule not in self.graph:
                    continue

                self.graph.add_edge(
                    blocking_rule,
                    rule.rule_id,
                    relation="blocks",
                )

    def get_nodes(self) -> List[str]:
        return list(self.graph.nodes)

    def get_edges(self) -> List[DependencyEdge]:
        edges = []

        for source, target, data in self.graph.edges(data=True):
            edges.append(
                DependencyEdge(
                    source=source,
                    target=target,
                    relation=data.get("relation", "unknown"),
                    metadata={
                        key: value
                        for key, value in data.items()
                        if key != "relation"
                    },
                )
            )

        return edges

    def get_dependencies(self, rule_id: str) -> List[str]:
        """
        Return rules that the given rule explicitly depends on.
        """
        return [
            target
            for _, target, data in self.graph.out_edges(
                rule_id,
                data=True,
            )
            if data.get("relation") == "depends_on"
        ]

    def get_blocked_rules(self, rule_id: str) -> List[str]:
        """
        Return rules blocked by the given rule.
        """
        return [
            target
            for _, target, data in self.graph.out_edges(
                rule_id,
                data=True,
            )
            if data.get("relation") == "blocks"
        ]

    def get_blocking_rules(self, rule_id: str) -> List[str]:
        """
        Return rules that block the given rule.
        """
        return [
            source
            for source, _, data in self.graph.in_edges(
                rule_id,
                data=True,
            )
            if data.get("relation") == "blocks"
        ]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nodes": [
                {
                    "id": node_id,
                    **attributes,
                }
                for node_id, attributes
                in self.graph.nodes(data=True)
            ],
            "edges": [
                {
                    "source": source,
                    "target": target,
                    **data,
                }
                for source, target, data
                in self.graph.edges(data=True)
            ],
        }

    def has_cycle(self) -> bool:
        """
        Check whether the current dependency graph contains
        a directed cycle.
        """
        return not nx.is_directed_acyclic_graph(self.graph)

    def topological_order(self) -> List[str]:
        """
        Return a topological ordering when possible.

        Raises NetworkXUnfeasible if the graph contains
        a directed cycle.
        """
        return list(nx.topological_sort(self.graph))
    @classmethod
    def from_interactions(
        cls,
        rules: List[Rule],
        interactions: Iterable[Any],
    ) -> "DependencyGraph":
        """
        Build a dependency graph using empirically observed
        rule interactions.

        Only interaction types that represent execution ordering
        are converted into directed graph edges.
        """

        graph = cls(rules)

        for interaction in interactions:
            relation = interaction.relation

            if relation not in {
                "observed_before",
                "blocks",
            }:
                continue

            source = interaction.source
            target = interaction.target

            if source not in graph.graph:
                continue

            if target not in graph.graph:
                continue

            graph.graph.add_edge(
                source,
                target,
                relation=relation,
                count=interaction.count,
                examples=list(interaction.examples),
                source_type="empirical",
            )

        return graph
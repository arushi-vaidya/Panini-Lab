from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Tuple

from .derivation import DerivationResult


@dataclass
class RuleInteraction:
    source: str
    target: str
    relation: str
    count: int
    examples: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "relation": self.relation,
            "count": self.count,
            "examples": list(self.examples),
        }


class InteractionMiner:
    """
    Mines empirical rule interactions from derivation traces.

    This module does NOT claim that every observed ordering is a
    formal Paninian dependency.

    Instead, it records relationships observed in the executed
    derivations.
    """

    def __init__(self) -> None:
        self._interactions: Dict[
            Tuple[str, str, str],
            Dict[str, Any],
        ] = {}

    def observe(
        self,
        result: DerivationResult,
        input_surface: str | None = None,
    ) -> None:
        """
        Analyze one derivation result and record rule interactions.
        """

        fired_rules = result.fired_rules

        if len(fired_rules) < 2:
            return

        example = (
            input_surface
            if input_surface is not None
            else result.input
        )

        # Record pairwise execution ordering.
        for index, source in enumerate(fired_rules):
            for target in fired_rules[index + 1:]:
                self._record(
                    source=source,
                    target=target,
                    relation="observed_before",
                    example=example,
                )

        # Record rules that participated in the same derivation.
        for index, source in enumerate(fired_rules):
            for target in fired_rules[index + 1:]:
                self._record(
                    source=source,
                    target=target,
                    relation="co_fired",
                    example=example,
                )

    def _record(
        self,
        source: str,
        target: str,
        relation: str,
        example: str,
    ) -> None:
        key = (source, target, relation)

        if key not in self._interactions:
            self._interactions[key] = {
                "count": 0,
                "examples": [],
            }

        entry = self._interactions[key]

        entry["count"] += 1

        if example not in entry["examples"]:
            entry["examples"].append(example)

    def get_interactions(self) -> List[RuleInteraction]:
        interactions = []

        for (source, target, relation), data in self._interactions.items():
            interactions.append(
                RuleInteraction(
                    source=source,
                    target=target,
                    relation=relation,
                    count=data["count"],
                    examples=data["examples"],
                )
            )

        return sorted(
            interactions,
            key=lambda item: (
                item.source,
                item.target,
                item.relation,
            ),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "interactions": [
                interaction.to_dict()
                for interaction in self.get_interactions()
            ]
        }

    def clear(self) -> None:
        self._interactions.clear()
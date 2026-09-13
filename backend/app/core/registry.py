from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .models import Rule


class RuleRegistry:

    def __init__(
        self,
        rules_path: str | Path
    ):

        self.rules_path = Path(
            rules_path
        )

        self.rules: Dict[str, Rule] = {}

        self.load_rules()

    # ========================================================
    # LOAD
    # ========================================================

    def load_rules(self):

        with self.rules_path.open(
            "r",
            encoding="utf-8"
        ) as file:

            raw_rules = json.load(file)

        loaded_rules = [
            Rule(**data)
            for data in raw_rules
        ]

        ids = [
            rule.id
            for rule in loaded_rules
        ]

        if len(ids) != len(set(ids)):

            raise ValueError(
                "Rule IDs must be unique."
            )

        self.rules = {
            rule.id: rule
            for rule in loaded_rules
        }

        self.validate_dependencies()

    # ========================================================
    # DEPENDENCY VALIDATION
    # ========================================================

    def validate_dependencies(self):

        rule_ids = set(
            self.rules.keys()
        )

        for rule in self.rules.values():

            for dependency in rule.dependencies:

                if dependency not in rule_ids:

                    raise ValueError(
                        f"Rule {rule.id} depends on "
                        f"unknown rule {dependency}."
                    )

            for blocked_rule in rule.blocks:

                if blocked_rule not in rule_ids:

                    raise ValueError(
                        f"Rule {rule.id} blocks "
                        f"unknown rule {blocked_rule}."
                    )

            for blocker in rule.blocked_by:

                if blocker not in rule_ids:

                    raise ValueError(
                        f"Rule {rule.id} is blocked by "
                        f"unknown rule {blocker}."
                    )

    # ========================================================
    # GET RULE
    # ========================================================

    def get_rule(
        self,
        rule_id: str
    ) -> Rule:

        if rule_id not in self.rules:

            raise ValueError(
                f"Rule {rule_id} not found."
            )

        return self.rules[rule_id]

    # ========================================================
    # GET ALL
    # ========================================================

    def get_all_rules(self) -> List[Rule]:

        return list(
            self.rules.values()
        )

    # ========================================================
    # ENABLE
    # ========================================================

    def enable_rule(
        self,
        rule_id: str
    ):

        self.get_rule(
            rule_id
        ).enabled = True

    # ========================================================
    # DISABLE
    # ========================================================

    def disable_rule(
        self,
        rule_id: str
    ):

        self.get_rule(
            rule_id
        ).enabled = False

    # ========================================================
    # RESET
    # ========================================================

    def reset_rules(self):

        for rule in self.rules.values():

            rule.enabled = True

    # ========================================================
    # ENABLED RULES
    # ========================================================

    def enabled_rules(self):

        return [
            rule
            for rule in self.rules.values()
            if rule.enabled
        ]
import json
from pathlib import Path
from typing import Dict

from .models import Rule


class RuleRegistry:
    """
    Loads and manages the computational rule set.
    """

    def __init__(self, rules_path: str):
        self.rules_path = Path(rules_path)
        self.rules: Dict[str, Rule] = {}

        self.load_rules()

    def load_rules(self):
        """
        Load rules from JSON.
        """

        with open(self.rules_path, "r", encoding="utf-8") as file:
            raw_rules = json.load(file)

        self.rules = {
            rule_data["id"]: Rule(**rule_data)
            for rule_data in raw_rules
        }

    def get_rule(self, rule_id: str) -> Rule:
        """
        Retrieve a rule by ID.
        """

        if rule_id not in self.rules:
            raise ValueError(f"Rule {rule_id} not found.")

        return self.rules[rule_id]

    def get_all_rules(self):
        """
        Return all registered rules.
        """

        return list(self.rules.values())

    def enable_rule(self, rule_id: str):
        self.get_rule(rule_id).enabled = True

    def disable_rule(self, rule_id: str):
        self.get_rule(rule_id).enabled = False

    def reset_rules(self):
        """
        Enable all rules.
        """

        for rule in self.rules.values():
            rule.enabled = True
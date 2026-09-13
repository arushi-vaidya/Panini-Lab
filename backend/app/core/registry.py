from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from .models import (
    BlockingType,
    ConditionType,
    OperationType,
    Rule,
    RuleCondition,
    RuleOperation,
    RuleScope,
)


class RuleRegistry:

    def __init__(self):
        self.rules: Dict[str, Rule] = {}

    def register(
        self,
        rule: Rule,
    ) -> None:

        rule.validate()

        if rule.rule_id in self.rules:
            raise ValueError(
                f"Duplicate rule ID: {rule.rule_id}"
            )

        self.rules[rule.rule_id] = rule

    def get(
        self,
        rule_id: str,
    ) -> Rule:

        if rule_id not in self.rules:
            raise KeyError(
                f"Unknown rule: {rule_id}"
            )

        return self.rules[rule_id]

    def all_rules(self) -> List[Rule]:

        return list(
            self.rules.values()
        )

    def enabled_rules(self) -> List[Rule]:

        return [
            rule
            for rule in self.rules.values()
            if rule.enabled
        ]

    def disable(
        self,
        rule_id: str,
    ) -> None:

        self.get(rule_id).enabled = False

    def enable(
        self,
        rule_id: str,
    ) -> None:

        self.get(rule_id).enabled = True

    def reset(self) -> None:

        for rule in self.rules.values():
            rule.enabled = True

    def validate_dependencies(self) -> None:

        known = set(
            self.rules.keys()
        )

        for rule in self.rules.values():

            for dependency in rule.dependencies:

                if dependency not in known:
                    raise ValueError(
                        f"{rule.rule_id} depends on "
                        f"unknown rule {dependency}"
                    )

            for blocked in rule.blocks:

                if blocked not in known:
                    raise ValueError(
                        f"{rule.rule_id} blocks "
                        f"unknown rule {blocked}"
                    )

            for blocker in rule.blocked_by:

                if blocker not in known:
                    raise ValueError(
                        f"{rule.rule_id} is blocked by "
                        f"unknown rule {blocker}"
                    )

    def load_json(
        self,
        path: str | Path,
    ) -> None:

        path = Path(path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        for raw_rule in data.get(
            "rules",
            [],
        ):

            conditions = []

            for raw_condition in raw_rule.get(
                "conditions",
                [],
            ):

                conditions.append(
                    RuleCondition(
                        condition_type=ConditionType(
                            raw_condition[
                                "condition_type"
                            ]
                        ),
                        pattern=raw_condition.get(
                            "pattern"
                        ),
                        feature_key=raw_condition.get(
                            "feature_key"
                        ),
                        feature_value=raw_condition.get(
                            "feature_value"
                        ),
                        left_pattern=raw_condition.get(
                            "left_pattern"
                        ),
                        right_pattern=raw_condition.get(
                            "right_pattern"
                        ),
                        marker=raw_condition.get(
                            "marker"
                        ),
                        negate=raw_condition.get(
                            "negate",
                            False,
                        ),
                        metadata=raw_condition.get(
                            "metadata",
                            {},
                        ),
                    )
                )

            operations = []

            for raw_operation in raw_rule.get(
                "operations",
                [],
            ):

                operations.append(
                    RuleOperation(
                        operation_type=OperationType(
                            raw_operation[
                                "operation_type"
                            ]
                        ),
                        target_pattern=raw_operation.get(
                            "target_pattern"
                        ),
                        replacement=raw_operation.get(
                            "replacement"
                        ),
                        position=raw_operation.get(
                            "position"
                        ),
                        feature_key=raw_operation.get(
                            "feature_key"
                        ),
                        feature_value=raw_operation.get(
                            "feature_value"
                        ),
                        marker=raw_operation.get(
                            "marker"
                        ),
                        metadata=raw_operation.get(
                            "metadata",
                            {},
                        ),
                    )
                )

            raw_scope = raw_rule.get(
                "scope",
                {},
            )

            scope = RuleScope(
                domains=raw_scope.get(
                    "domains",
                    [],
                ),
                categories=raw_scope.get(
                    "categories",
                    [],
                ),
                required_features=raw_scope.get(
                    "required_features",
                    {},
                ),
                excluded_features=raw_scope.get(
                    "excluded_features",
                    {},
                ),
            )

            rule = Rule(
                rule_id=raw_rule["rule_id"],
                sutra=raw_rule["sutra"],
                name=raw_rule["name"],
                conditions=conditions,
                operations=operations,
                priority=raw_rule.get(
                    "priority",
                    0,
                ),
                scope=scope,
                dependencies=raw_rule.get(
                    "dependencies",
                    [],
                ),
                blocking_type=BlockingType(
                    raw_rule.get(
                        "blocking_type",
                        "none",
                    )
                ),
                blocks=raw_rule.get(
                    "blocks",
                    [],
                ),
                blocked_by=raw_rule.get(
                    "blocked_by",
                    [],
                ),
                enabled=raw_rule.get(
                    "enabled",
                    True,
                ),

                repeatable=raw_rule.get(
                    "repeatable",
                    False,
                ),

                status=raw_rule.get(
                    "status",
                    "experimental",
                ),
                description=raw_rule.get(
                    "description",
                    "",
                ),
                metadata=raw_rule.get(
                    "metadata",
                    {},
                ),
            )

            self.register(rule)

        self.validate_dependencies()
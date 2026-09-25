from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Set

from .models import GrammarState, Rule
from .rule_engine import RuleEngine


@dataclass
class DerivationStep:
    """
    Represents one successful rule application during a derivation.
    """

    step: int
    rule_id: str
    sutra: str
    rule_name: str

    before_surface: str
    after_surface: str

    before_state: Dict[str, Any]
    after_state: Dict[str, Any]

    changed: bool
    explanation: str

    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the derivation step into a JSON-serializable dictionary.
        """
        return asdict(self)


@dataclass
class DerivationResult:
    initial_state: GrammarState
    final_state: GrammarState
    steps: List[DerivationStep]
    skipped_rules: List[str]
    disabled_rules: List[str]
    fired_rules: List[str]
    terminated_reason: str

    @property
    def output(self) -> str:
        """Final surface form produced by the derivation."""
        return self.final_state.surface

    @property
    def input(self) -> str:
        """Initial surface form supplied to the derivation."""
        return self.initial_state.surface

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input": self.input,
            "output": self.output,
            "initial_state": self.initial_state.model_dump(),
            "final_state": self.final_state.model_dump(),
            "steps": [step.to_dict() for step in self.steps],
            "skipped_rules": self.skipped_rules,
            "disabled_rules": self.disabled_rules,
            "fired_rules": self.fired_rules,
            "terminated_reason": self.terminated_reason,
        }

class DerivationEngine:
    """
    Executes a collection of grammar rules over a GrammarState.

    The engine is intentionally deterministic.

    Rule ordering:
        1. Higher priority first
        2. Rule ID ascending for deterministic tie-breaking

    A rule may be:
        - disabled
        - explicitly disabled for an experiment
        - non-repeatable
        - repeatable

    Every successful transformation creates a DerivationStep.
    """

    def __init__(
        self,
        rules: List[Rule],
        rule_engine: Optional[RuleEngine] = None,
    ):

        self.rules = sorted(
            rules,
            key=lambda rule: (
                -rule.priority,
                rule.rule_id,
            ),
        )

        self.rule_engine = (
            rule_engine
            if rule_engine is not None
            else RuleEngine()
        )

    # =========================================================
    # PUBLIC API
    # =========================================================

    def derive(
        self,
        initial_state: GrammarState,
        disabled_rules: Optional[Set[str]] = None,
        max_steps: int = 100,
    ) -> DerivationResult:
        """
        Execute the grammar starting from initial_state.

        Parameters
        ----------
        initial_state:
            Starting GrammarState.

        disabled_rules:
            Rule IDs that should be disabled for this derivation.
            Useful for counterfactual experiments.

        max_steps:
            Safety limit preventing accidental infinite derivations.

        Returns
        -------
        DerivationResult
        """

        disabled_rules = (
            set(disabled_rules)
            if disabled_rules is not None
            else set()
        )

        # Never mutate the caller's state.
        state = deepcopy(initial_state)

        steps: List[DerivationStep] = []

        skipped_rules: List[str] = []

        fired_rules: List[str] = []

        # Tracks rules that have already fired.
        fired_once: Set[str] = set()

        terminated_reason = "no_applicable_rules"

        while True:

            # -------------------------------------------------
            # Safety termination
            # -------------------------------------------------

            if len(steps) >= max_steps:

                terminated_reason = (
                    "max_steps_reached"
                )

                break

            applied_rule = False

            # -------------------------------------------------
            # Evaluate rules in deterministic order
            # -------------------------------------------------

            for rule in self.rules:

                # =============================================
                # Rule disabled in registry
                # =============================================

                if not rule.enabled:

                    skipped_rules.append(
                        rule.rule_id
                    )

                    continue

                # =============================================
                # Rule disabled by experiment
                # =============================================

                if rule.rule_id in disabled_rules:

                    skipped_rules.append(
                        rule.rule_id
                    )

                    continue

                # =============================================
                # Non-repeatable rule
                # =============================================

                if (
                    not rule.repeatable
                    and rule.rule_id in fired_once
                ):

                    continue

                # =============================================
                # Check rule conditions
                # =============================================

                applicable = self.rule_engine.evaluate(
                    rule,
                    state,
                )

                if not applicable:
                    continue

                # =============================================
                # Snapshot BEFORE state
                # =============================================

                before = deepcopy(state)

                # =============================================
                # Apply rule
                # =============================================

                after = self.rule_engine.apply(
                    rule,
                    state,
                )

                # =============================================
                # Determine whether state changed
                # =============================================

                changed = self._state_changed(
                    before,
                    after,
                )

                # A rule that technically evaluated as true
                # but did not modify the state should not create
                # a derivation step.
                if not changed:

                    continue

                # =============================================
                # Commit new state
                # =============================================

                state = after

                # =============================================
                # Record rule execution
                # =============================================

                fired_once.add(
                    rule.rule_id
                )

                if rule.rule_id not in fired_rules:

                    fired_rules.append(
                        rule.rule_id
                    )

                step_number = len(steps) + 1

                step = self._create_step(
                    step_number,
                    rule,
                    before,
                    after,
                )

                steps.append(step)

                applied_rule = True

                # -------------------------------------------------
                # Important:
                #
                # Restart rule evaluation from the highest-priority
                # rule after every successful transformation.
                #
                # This allows newly-created states to activate
                # higher-priority rules.
                # -------------------------------------------------

                break

            # -------------------------------------------------
            # No rule fired during this pass
            # -------------------------------------------------

            if not applied_rule:

                terminated_reason = (
                    "no_applicable_rules"
                )

                break

        return DerivationResult(
            initial_state=initial_state,
            final_state=state,
            steps=steps,
            skipped_rules=skipped_rules,
            disabled_rules=sorted(
                disabled_rules
            ),
            fired_rules=fired_rules,
            terminated_reason=terminated_reason,
        )

    # =========================================================
    # STATE COMPARISON
    # =========================================================

    @staticmethod
    def _state_changed(
        before: GrammarState,
        after: GrammarState,
    ) -> bool:
        """
        Determine whether a rule actually changed the
        computational grammar state.

        We compare the serialized state rather than only the
        surface string because a rule may change:

            - features
            - markers
            - token activity
            - token identity
            - positions

        without necessarily changing the visible surface.
        """

        before_snapshot = before.model_dump()
        after_snapshot = after.model_dump()
        before_snapshot.pop("step", None)
        after_snapshot.pop("step", None)
        return before_snapshot != after_snapshot

    # =========================================================
    # DERIVATION STEP CREATION
    # =========================================================

    @staticmethod
    def _create_step(
        step_number: int,
        rule: Rule,
        before: GrammarState,
        after: GrammarState,
    ) -> DerivationStep:
        """
        Construct a complete derivation trace entry.
        """

        before_surface = before.surface
        after_surface = after.surface

        explanation = (
            f"{rule.sutra} ({rule.name}): "
            f"{before_surface} → {after_surface}"
        )

        return DerivationStep(
            step=step_number,

            rule_id=rule.rule_id,

            sutra=rule.sutra,

            rule_name=rule.name,

            before_surface=before_surface,

            after_surface=after_surface,

            before_state=before.model_dump(),

            after_state=after.model_dump(),

            changed=(
                before_surface
                != after_surface
            ),

            explanation=explanation,

            metadata={
                "priority": rule.priority,
                "status": rule.status,
                "repeatable": rule.repeatable,
                "dependencies": list(
                    rule.dependencies
                ),
                "blocking_type": (
                    rule.blocking_type
                ),
                "blocks": list(
                    rule.blocks
                ),
                "blocked_by": list(
                    rule.blocked_by
                ),
                "rule_metadata": dict(
                    rule.metadata
                ),
            },
        )

    # =========================================================
    # CONVENIENCE METHODS
    # =========================================================

    def get_rule(
        self,
        rule_id: str,
    ) -> Optional[Rule]:
        """
        Retrieve a rule by rule ID.
        """

        for rule in self.rules:

            if rule.rule_id == rule_id:
                return rule

        return None

    def get_rule_order(self) -> List[str]:
        """
        Return the deterministic execution order.
        """

        return [
            rule.rule_id
            for rule in self.rules
        ]

    def get_enabled_rules(self) -> List[Rule]:
        """
        Return currently enabled rules.
        """

        return [
            rule
            for rule in self.rules
            if rule.enabled
        ]

    def get_disabled_rules(self) -> List[Rule]:
        """
        Return rules disabled in the registry.
        """

        return [
            rule
            for rule in self.rules
            if not rule.enabled
        ]
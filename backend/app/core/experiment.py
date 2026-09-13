from .derivation import DerivationEngine
from .models import DerivationResult


class CounterfactualExperiment:

    def __init__(self, engine: DerivationEngine):

        self.engine = engine

    def run(
        self,
        input_form: str,
        disabled_rules=None
    ):

        if disabled_rules is None:
            disabled_rules = []

        # Original derivation
        self.engine.registry.reset_rules()

        original = self.engine.derive(
            input_form
        )

        # Counterfactual derivation
        self.engine.registry.reset_rules()

        for rule_id in disabled_rules:
            self.engine.registry.disable_rule(
                rule_id
            )

        counterfactual = self.engine.derive(
            input_form
        )

        # Reset system after experiment
        self.engine.registry.reset_rules()

        return original, counterfactual
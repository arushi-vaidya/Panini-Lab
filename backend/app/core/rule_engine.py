from typing import Tuple

from .models import Rule


class RuleEngine:
    """
    Executes individual computational grammar rules.
    """

    def apply_rule(
        self,
        form: str,
        rule: Rule
    ) -> Tuple[str, bool]:

        if not rule.enabled:
            return form, False

        if rule.input_pattern not in form:
            return form, False

        new_form = form.replace(
            rule.input_pattern,
            rule.replacement,
            1
        )

        return new_form, new_form != form
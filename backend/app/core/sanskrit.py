from .models import GrammarState, StateToken


def tokenize_sanskrit(
    text: str,
) -> GrammarState:

    tokens = []

    for index, character in enumerate(text):

        tokens.append(
            StateToken(
                token_id=f"input_{index}",
                surface=character,
                source="input",
                position=index,
                active=True,
            )
        )

    return GrammarState(
        tokens=tokens,
        step=0,
    )
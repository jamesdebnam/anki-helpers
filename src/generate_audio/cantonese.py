import re

import pycantonese

from src.types import FormattedCard


def split_jyutping(jyutping: str) -> str:
    # Use a regular expression to match Jyutping syllables.
    # It matches letters (including blends like 'ng') followed by a tone number (1-6).
    syllables = re.findall(r"[a-z]+[1-6]", jyutping)

    return " ".join(syllables)


def convert_cantonese_to_jyutping(card: FormattedCard) -> FormattedCard:
    text = card["back_field"]

    cantonese_characters = "".join(
        char for char in text if "\u4e00" <= char <= "\u9fff"
    )

    if not cantonese_characters:
        return card

    jyutping = pycantonese.characters_to_jyutping(cantonese_characters)

    romanised = " ".join([split_jyutping(jp) for canto, jp in jyutping])

    card["romanised"] = romanised

    return card

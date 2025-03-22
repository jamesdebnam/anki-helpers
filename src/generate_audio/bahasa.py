from src.types import FormattedCard


def format_bahasa(card: FormattedCard):
    card["back_field"] = card["back_field"].replace("/", "atau")
    return card

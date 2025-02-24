from typing import TypedDict


class FormattedCard(TypedDict):
    card_id: int
    front_field: str
    back_field: str
    includes_audio: bool


class FormattedCardWithRomanised(FormattedCard):
    romanised: str

import sys
import os

from anki.storage import Collection
from anki.notes import Note
from anki.media import MediaManager
import re

from src.types import FormattedCard, FormattedCard


def clean_back_field(back_field: str) -> str:
    """
    Cleans the back field by removing square-bracketed content (like [sound:...]),
    <br></br> tags, and &nbsp; entities.
    """
    # Remove anything in square brackets
    back_field = re.sub(r"\[.*?\]", "", back_field)
    # Remove all HTML tags
    back_field = re.sub(r"<.*?>", "", back_field, flags=re.IGNORECASE)
    # Remove &nbsp; entities
    back_field = back_field.replace("&nbsp;", "")

    # Strip leading and trailing whitespace
    return back_field.strip()


def append_image_to_card(col: Collection, image_file: str, card: FormattedCard):
    media_manager = MediaManager(col, False)
    card_obj = col.get_card(card["card_id"])
    note: Note = card_obj.note()

    if len(note.fields) > 0:
        media_manager.add_file(image_file)

        note.fields[0] = (
            f'{card["front_field"]} <br><br/> <img src="{os.path.basename(image_file)}">'
        )

        col.update_note(note)
        print(
            f"Image appended to the front field of card {card['card_id']} successfully."
        )
    else:
        print("Card does not have a front field.")


def append_audio_to_card(col: Collection, audio_file: str, card: FormattedCard):
    media_manager = MediaManager(col, False)

    card_obj = col.get_card(card["card_id"])
    note: Note = card_obj.note()

    if len(note.fields) > 1:
        media_manager.add_file(audio_file)
        note.fields[1] = (
            f'[sound:{os.path.basename(audio_file)}] <br></br> {card["romanised"]}'
        )
        if card["back_field"] != card["romanised"]:
            note.fields[1] += f'<br></br> {card["back_field"]}'
        col.update_note(note)
        print(f"Audio file appended to card {card['card_id']} successfully.")
    else:
        print("Card does not have a back field.")


def format_card(card) -> FormattedCard:
    note = card.note()
    fields = note.fields

    front_field = fields[0] if fields else ""
    back_field = fields[1] if len(fields) > 1 else ""
    includes_audio = "[sound:" in back_field
    includes_image = "<img" in front_field

    back_field_cleaned = clean_back_field(back_field)

    formatted_card: FormattedCard = {
        "card_id": card.id,
        "front_field": front_field,
        "back_field": back_field_cleaned,
        "includes_audio": includes_audio,
        "includes_image": includes_image,
        "romanised": back_field_cleaned,
    }
    return formatted_card


def find_cards(col: Collection, deck_name: str) -> list[FormattedCard]:
    recent_cards: list[FormattedCard] = []
    deck = col.decks.by_name(deck_name)
    if not deck:
        print(f"Deck '{deck_name}' not found.")
        return []

    # Find cards in the specified deck added in the last 24 hours
    print(col.find_cards(f"deck:{deck_name}"))
    for card in col.find_cards(f"deck:{deck_name}"):
        card_obj = col.get_card(card)
        formatted_card = format_card(card_obj)

        recent_cards.append(formatted_card)

    if not recent_cards:
        print(f"No cards found in deck '{deck_name}'")
        return []
    return recent_cards

import os
import sys
from anki.storage import Collection

from src.cantonese import convert_cantonese_to_jyutping
from src.db import find_cards, append_audio_to_card
from concurrent.futures import ThreadPoolExecutor
from src.audio import request_text_to_speech
from src.types import FormattedCardWithRomanised


def process_card(card: FormattedCardWithRomanised, col: Collection , deck_name: str):
    try:
        print(col)
        print(card)
        audio_file_path = request_text_to_speech(card, deck_name)
        append_audio_to_card(col,audio_file_path, card)

        print(f"Processed card {card['card_id']} successfully.")
    except Exception as e:
        print(f"Failed to process card {card['card_id']}: {str(e)}")


def locate_collection():
    if sys.platform == "win32":
        base_path = os.path.expandvars(r"%APPDATA%\Anki2")
    elif sys.platform == "darwin":
        base_path = os.path.expanduser("~/Library/Application Support/Anki2")
    else:
        base_path = os.path.expanduser("~/.local/share/Anki2")

    return os.path.join(base_path, "User 1", "collection.anki2")


def main(deck_name: str):
    col_path = locate_collection()
    if not os.path.exists(col_path):
        print(f"Could not find collection.anki2 at {col_path}")
        return

    col = Collection(col_path)
    try:

        cards = find_cards(col,deck_name)
        if deck_name == "Cantonese":
            cards = [convert_cantonese_to_jyutping(card) for card in cards]

        cards_without_audio = [card for card in cards if not card["includes_audio"]]

        print(cards_without_audio)
        print(f"Processing {len(cards_without_audio)} cards without audio...")
        tasks = [(card, col, deck_name) for card in cards_without_audio]

        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(lambda task: process_card(*task), tasks)

        print("All cards have been processed.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        col.close()

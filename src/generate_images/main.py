import os
import sys
from concurrent.futures import ThreadPoolExecutor

from anki.storage import Collection

from src.db import find_cards, append_image_to_card
from src.generate_images.image import generate_image
from src.types import FormattedCard
from src.utils import locate_collection


def process_card(card: FormattedCard, col: Collection, deck_name: str):
    try:
        image_file_path = generate_image(card["front_field"])
        append_image_to_card(col, image_file_path, card)

        print(f"Processed card {card['card_id']} successfully.")
    except Exception as e:
        print(f"Failed to process card {card['card_id']}: {str(e)}")


def main(deck_name: str):
    col_path = locate_collection()
    if not os.path.exists(col_path):
        print(f"Could not find collection.anki2 at {col_path}")
        return

    col = Collection(col_path)
    try:

        cards = find_cards(col, deck_name)

        cards_without_image = [card for card in cards if not card["includes_image"]]

        print(cards_without_image)
        print(f"Processing {len(cards_without_image)} cards without image...")
        tasks = [(card, col, deck_name) for card in cards_without_image]

        with ThreadPoolExecutor(max_workers=4) as executor:
            executor.map(lambda task: process_card(*task), tasks)

        print("All cards have been processed.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        col.close()

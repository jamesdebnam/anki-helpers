import sys

from src.generate_images.main import main

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python find_recent_cards_local.py <deck_name>")
        sys.exit(1)

    deck_name = sys.argv[1]
    main(deck_name)

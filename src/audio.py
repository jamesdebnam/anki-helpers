import os

from src.types import FormattedCard


import requests


def request_text_to_speech(card: FormattedCard, deck_name: str):
    voice = None
    if deck_name == "Cantonese":
        voice = "Man-Chi"
    if deck_name == "Bahasa":
        voice = "Abyasa"

    if voice is None:
        raise Exception("Voice not found.")

    url = f"https://api.narakeet.com/text-to-speech/m4a?voice={voice}"
    text = card["back_field"]
    options = {
        "headers": {
            "Accept": "application/octet-stream",
            "Content-Type": "text/plain",
            "x-api-key": os.environ["NARAKEET_API_KEY"],
        },
        "data": text.encode("utf8"),
    }

    try:
        response = requests.post(url, **options)
        response.raise_for_status()
        assets_dir = "./assets"
        if not os.path.exists(assets_dir):
            os.makedirs(assets_dir)

        file_path = f"{assets_dir}/{text}.m4a"
        with open(file_path, "wb") as f:
            f.write(response.content)

        return file_path
    except requests.exceptions.HTTPError as e:
        # Enhance the error message to include response content if available
        error_message = (
            f"HTTP error occurred: {e.response.status_code} - {e.response.reason}"
        )
        error_details = e.response.text
        raise Exception(f"{error_message}. Details: {error_details}") from None

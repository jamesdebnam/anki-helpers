# anki-helpers
Helpful anki tools for my own enjoyment

Feel free to download and use these tools for your own personal enjoyment too!

Usage is as follows:

1. Create accounts at stability ai and narakeet, input API keys in a local .env file
2. To generate audio, you will first need to add the voice you'd like to use based on your deck name in narakeet. Add 
this to request_text_to_speech, or you'll get a voice not found error
3. Run the following command for audio: 

```
$ pipenv install
$ pipenv run generate_audio <DECK_NAME>
```

4. Run the following command for image generation:

```
$ pipenv install
$ pipenv run generate_images <DECK_NAME>
```

### Usage notes

It's very important you have anki decks downloaded locally, and that your anki application is not running!!
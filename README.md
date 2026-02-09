
A simple Telegram bot that stores messages (text, media, files) and generates shareable deep links. When a user opens the link, the stored content is sent to them automatically.

## Author
* **Author:** Mr. Velox
* **Telegram:** C2_9H

## Features
* Supports Text, Photos, Videos, Audio, Voice, and Documents.
* SQLite database for persistent storage.
* Unique ID generation for every upload.
* Deep linking support (`/start <id>`).

## Setup
1.  Install Python 3.9+.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Open `main.py` and replace `YOUR_TOKEN_HERE` with your actual Telegram Bot Token.
4.  Run the bot: `python main.py`

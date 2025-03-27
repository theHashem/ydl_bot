# YouTube to MP3 Telegram Bot

This Telegram bot allows users to download YouTube videos as MP3 files.

Use the existing bot <a href="https://t.me/ydl01_bot">@ydl01_bot</a>

Feel free to write me if you have any questions: <a href="https://t.me/NoCallAllowed">@NoCallAllowed</a>

## Features

- Downloads MP3 files from YouTube video links.
- Sends the downloaded MP3 files directly via Telegram.


## Requirements

- Python 3.7 or higher
- Telegram Bot Token (create a bot using BotFather)
- A server or Raspberry Pi to run the bot

## Update yt-dlp Command:

```bash
pip install --upgrade yt-dlp
```
or
```bash
yt-dlp -U 
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/theHashem/ydl_bot.git
```

### 2. Create a Virtual Environment and Activate It

```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate   # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

1. Add your Telegram Bot Token in the `main()` function in the code.
2. Start the bot:

   ```bash
   python ydl_bot.py
   ```

3. Open Telegram, find your bot, and send it a YouTube link. The bot will download and send you the MP3 file.

## Raspberry Pi as Telegram Bot Server

### 1. Copy the Bot Code to Your Raspberry Pi

Place `ydl_bot.py` in a directory on your Raspberry Pi.

### 2. Create a Systemd Service

Create a new service file:

```bash
sudo nano /etc/systemd/system/telegram_bot.service
```

Add the following content:

```ini
[Unit]
Description=Telegram Bot Service
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/bin/python3 /path/to/ydl_bot.py
WorkingDirectory=/path/to/
Restart=always
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
```

Replace `/path/to/` with the actual path to your bot script.

### 3. Enable and Start the Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram_bot.service
sudo systemctl start telegram_bot.service
```

Now, your Telegram bot will automatically start when the Raspberry Pi boots up.

## Notes

- Ensure that the `downloads/` directory exists in the script's working directory.
- Install `ffmpeg` on your system for proper audio processing:

  ```bash
  sudo apt install ffmpeg
  ```

Enjoy using your YouTube to MP3 Telegram Bot!

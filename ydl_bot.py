"""
Create by Hashem 
Web: https://www.hashem.it
Github: https://github.com/theHashem
Lindin: https://linkedin.com/in/hashem01
Telegram: https://t.me/NoCallAllowed

"""

import telebot
import yt_dlp
import os

# Your Telegram-Bot-Token
TOKEN = "your_Telegram_Token"
bot = telebot.TeleBot(TOKEN)

# Function to download the MP3 file
def download_audio_as_mp3(video_url):
    try:
        # Options for yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            return filename
    except Exception as e:
        print(f"Fehler beim Herunterladen: {e}")
        return None

# Bot-Handler for messages
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi, Send me a YouTube-Link!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    video_url = message.text

    # Check if the message is a YouTube link
    if "youtube.com" in video_url or "youtu.be" in video_url:
        # Send message that the download is starting
        waiting_message = bot.reply_to(message, "Please wait, the audio is downloading...")

        # MP3 download
        mp3_file = download_audio_as_mp3(video_url)

        if mp3_file:
            # Send MP3 file to the user
            with open(mp3_file, 'rb') as audio:
                bot.send_audio(message.chat.id, audio)
            
            # Delete local file to save storage space
            os.remove(mp3_file)

            # Delete message
            bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)
        else:
            bot.reply_to(message, "Sorry, there was a problem downloading the file.")
    else:
        bot.reply_to(message, "No valid YouTube link.")

# Start bot
print("Bot running...")
bot.polling()
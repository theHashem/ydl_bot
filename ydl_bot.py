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

# Your Telegram Bot token and admin chat ID
TOKEN = "your_Telegram_Token"
ADMIN_CHAT_ID = "yourCahtID"

bot = telebot.TeleBot(TOKEN)

# Constant for maximum video duration (in seconds, here 50 minutes)
MAX_VIDEO_DURATION = 50 * 60

def download_audio_as_mp3(video_url):
    """Downloads the audio of a video as an MP3 file."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            base, ext = os.path.splitext(filename)
            if ext.lower() in ['.webm', '.m4a']:
                filename = base + ".mp3"
            return filename
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None

def save_link(link):
    """Notifies the admin about a new, valid link."""
    try:
        bot.send_message(ADMIN_CHAT_ID, f"New link saved: {link}")
    except Exception as e:
        print(f"Error sending link to admin: {e}")

def notify_new_user(chat_id):
    """Notifies the admin with the new user chat ID and the current user count."""
    count = get_user_count()
    try:
        bot.send_message(ADMIN_CHAT_ID, f"New user added: {chat_id}. Updated user count: {count}")
    except Exception as e:
        print(f"Error sending new user notification to admin: {e}")

def save_user_id(chat_id):

    file_name = "user_ids.txt"
    try:
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                f.write(str(chat_id) + "\n")
            notify_new_user(chat_id)
        else:
            with open(file_name, "r") as f:
                user_ids = {line.strip() for line in f if line.strip()}
            if str(chat_id) not in user_ids:
                with open(file_name, "a") as f:
                    f.write(str(chat_id) + "\n")
                notify_new_user(chat_id)
    except Exception as e:
        print(f"Error saving user ID: {e}")

def get_user_count():
    """Returns the number of saved user chat IDs."""
    file_name = "user_ids.txt"
    try:
        if not os.path.exists(file_name):
            return 0
        with open(file_name, "r") as f:
            user_ids = {line.strip() for line in f if line.strip()}
        return len(user_ids)
    except Exception as e:
        print(f"Error reading the user file: {e}")
        return 0

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Save the user's chat ID
    save_user_id(message.chat.id)
    bot.reply_to(message, "Hi, send me a YouTube link!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Save the user's chat ID for every received message
    save_user_id(message.chat.id)
    
    video_url = message.text.strip()
    
    # Check if the message is a valid YouTube link
    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        bot.reply_to(message, "Not a valid YouTube link.")
        return

    # Notify the admin about the new link
    save_link(video_url)

    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(video_url, download=False)
    except Exception as e:
        bot.reply_to(message, "Error fetching video information.")
        print(f"Error fetching video information: {e}")
        return

    # Check the duration of the video
    duration = info.get("duration", 0)
    if duration > MAX_VIDEO_DURATION:
        bot.reply_to(message, "The video is longer than 50 minutes. Processing aborted, file too large.")
        return

    waiting_message = bot.reply_to(message, "Please wait, audio is being downloaded...")
    mp3_file = download_audio_as_mp3(video_url)

    if mp3_file and os.path.exists(mp3_file):
        with open(mp3_file, "rb") as audio:
            bot.send_audio(message.chat.id, audio)
        os.remove(mp3_file)
        bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)
    else:
        bot.reply_to(message, "Error downloading the file.")

if __name__ == '__main__':
    print("Bot is running...")
    bot.polling()
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

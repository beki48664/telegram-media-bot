import telebot
from telebot import types
import yt_dlp
import os

TOKEN = "8064305593:AAHI5ytBdKajbpxatcp0nUObQYJD70nB7pE"

bot = telebot.TeleBot(TOKEN)

search_results = {}

# START
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "🎵 Qo'shiq nomini yoz\n"
        "📥 Yoki YouTube / Instagram / TikTok link yubor")

# MAIN
@bot.message_handler(func=lambda m: True)
def handle(message):

    text = message.text

    # 🔹 LINK BO'LSA
    if "youtube.com" in text or "youtu.be" in text or "instagram.com" in text or "tiktok.com" in text:

        bot.send_message(message.chat.id, "📥 Video yuklanmoqda...")

        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.%(ext)s'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                file = ydl.prepare_filename(info)

            bot.send_video(message.chat.id, open(file, 'rb'))
            os.remove(file)

        except:
            bot.send_message(message.chat.id, "❌ Video yuklab bo‘lmadi")

    # 🔹 QO‘SHIQ NOMI BO'LSA
    else:
        bot.send_message(message.chat.id, "🔎 Qidirilmoqda...")

        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(f"ytsearch10:{text}", download=False)

            results = info['entries']
            search_results[message.chat.id] = results

            msg = "🎧 Natijalar:\n\n"
            keyboard = types.InlineKeyboardMarkup()

            for i, r in enumerate(results):
                msg += f"{i+1}. {r['title']}\n"
                keyboard.add(types.InlineKeyboardButton(str(i+1), callback_data=str(i)))

            bot.send_message(message.chat.id, msg, reply_markup=keyboard)

        except:
            bot.send_message(message.chat.id, "❌ Qidirishda xatolik")

# 🔹 TUGMA BOSILGANDA
@bot.callback_query_handler(func=lambda call: True)
def download(call):

    try:
        index = int(call.data)
        results = search_results.get(call.message.chat.id)

        url = results[index]['webpage_url']

        bot.send_message(call.message.chat.id, "🎧 Yuklanmoqda...")

        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': 'song.%(ext)s'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)

        bot.send_audio(call.message.chat.id, open(file, 'rb'))
        os.remove(file)

    except:
        bot.send_message(call.message.chat.id, "❌ Yuklab bo‘lmadi")

bot.infinity_polling()
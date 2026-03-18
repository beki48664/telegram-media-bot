import telebot
from telebot import types
import yt_dlp
import os
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = "8064305593:AAHI5ytBdKajbpxatcp0nUObQYJD70nB7pE"
bot = telebot.TeleBot(TOKEN)

search_results = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
    "🎵 Qo‘shiq nomini yoz yoki link yubor")

@bot.message_handler(func=lambda m: True)
def search(message):
    text = message.text

    # LINK BO'LSA
    if "http" in text:
        bot.send_message(message.chat.id, "📥 Yuklanmoqda...")

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
            bot.send_message(message.chat.id, "❌ Xatolik")

    # QO‘SHIQ NOMI BO'LSA
    else:
        bot.send_message(message.chat.id, "🔎 Qidirilmoqda...")

        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(f"ytsearch5:{text}", download=False)

            results = info['entries']
            search_results[message.chat.id] = results

            keyboard = types.InlineKeyboardMarkup()
            msg = "🎧 Variantlar:\n\n"

            for i, r in enumerate(results):
                title = r['title']
                msg += f"{i+1}. {title}\n"
                keyboard.add(types.InlineKeyboardButton(str(i+1), callback_data=str(i)))

            bot.send_message(message.chat.id, msg, reply_markup=keyboard)

        except:
            bot.send_message(message.chat.id, "❌ Qidirishda xatolik")

@bot.callback_query_handler(func=lambda call: True)
def download(call):
    try:
        index = int(call.data)
        results = search_results.get(call.message.chat.id)

        url = results[index]['webpage_url']
        title = results[index]['title']

        bot.send_message(call.message.chat.id, "🎧 Yuklanmoqda...")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)

        with open(file, 'rb') as audio:
            bot.send_document(call.message.chat.id, audio, caption=title)

        os.remove(file)

    except Exception as e:
        print(e)
        bot.send_message(call.message.chat.id, "❌ Yuklab bo‘lmadi")

bot.infinity_polling()
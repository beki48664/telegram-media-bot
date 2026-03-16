import telebot
from telebot import types
from config import TOKEN
from search import search_music
from downloader import download_audio
from admin import add_user

bot=telebot.TeleBot(TOKEN)

results_store={}

@bot.message_handler(commands=['start'])
def start(m):

    add_user(m.chat.id)

    bot.send_message(m.chat.id,"🎵 Qo'shiq nomini yoz")

@bot.message_handler(func=lambda m:True)
def music(m):

    results=search_music(m.text)

    results_store[m.chat.id]=results

    msg=""

    keyboard=types.InlineKeyboardMarkup()

    for i,r in enumerate(results):

        msg+=f"{i+1}. {r['title']}\n"

        keyboard.add(
            types.InlineKeyboardButton(
                str(i+1),
                callback_data=str(i)
            )
        )

    bot.send_message(m.chat.id,msg,reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call:True)
def download(call):

    results=results_store.get(call.message.chat.id)

    url=results[int(call.data)]['webpage_url']

    bot.send_message(call.message.chat.id,"⬇️ Yuklanmoqda...")

    file=download_audio(url)

    bot.send_audio(call.message.chat.id,open(file,'rb'))

bot.infinity_polling()
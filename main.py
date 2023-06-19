from telebot.async_telebot import AsyncTeleBot
import asyncio
from telebot.types import ForceReply
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = AsyncTeleBot('6286035570:AAGUyK_aRQaZdERTc3ZDYB5fqY-mcH6UWQM')

#@SIXDAY\n

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    global chat_id
    chat_id = message.chat.id
    markup = ForceReply(selective=False, input_field_placeholder = 'Имя:')
    info = await bot.send_message(chat_id, 'Привет, ввдите ваше имя', reply_markup=markup)
    print(info)



    # markup = InlineKeyboardMarkup()
    # markup.add(InlineKeyboardButton(text='Первая кнопка', callback_data='1'))
    # markup.add(InlineKeyboardButton(text='Вторая кнопка', callback_data='2'))
    # await bot.send_message(chat_id, 'Кнопки под сообщением', reply_markup=markup)
    # указываем широту и долготу дробными числами

asyncio.run(bot.polling())
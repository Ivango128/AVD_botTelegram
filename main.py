from telebot import types
from telebot.async_telebot import AsyncTeleBot
import asyncio
import os

from telebot.asyncio_filters import SimpleCustomFilter
from telebot.types import ForceReply
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = AsyncTeleBot('6286035570:AAGUyK_aRQaZdERTc3ZDYB5fqY-mcH6UWQM')
bd_file_name = 'bd.txt'

questions_list = [['Укажите ваше ФИО', None],
                  ['Возвраст (число полных лет)', None],
                  ['Выберите ваш уровень оброзования', {'высшие': 'high',
                                                        'не оконченое высшие': 'not_hight',
                                                        'среднее профессиональное': 'middle_prof',
                                                        'начальное профессиональное': 'start_prof',
                                                        'среднее': 'middle',
                                                        'не оконченое среднее': 'not_middle'}],
                  ['Название учебного заведения', None]]

index_question = 0

def first_power():
    if os.path.isfile(bd_file_name):
        print("Файл существует")
    else:
        with open(bd_file_name, 'w', encoding= 'UTF-8') as file:
            print('Файл создан')

def new_user_reg(message):
    chat_id = message.from_user.id
    new_user_bool = False
    with open(bd_file_name, 'r', encoding= 'UTF-8') as file:
        file_bd = file.read()
        if len(file_bd) != 0:
            if str(chat_id) in file_bd:
                print("Пользователь уже зарегистрирован")
                new_user_bool = False
            else:
                print("Пользователь не зарегистрирован")
                new_user_bool = True
        else:
            print("Пользователь не зарегистрирован")
            new_user_bool = True
    if new_user_bool:
        with open(bd_file_name, 'a', encoding= 'UTF-8') as file:
            file.write(str(chat_id) + '|'+ str(message.from_user.first_name) + '\n')
        return False

    return True


def create_keyboard_markup(button_dict):
    keyboard = types.InlineKeyboardMarkup()
    for button_text, callback_data in button_dict.items():
        button = types.InlineKeyboardButton(button_text, callback_data=callback_data)
        keyboard.add(button)

    return keyboard

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    global chat_id
    chat_id = message.from_user.id
    print(str(chat_id) + " " + str(message.from_user.first_name))
    button_dict = {
        'О нас': 'about_as',
        'Запись в отдел кадров': 'record_in_PD',
    }
    keyboard = create_keyboard_markup(button_dict)
    global bot_message
    if new_user_reg(message):
        bot_message = await bot.send_message(chat_id, 'С возвращением, ' + str(message.from_user.first_name) + '!', reply_markup=keyboard)
        print(bot_message.id)
    else:
        bot_message = await bot.send_message(chat_id, 'Привет, рад познокомится, ' + str(message.from_user.first_name) + '!', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
async def handle_callback(call):
    global index_question
    global bot_message
    #global chat_id
    chat_id = call.message.chat.id
    button_call = call.data
    # Обработка выбранной кнопки
    if button_call == 'about_as':
        await bot.edit_message_text("Вы выбрали кнопку 1.", chat_id, bot_message.id)
    elif button_call == 'record_in_PD':
        button_dict = {
            'Заполнить резюме': 'start_resume',
            'На главную 🏠': 'main',
        }
        await bot.edit_message_text("Вы можите заполнить резюме, и вам перезвонит сотрудник отдела кадров.", chat_id, bot_message.id, reply_markup=create_keyboard_markup(button_dict))
    elif button_call =='start_resume':
        global start_resume
        start_resume = call
        if questions_list[index_question][1] == None:
            markup = types.ForceReply(selective=False)
            await bot.delete_message(chat_id, bot_message.id)
            bot_message = await bot.send_message(chat_id, questions_list[index_question][0], reply_markup=markup)
            #index_question += 1
        else:
            await bot.delete_message(chat_id, bot_message.id)
            bot_message = await bot.send_message(chat_id, questions_list[index_question][0],  reply_markup=create_keyboard_markup(questions_list[index_question][1]))
            #index_question += 1
    elif button_call == 'main':
        button_dict = {
            'О нас': 'about_as',
            'Запись в отдел кадров': 'record_in_PD',
        }
        await bot.edit_message_text('Начнем заново? 😊', chat_id, bot_message.id, reply_markup=create_keyboard_markup(button_dict))


@bot.message_handler(func=lambda message: True)
async def handle_reply(message):
    print(message.reply_to_message)
    if message.reply_to_message is not None:
        global index_question
        index_question += 1
        await handle_callback(start_resume)
        await bot.delete_message(chat_id, message.id)










first_power()
asyncio.run(bot.polling())
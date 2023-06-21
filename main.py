from telebot import types
from telebot.async_telebot import AsyncTeleBot
import asyncio
import os
import json


bot = AsyncTeleBot('6286035570:AAGUyK_aRQaZdERTc3ZDYB5fqY-mcH6UWQM')
bd_file_name = 'bd_candidate.json'

questions_list = [['Укажите ваше ФИО', None],
                  ['Возвраст (число полных лет)', None],
                  ['Выберите ваш уровень оброзования', {'высшие': 'high',
                                                        'не оконченое высшие': 'not_hight',
                                                        'среднее профессиональное': 'middle_prof',
                                                        'начальное профессиональное': 'start_prof',
                                                        'среднее': 'middle',
                                                        'не оконченое среднее': 'not_middle'}],
                  ['Название учебного заведения', None]]


def first_power():
    if os.path.isfile('session.json'):
        print("Файл существует")
    else:
        session = {}
        with open('session.json', 'w') as file:
            # Записываем данные в JSON-файл
            json.dump(session, file)

    if os.path.isfile(bd_file_name):
        print("Файл существует")
    else:
        bd_candidate = {}
        with open(bd_file_name, 'w') as file:
            # Записываем данные в JSON-файл
            json.dump(bd_candidate, file)



def new_user_reg(message):
    chat_id = message.from_user.id
    print(type(chat_id))
    new_user_bool = False
    with open('session.json', 'r') as file:
        # Загружаем данные из JSON-файла
        session = json.load(file)
    if str(chat_id) in session:
        print("Пользователь уже зарегистрирован")
        return True
    else:
        print("Пользователь не зарегистрирован")
        session[chat_id] = {
            'name': message.from_user.first_name,
            'index_question': 0
        }
        with open('session.json', 'w') as file:
            json.dump(session, file, ensure_ascii=False)
        return False

def get_session():
    with open('session.json', 'r') as file:
        # Загружаем данные из JSON-файла
        session = json.load(file)
    return session
def save_session(session):
    with open('session.json', 'w') as file:
        # Записываем данные в JSON-файл
        json.dump(session, file, ensure_ascii=False)

async def response_handler(chat_id, session):
    global bot_message
    index_question = session[str(chat_id)]['index_question']
    if questions_list[index_question][1] == None:
        markup = types.ForceReply(selective=False)
        await bot.delete_message(chat_id, bot_message.id)
        bot_message = await bot.send_message(chat_id, questions_list[index_question][0], reply_markup=markup)

    else:
        await bot.delete_message(chat_id, bot_message.id)
        bot_message = await bot.send_message(chat_id, questions_list[index_question][0], reply_markup=create_keyboard_markup(questions_list[index_question][1]))




def create_keyboard_markup(button_dict):
    keyboard = types.InlineKeyboardMarkup()
    for button_text, callback_data in button_dict.items():
        button = types.InlineKeyboardButton(button_text, callback_data=callback_data)
        keyboard.add(button)

    return keyboard

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
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
    else:
        bot_message = await bot.send_message(chat_id, 'Привет, рад познокомится, ' + str(message.from_user.first_name) + '!', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
async def handle_callback(call):
    global bot_message
    chat_id = call.message.chat.id
    button_call = call.data
    session = get_session()
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
        await response_handler(chat_id, session)
    elif button_call =='high':
        pass
    elif button_call == 'main':
        button_dict = {
            'О нас': 'about_as',
            'Запись в отдел кадров': 'record_in_PD',
        }
        await bot.edit_message_text('Начнем заново? 😊', chat_id, bot_message.id, reply_markup=create_keyboard_markup(button_dict))


@bot.message_handler(func=lambda message: True)
async def handle_reply(message):
    chat_id = message.chat.id
    if message.reply_to_message is not None:
        session = get_session()
        session[str(chat_id)]['index_question'] += 1
        save_session(session)
        await handle_callback(start_resume)
        await bot.delete_message(chat_id, message.id)










first_power()
asyncio.run(bot.polling())
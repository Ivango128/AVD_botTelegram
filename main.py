from telebot import types
from telebot.async_telebot import AsyncTeleBot
import asyncio
import os
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = AsyncTeleBot(os.getenv('TOKEN'))

question_category = ['full_name','old','education', 'name_organization', 'year_ending', 'speciality',
                     'study_now', 'location', 'renting_house', 'phone_number', 'family_status', 'children',
                     'military_service', 'experience', 'shift_work', 'business_trips', 'housing_problem',
                     'skill_PK', 'knowledge_programms', 'language_level', 'contraindications', 'found_us', 'personal_qualities']


questions_list = [['Укажите ваше ФИО', None],
                  ['Возраст (число полных лет)', None],
                  ['Выберите ваш уровень образования', {'высшие': 'high',
                                                        'неоконченное высшее': 'not_hight',
                                                        'среднее профессиональное': 'middle_prof',
                                                        'начальное профессиональное': 'start_prof',
                                                        'среднее': 'middle',
                                                        'неоконченное среднее': 'not_middle'}],
                  ['Название учебного заведения', None],
                  ['Год окончания?', None],
                  ['Специальность по диплому', None],
                  ['Учеба в настоящее время', None],
                  ['В каком районе Вы живете?', None],
                  ['Снимаете ли вы жилье?', {'да': 'home', 'нет': 'not_home'}],
                  ['Контактный телефон', None],
                  ['Семейное положение', {'свободен': 'free_family','есть парень/девушка': 'boy_family', 'женат/замужем': 'married'}],
                  ['Дети до 18 лет, (указать возраст, инвалидность)\nПример: 16-нет, 12-есть', None],
                  ['Служба в органах ВС', {'да': 'served', 'нет': 'not_served'}],
                  ['Опыт работы по претендуемой профессии? (кол-во лет)', None],
                  ['Имеете ли Вы возможность работать по сменам?', {'да': 'change', 'нет': 'not_change'}],
                  ['Имеете ли Вы возможность ездить в командировки?', {'да': 'mission', 'нет': 'not_mission'}],
                  ['Решена ли у Вас жилищная проблема?', {'да': 'problem', 'нет': 'not_problem'}],
                  ['Умеете ли Вы работать на ПК?', {'да': 'pk', 'нет': 'not_pk'}],
                  ['Какие программы вы знаете?', None],
                  ['Выберите уровень знания иностранного языка', {'(А1) – начальный': 'first_level',
                                                                  '(А2) – ниже среднего': 'second_level',
                                                                  '(В1) – средний': 'third_level',
                                                                  '(В2) – выше среднего': 'fourth_level',
                                                                  '(C1) – продвинутый': 'fifth_level',
                                                                  '(C2) – профессиональный уровень владения': 'sixth_level',
                                                                  'Не знаю': 'zero_level'}],
                  ['Личные противопоказания по состоянию здоровья?', None],
                  ['Как Вы о нас узнали?', None],
                  ['Личные качества?', None]
                  ]


def first_power():
    if os.path.isfile('session.json'):
        print("Файл существует")
    else:
        session = {}
        with open('session.json', 'w') as file:
            # Записываем данные в JSON-файл
            json.dump(session, file)



def new_user_reg(message):
    chat_id = message.from_user.id
    print(type(chat_id)) # Проверка типа
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


async def response_handler(chat_id ):
    global bot_message
    session = get_session()
    index_question = session[str(chat_id)]['index_question']
    if questions_list[index_question][1] == None:
        markup = types.ForceReply(selective=False)
        await bot.delete_message(chat_id, bot_message.id)
        bot_message = await bot.send_message(chat_id, questions_list[index_question][0], reply_markup=markup)
    else:
        await bot.delete_message(chat_id, bot_message.id)
        bot_message = await bot.send_message(chat_id, questions_list[index_question][0], reply_markup=create_keyboard_markup(questions_list[index_question][1]))


def get_button_text(call, callback_data):
    button_list = call.json['message']['reply_markup']['inline_keyboard']
    for row in button_list:
        for button in row:
            if button['callback_data'] == callback_data:
                return button['text']
    return None


def create_keyboard_markup(button_dict):
    keyboard = types.InlineKeyboardMarkup()
    for button_text, callback_data in button_dict.items():
        button = types.InlineKeyboardButton(button_text, callback_data=callback_data)
        keyboard.add(button)

    return keyboard

@bot.message_handler(commands=['main'])
async def send_main(message):
    chat_id = message.from_user.id
    button_dict = {
        'О нас': 'about_as',
        'Продолжить заполнять резюме': 'record_in_PD',
    }
    global bot_message
    await bot.delete_message(chat_id, bot_message.id)
    await bot.delete_message(chat_id, message.id)
    bot_message = await bot.send_message(chat_id,'Начнем заново? 😊', reply_markup=create_keyboard_markup(button_dict))

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

async def handle_callback_response(chat_id, call, button_call):
    session = get_session()
    session[str(chat_id)][question_category[session[str(chat_id)]['index_question']]] = get_button_text(call, button_call)
    session[str(chat_id)]['index_question'] += 1
    save_session(session)
    await handle_callback(start_resume)


@bot.callback_query_handler(func=lambda call: True)
async def handle_callback(call):
    print(call.json['message']['reply_markup']['inline_keyboard'])
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
        await response_handler(chat_id)
    elif button_call == 'main':
        button_dict = {
            'О нас': 'about_as',
            'Продолжить заполнять резюме': 'record_in_PD',
        }
        await bot.edit_message_text('Начнем заново? 😊', chat_id, bot_message.id, reply_markup=create_keyboard_markup(button_dict))
    else:
        await handle_callback_response(chat_id, call, button_call)


async def handle_reply_response(chat_id, message):
    session = get_session()
    try:
        session[str(chat_id)][question_category[session[str(chat_id)]['index_question']]] = int(message.text)
    except:
        session[str(chat_id)][question_category[session[str(chat_id)]['index_question']]] = message.text
    session[str(chat_id)]['index_question'] += 1
    save_session(session)
    await handle_callback(start_resume)
    await bot.delete_message(chat_id, message.id)


@bot.message_handler(func=lambda message: True)
async def handle_reply(message):
    chat_id = message.chat.id
    session = get_session()
    if message.reply_to_message is not None:
        await handle_reply_response(chat_id, message)



first_power()
asyncio.run(bot.polling())
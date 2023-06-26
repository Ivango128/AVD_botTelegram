from telebot import types
from telebot.async_telebot import AsyncTeleBot
import asyncio
import os
import json
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import re
#from telebot.types import User

from sendEmail import send_email
from sendEmail import create_docx

from variable import Users

load_dotenv(find_dotenv())

bot = AsyncTeleBot(os.getenv('TOKEN'))
finish_text_path = os.getenv('PATH_finis_text')
session_path = os.getenv('PATH_session')


question_category = ['full_name','old','education', 'name_organization1', 'year_ending', 'speciality',
                     'study_now', 'location', 'renting_house', 'phone_number', 'family_status', 'children',
                     'military_service', 'experience', 'shift_work', 'business_trips', 'housing_problem',
                     'skill_PK', 'knowledge_programms', 'language_level', 'contraindications', 'found_us', 'personal_qualities', 'work_experience']

work_experience_keys_list = ['period_employment', 'name_organization', 'position_held', 'reason_leaving']
level_claims_keys_list = ['work_period', 'minimum_salary', 'desired_salary']


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
                  ['Личные качества?', None]]


q_list_prov = []
for item in questions_list:
    q_list_prov.append(item[0])

w = ['Период работы\nПример ввода: 06.21 - 05.23', 'Название организации', 'Занимаемая должность','Причина увольнения']
c = ['Желаемая профеcсия и должность', 'Минимальная зп', 'Желаемая зп']

q_list_prov.extend(w)
q_list_prov.extend(c)

user_data = Users()

def first_power():
    if os.path.isfile(session_path):
        print("Файл существует")
    else:
        session = {}
        with open(session_path, 'w') as file:
            # Записываем данные в JSON-файл
            json.dump(session, file)



def new_user_reg(message):
    chat_id = message.from_user.id
    new_user_bool = False
    with open(session_path, 'r') as file:
        # Загружаем данные из JSON-файла
        session = json.load(file)
    if str(chat_id) in session:
        user_data.add_user(str(chat_id))
        print("Пользователь уже зарегистрирован")
        return True
    else:
        print("Пользователь не зарегистрирован")
        user_data.add_user(str(chat_id))
        session[chat_id] = {
            'name': message.from_user.first_name,
            'bot_message_id': 0,
            'index_question': 0,
            'current_question': 0,
            'index_q_work': 0,
            'value_q_work': 0,
            'index_q_level': 0,
            'value_q_level': 0,
            'count_send_resume':0,
            'data_send_resume': '',
            'data_send_request': '',
            'answers': {
                "full_name": "",
                "old": "",
                "education": "",
                "name_organization1": "",
                "year_ending": "",
                "speciality": "",
                "study_now": "",
                "location": "",
                "renting_house": "",
                "phone_number": "",
                "family_status": "",
                "children": "",
                "military_service": "",
                "experience": "",
                "shift_work": "",
                "business_trips": "",
                "housing_problem": "",
                "skill_PK": "",
                "knowledge_programms": "",
                "language_level": "",
                "contraindications": "",
                "found_us": "",
                "personal_qualities": "",
                'work_experience': [{
                    "period_employment": "",
                    "name_organization": "",
                    "position_held": "",
                    "reason_leaving": ""
                }],
                'level_of_claims': [{
                    "work_period": "",
                    "minimum_salary": "",
                    "desired_salary": ""
                }]
            }
        }
        with open(session_path, 'w') as file:
            json.dump(session, file, ensure_ascii=False)
        return False

def get_session():
    with open(session_path, 'r') as file:
        # Загружаем данные из JSON-файла
        session = json.load(file)
    return session
def save_session(session):
    with open(session_path, 'w') as file:
        # Записываем данные в JSON-файл
        json.dump(session, file, ensure_ascii=False)


def preparation_dictionaries(chat_id):
    session = get_session()
    work_experience = session[str(chat_id)]['answers']['work_experience']
    level_of_claims = session[str(chat_id)]['answers']['level_of_claims']
    answers = session[str(chat_id)]['answers']
    del answers['work_experience']
    del answers['level_of_claims']
    answers['data_send_resume'] = str(datetime.now().strftime("%d.%m.%Y"))
    return answers, work_experience, level_of_claims




def get_finish_text(chat_id):
    session = get_session()
    with open("confirmation.txt", "r", encoding='UTF-8') as file:
        finsh_text = file.read()
        finsh_text = finsh_text.replace('FIO', session[str(chat_id)]['answers']['full_name'])
    return finsh_text

async def response_handler(chat_id):
    session = get_session()
    index_question = session[str(chat_id)]['index_question']
    if questions_list[index_question][1] == None:
        markup = types.ForceReply(selective=False)
        await bot.delete_message(chat_id, session[str(chat_id)]['bot_message_id'])
        bot_message = await bot.send_message(chat_id, questions_list[index_question][0], reply_markup=markup)
        session[str(chat_id)]['bot_message_id'] = bot_message.id
        save_session(session)
    else:
        await bot.delete_message(chat_id, session[str(chat_id)]['bot_message_id'])
        bot_message = await bot.send_message(chat_id, questions_list[index_question][0], reply_markup=create_keyboard_markup(questions_list[index_question][1]))
        session[str(chat_id)]['bot_message_id'] = bot_message.id
        save_session(session)


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


async def question_period_work_and_level_claims(call, chapter, text):
    session = get_session()
    work_experience_string = ''
    chat_id = call.from_user.id
    for item in session[str(chat_id)]['answers'][chapter]:
        if item:
            work_experience_string += " ".join(item.values()) + "\n"
    button_dict = {
        'следующий вопрос': 'next_question',
        'добавить': 'add_work',
    }
    await bot.delete_message(chat_id, session[str(chat_id)]['bot_message_id'])
    bot_message = await bot.send_message(chat_id, text+'\n'+work_experience_string, reply_markup=create_keyboard_markup(button_dict))
    session[str(chat_id)]['bot_message_id'] = bot_message.id
    save_session(session)

async def four_question_work(call):
    chat_id = call.from_user.id
    session = get_session()
    work_list = ['Период работы\nПример ввода: 06.21 - 05.23', 'Название организации', 'Занимаемая должность','Причина увольнения']
    claims_list = ['Желаемая профеcсия и должность', 'Минимальная зп', 'Желаемая зп']
    markup = types.ForceReply(selective=False)
    await bot.delete_message(chat_id, session[str(chat_id)]['bot_message_id'])
    if session[str(chat_id)]['index_question'] == len(questions_list):
        bot_message = await bot.send_message(chat_id, work_list[session[str(chat_id)]['index_q_work']], reply_markup=markup)
        session[str(chat_id)]['bot_message_id'] = bot_message.id
        save_session(session)
    elif session[str(chat_id)]['index_question'] == len(questions_list)+1:
        bot_message = await bot.send_message(chat_id, claims_list[session[str(chat_id)]['index_q_level']], reply_markup=markup)
        session[str(chat_id)]['bot_message_id'] = bot_message.id
        save_session(session)

async def handle_callback_response(chat_id, call, button_call):
    session = get_session()
    session[str(chat_id)]['answers'][question_category[session[str(chat_id)]['index_question']]] = get_button_text(call, button_call)
    session[str(chat_id)]['index_question'] += 1
    save_session(session)
    await handle_callback(user_data.users[str(chat_id)]['start_resume'])

async def finish_resume(call):
    chat_id = call.from_user.id
    session = get_session()
    finish_text = get_finish_text(chat_id)

    button_dict = {'Подтвердить и отправить 📨': 'send',
                   'Заполнить резюме заново 📝': 'refill'}
    await bot.delete_message(chat_id, session[str(chat_id)]['bot_message_id'])
    bot_message = await bot.send_message(chat_id, finish_text, reply_markup=create_keyboard_markup(button_dict))
    session[str(chat_id)]['bot_message_id'] = bot_message.id
    save_session(session)

async def send_email_andfinish_text(call):
    chat_id = call.from_user.id
    session = get_session()
    shablon = os.getenv('SHABLON')
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    dictonary, data, data1 = preparation_dictionaries(chat_id)
    subject = f"Претендент на работу {session[str(chat_id)]['answers']['full_name']}"
    body = f'Резюме поступающего на работу в АО "ОДК-Авиадвигатель"'

    create_docx(shablon, session[str(chat_id)]['answers']['full_name'], dictonary, data, data1)
    send_email(sender_email,sender_password,receiver_email, subject, body, session[str(chat_id)]['answers']['full_name']+'.docx')



@bot.message_handler(commands=['main'])
async def send_main(message):
    chat_id = message.from_user.id
    session = get_session()
    session[str(chat_id)]['current_question'] = 0
    save_session(session)
    button_dict = {
        'О нас': 'about_as',
        'Продолжить заполнять резюме': 'record_in_PD',
    }
    session = get_session()
    await bot.delete_message(chat_id, session[str(chat_id)]['bot_message_id'])
    await bot.delete_message(chat_id, message.id)
    bot_message = await bot.send_message(chat_id,'Начнем заново? 😊', reply_markup=create_keyboard_markup(button_dict))
    session[str(chat_id)]['bot_message_id'] = bot_message.id
    save_session(session)

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    chat_id = message.from_user.id
    print(str(chat_id) + " " + str(message.from_user.first_name))
    button_dict = {
        'О нас': 'about_as',
        'Запись в отдел кадров': 'record_in_PD',
    }
    keyboard = create_keyboard_markup(button_dict)
    if new_user_reg(message):
        bot_message = await bot.send_message(chat_id, 'С возвращением, ' + str(message.from_user.first_name) + '!', reply_markup=keyboard)
        session = get_session()
        session[str(chat_id)]['bot_message_id'] = bot_message.id
        save_session(session)
    else:
        bot_message = await bot.send_message(chat_id, 'Привет, рад познокомится, ' + str(message.from_user.first_name) + '!', reply_markup=keyboard)
        session = get_session()
        session[str(chat_id)]['bot_message_id'] = bot_message.id
        save_session(session)

    await bot.delete_message(chat_id, message.id)


@bot.callback_query_handler(func=lambda call: True)
async def handle_callback(call):
    time_limit = int(os.getenv('TIME_LIMIT'))
    chat_id = call.message.chat.id
    button_call = call.data
    session = get_session()
    if button_call == 'about_as':
        button_dict = {
            'На главную 🏠': 'main',
        }
        await bot.edit_message_text("Ознакомится можно по ссылке https://www.avid.ru/", chat_id, session[str(chat_id)]['bot_message_id'], reply_markup=create_keyboard_markup(button_dict))
    elif button_call == 'record_in_PD':
        button_dict = {
            'Заполнить резюме': 'start_resume',
            'На главную 🏠': 'main',
        }
        await bot.edit_message_text("Вы можете заполнить резюме, и вам перезвонит сотрудник отдела кадров.", chat_id, session[str(chat_id)]['bot_message_id'], reply_markup=create_keyboard_markup(button_dict))
    elif button_call =='start_resume':
        user_data.users[str(chat_id)]['start_resume'] = call
        session[str(chat_id)]['current_question'] +=1
        save_session(session)
        if session[str(chat_id)]['index_question'] == len(questions_list):
            await question_period_work_and_level_claims(call, 'work_experience', 'Сведения о работе за последние 10 лет')
        elif session[str(chat_id)]['index_question'] == len(questions_list)+1:
            await question_period_work_and_level_claims(call, 'level_of_claims', 'Уровень притязаний (Желаемая профессия и ЗП)')
        elif session[str(chat_id)]['index_question'] == len(questions_list)+2:
            await finish_resume(call)
        else:
            await response_handler(chat_id)
    elif button_call == 'next_question':
        session = get_session()
        session[str(chat_id)]['index_question'] += 1
        save_session(session)
        await handle_callback(user_data.users[str(chat_id)]['start_resume'])
    elif button_call == 'add_work':
        user_data.users[str(chat_id)]['add_work_call'] = call
        await four_question_work(call)
    elif button_call == 'main':
        session = get_session()
        session[str(chat_id)]['current_question'] = 0
        save_session(session)
        button_dict = {
            'О нас': 'about_as',
            'Продолжить заполнять резюме': 'record_in_PD',
        }
        await bot.edit_message_text('Начнем заново? 😊', chat_id, session[str(chat_id)]['bot_message_id'], reply_markup=create_keyboard_markup(button_dict))
    elif button_call == 'refill':
        session = get_session()
        session[str(chat_id)]['index_question'] = 0
        save_session(session)
        await handle_callback(user_data.users[str(chat_id)]['start_resume'])
    elif button_call =='send':
        if session[str(chat_id)]['count_send_resume'] == 0:
            print('Отправляем запрос')
            button_dict = {'На главную 🏠': 'main'}
            await bot.edit_message_text('Резюме отправлено, ожидайте звонка менеджера ☎', chat_id, session[str(chat_id)]['bot_message_id'], reply_markup=create_keyboard_markup(button_dict))
            await send_email_andfinish_text(call)
            current_time = datetime.now().time()
            session[str(chat_id)]['data_send_request'] = str(current_time)
            save_session(session)
        else:
            current_time = datetime.now().time()
        session = get_session()
        time_string = session[str(chat_id)]['data_send_request']
        time_string = datetime.strptime(time_string, "%H:%M:%S.%f").time()
        time_string = time_string.hour * 60 + time_string.minute
        current_minutes = current_time.hour * 60 + current_time.minute
        if session[str(chat_id)]['count_send_resume'] > 0:
            if current_minutes >= time_string + time_limit:
                current_time = datetime.now().time()
                session[str(chat_id)]['data_send_request'] = str(current_time)
                save_session(session)
                button_dict = {'На главную 🏠': 'main'}
                await bot.edit_message_text('Резюме отправлено, ожидайте звонка менеджера ☎', chat_id, session[str(chat_id)]['bot_message_id'], reply_markup=create_keyboard_markup(button_dict))
                await send_email_andfinish_text(call)
            else:
                button_dict = {'Назад 🔙': 'back'}
                await bot.edit_message_text('Отправлять резюме можно 1 раз в сутки\nВозвращайтесь завтра 😊', chat_id, session[str(chat_id)]['bot_message_id'], reply_markup=create_keyboard_markup(button_dict))

        else:
            session[str(chat_id)]['count_send_resume'] += 1
            save_session(session)
    elif button_call == 'back':
        await handle_callback(user_data.users[str(chat_id)]['start_resume'])
    else:
        await handle_callback_response(chat_id, call, button_call)


async def handle_reply_response(chat_id, message):
    session = get_session()
    try:
        session[str(chat_id)]['answers'][question_category[session[str(chat_id)]['index_question']]] = int(message.text)
    except:
        session[str(chat_id)]['answers'][question_category[session[str(chat_id)]['index_question']]] = message.text
    session[str(chat_id)]['index_question'] += 1
    save_session(session)
    await bot.delete_message(chat_id, message.id)
    await handle_callback(user_data.users[str(chat_id)]['start_resume'])

async def handle_reply_response_four(chat_id, message):
    session = get_session()
    value_q_work = session[str(chat_id)]['value_q_work']

    session[str(chat_id)]['answers']['work_experience'][value_q_work][work_experience_keys_list[session[str(chat_id)]['index_q_work']]] = message.text

    session[str(chat_id)]['index_q_work'] += 1
    save_session(session)
    await bot.delete_message(chat_id, message.id)
    if session[str(chat_id)]['index_q_work'] == len(work_experience_keys_list):
        session[str(chat_id)]['answers']['work_experience'].append({})
        session[str(chat_id)]['value_q_work'] += 1
        session[str(chat_id)]['index_q_work'] = 0
        save_session(session)
        await handle_callback(user_data.users[str(chat_id)]['start_resume'])
    else:
        await four_question_work(user_data.users[str(chat_id)]['add_work_call'])

async def handle_reply_response_three(chat_id, message):
    session = get_session()
    value_q_level = session[str(chat_id)]['value_q_level']

    session[str(chat_id)]['answers']['level_of_claims'][value_q_level][level_claims_keys_list[session[str(chat_id)]['index_q_level']]] = message.text

    session[str(chat_id)]['index_q_level'] += 1
    save_session(session)
    await bot.delete_message(chat_id, message.id)
    if session[str(chat_id)]['index_q_level'] == len(level_claims_keys_list):
        session[str(chat_id)]['answers']['level_of_claims'].append({})
        session[str(chat_id)]['value_q_level'] += 1
        session[str(chat_id)]['index_q_level'] = 0
        save_session(session)
        await handle_callback(user_data.users[str(chat_id)]['start_resume'])
    else:
        await four_question_work(user_data.users[str(chat_id)]['add_work_call'])


@bot.message_handler(func=lambda message: True)
async def handle_reply(message):
    chat_id = message.chat.id
    session = get_session()
    emoji_pattern = re.compile(r'[^\w\s,]')
    # Проверьте, есть ли смайлик в сообщении
    has_emoji = bool(emoji_pattern.search(message.text))
    if not has_emoji:
        if message.reply_to_message is not None:
            if session[str(chat_id)]['bot_message_id'] == message.reply_to_message.message_id:
                if message.reply_to_message.text in q_list_prov:
                    if session[str(chat_id)]['index_question'] == len(questions_list):
                        await handle_reply_response_four(chat_id, message)
                    elif session[str(chat_id)]['index_question'] == len(questions_list)+1:
                        await handle_reply_response_three(chat_id, message)
                    else:
                        await handle_reply_response(chat_id, message)
                else:
                    print('Error')
                    await bot.delete_message(chat_id, message.id)

            else:
                await bot.delete_message(chat_id, message.reply_to_message.id)
                await bot.delete_message(chat_id, message.id)

        else:
            if session[str(chat_id)]['current_question'] > 0:
                await bot.delete_message(chat_id, message.id)
                await handle_callback(user_data.users[str(chat_id)]['start_resume'])
            else:
                await send_main(message)

    else:
        await bot.delete_message(chat_id, message.id)
        await handle_callback(user_data.users[str(chat_id)]['start_resume'])



first_power()
asyncio.run(bot.polling())
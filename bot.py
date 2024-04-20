import telebot
import requests
from telebot import types
from typing import Dict
from dataclasses import dataclass

from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, Message, ForceReply


bot = telebot.TeleBot('Your token here')

buttons = [
    "JavaScript",
    "Golang",
    "Python",
    "Java",
    "Rust",
    "PHP",
    "Kotlin",
    "Swift",
    "C++",
    "C#",
    "SQL",
    "Unity",
    "Unreal Engine",
    ######
    "System Administrator",
    "Information Sequrity",
    "DevOps",
    "SRE",
    "QA",
    "Data Engineer",
    "Data Scientist",
    "Front End",
    "Back End"
]

keyboard = telebot.types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=False, selective=True)
for button_text in buttons:
    button = telebot.types.KeyboardButton(text=str(button_text))
    keyboard.add(button)


@bot.message_handler(func=lambda message: message.text in buttons)
def handle_button_press(message):
    chat_id = message.chat.id
    button = message.text

    url = f"https://api.hh.ru/vacancies?text=NAME:{button}\
            &per_page=10\
            &area=1\
            &order_by=publication_time\
            &only_with_salary=true"
    headers = {'User-Agent': 'Telegram Bot'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        vacancies = response.json()['items']
        vacancies = [d for d in vacancies if d.get('salary') is not None]

        print(vacancies)

        if not vacancies:
            bot.send_message(chat_id=chat_id, text='No vacancies found.')
            return

        vacancies_text = '\n'.join([
            f"• name: {vacancy['name']},\n\
            company: {vacancy['employer']['name']},\n\
            min: {vacancy['salary']['from']},\n\
            max: {vacancy['salary']['to']},\n\
            currency: {vacancy['salary']['currency']},\n\
            link: {vacancy['alternate_url']} \n \n"
            for vacancy in vacancies
        ])
        bot.send_message(chat_id=chat_id, text=vacancies_text)
    else:
        bot.send_message(
            chat_id=chat_id, text='Sorry, there was an error processing your request.')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, 'Please select a button: ', reply_markup=keyboard)


bot.polling()

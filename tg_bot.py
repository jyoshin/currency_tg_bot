from curses.ascii import isdigit
from locale import currency
from tabnanny import check
import telebot
from telebot import types
from datetime import datetime
import requests
from sys import exit
import json

bot = telebot.TeleBot("Telegram API")

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text="Enter currency code")

@bot.message_handler(content_types=['text'])
def answer(message):
    check = has_numbers(message.text)
    if check:
        bot.send_message(message.chat.id, "Try another code.")
    else:
        currency_data = apiCurrency(message.text.replace(" ", "").upper())
        if 'base_code' in currency_data:
            bot.send_message(message.chat.id, printCurrency(message.text.replace(" ", "").upper(), currency_data['conversion_rate']),parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, "Try another code.")

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def apiCurrency(user_reply):
    response = requests.get(
        url=f'https://v6.exchangerate-api.com/v6/API_KEY/pair/{user_reply}/KZT')
    data = response.json()
    return data

def printCurrency(user_reply, coin):
    return "<code>" + str(user_reply) + " to KZT is " + str(coin) + "</code>"

bot.polling()



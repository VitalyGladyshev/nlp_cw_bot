# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 14:32:54 2020

@author: viv232
"""

import telebot
from telebot import types
# import math

from geopy.distance import geodesic
from geopy.geocoders import Nominatim

SHOPS = ({
            'title': "Магнит на Астраханской",
            'latm': 48.595863,
            'lonm': 45.716521,
            'address': 'ул. Астраханская, 8Г, Знаменск, Астраханская обл., 416550'
         }, {
            'title': "Магнит на Янгеля",
            'latm': 48.588989,
            'lonm': 45.715826,
            'address': 'пр-кт 9 мая, 12, Знаменск, Астраханская обл., 416550'
        }, {
            'title': "Магнит на Ватутина",
            'latm': 48.581888,
            'lonm': 45.734980,
            'address': 'ул. Ватутина, Знаменск, Астраханская обл., 416540'
        }
)

API_TOKEN = '1394117290:AAEVn7j-CNn-rJ-9eHACgi3Qg8kv2hPp51g'
bot = telebot.TeleBot(API_TOKEN)
markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)   # row_width=3)
btn_address = types.KeyboardButton("Адреса магазинов", request_location=True)
btn_payment = types.KeyboardButton("Способы оплаты")
btn_delivery = types.KeyboardButton("Способы доставки")
markup_menu.add(btn_address, btn_payment, btn_delivery)


markup_inline_payment = types.InlineKeyboardMarkup()
btn_in_cash = types.InlineKeyboardButton('Наличные', callback_data='cash')
btn_in_card = types.InlineKeyboardButton('По карте', callback_data='card')
btn_in_invoice = types.InlineKeyboardButton('Банковский перевод',
                                            callback_data='invoice')
markup_inline_payment.add(btn_in_cash, btn_in_card, btn_in_invoice)

geolocator = Nominatim(user_agent=API_TOKEN)
location = geolocator.geocode("Астраханская 8 Знаменск")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Это бот для интернет магазина", reply_markup=markup_menu)


ban_list = [13, 345, 23, 5645]
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: message.from_user.id not in ban_list)
def echo_message(message):
    print(message)
    if message.text == "Способы доставки":
        bot.reply_to(message, 'Доставка курьером, самовывоз, почта России', reply_markup=markup_menu)
    elif message.text == "Способы оплаты":
        bot.reply_to(message,
                     'В наших магазинах доступны следующие способы оплаты',
                     reply_markup=markup_inline_payment)
    else:
        bot.reply_to(message, 'Ваше сообщение принял: ' + message.text.lower(), reply_markup=markup_menu)


@bot.message_handler(func=lambda message: True, content_types=['location'])
def shop_location(message):
    print(message)
    lon = message.location.longitude
    lat = message.location.latitude

    bot.reply_to(message, f'Ваши координаты - широта: {lat} долгота: {lon}', reply_markup=markup_menu)

    # delta = 999999
    # shop_ind = 0
    # for i in range(len(SHOPS)):
    #     dlt = math.sqrt(abs(SHOPS[i]['latm'] - lat)**2 + abs(SHOPS[i]['lonm'] - lon)**2)
    #     if dlt < delta:
    #         shop_ind = i

    distance = []
    for s in SHOPS:
        result = geodesic((s['latm'], s['lonm']), (lat, lon)).kilometers
        distance.append(result)
    index = distance.index(min(distance))

    bot.send_message(message.chat.id, 'Ближайший к вам магазин')
    bot.send_venue(message.chat.id,
                   SHOPS[index]['latm'],
                   SHOPS[index]['lonm'],
                   SHOPS[index]['title'],
                   SHOPS[index]['address'])


@bot.callback_query_handler(func=lambda call:True)
def call_back_paynment(call):
    print(call)
    if call.data == 'cash':
        bot.send_message(call.message.chat.id, text="""
                Наличная оплата производитс в рублях на кассе магазина
                """, reply_markup=markup_inline_payment)


def main():
    """Start the bot."""
    bot.polling()


if __name__ == '__main__':
    main()

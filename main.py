# -*- coding: utf-8 -*-
import telebot
import json

from telebot import types
from model.Certificado import Certificado
from utils.DesenhaCertificado import DesenhaCertificado

API_TOKEN = '5253038403:AAFrAushkt62eL55Utvh7s2pGzBLWgq4L48'

password_app = "6969xxx"

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    print(message)
    msg = bot.reply_to(message, f"""\
        Olá! {message.chat.first_name} quer criar um certificado ?
    digite sua senha antes de tudo
    """)
    bot.register_next_step_handler(msg, process_password_compare_step)


def process_password_compare_step(message):
    try:
        chat_id = message.chat.id
        password = message.text
        if password_app == password:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('2016', '2017', '2018', '2019', '2020', '2021', '2022')
            msg = bot.send_message(chat_id, 'Qual o ano do certificado', reply_markup=markup)
            bot.register_next_step_handler(msg, process_year_step)
        else:
            bot.send_message(chat_id, 'Você é um forateiro! caso não seja clique aqui => /start')

    except Exception as e:
        bot.reply_to(message, 'oooops! deu ruim refaça tudo amigo! clicando aqui => /start')


def process_year_step(message):
    try:
        chat_id = message.chat.id
        ano = message.text
        user = Certificado(ano=ano)
        user_dict[chat_id] = user
        msg = bot.send_message(chat_id, 'Agora digite o nome da empresa')
        bot.register_next_step_handler(msg, process_company_step)
    except Exception as e:
        bot.reply_to(message, 'oooops! deu ruim refaça tudo amigo! clicando aqui => /start')


def process_company_step(message):
    try:
        chat_id = message.chat.id
        nome_fantasia = message.text
        user = user_dict[chat_id]
        user.nome_fantasia = nome_fantasia
        msg = bot.send_message(chat_id, 'Agora digite o segmento?')
        bot.register_next_step_handler(msg, process_segment_step)
    except Exception as e:
        bot.reply_to(message, 'oooops! deu ruim refaça tudo amigo! clicando aqui => /start')


def process_segment_step(message):
    try:
        chat_id = message.chat.id
        segmento = message.text

        user = user_dict[chat_id]
        user.segmento = segmento

        msg = bot.send_message(chat_id, 'Agora digite o nome da cidade')
        bot.register_next_step_handler(msg, process_city_step)
    except Exception as e:
        bot.reply_to(message, 'oooops! deu ruim refaça tudo amigo! clicando aqui => /start')


def process_city_step(message):
    try:
        chat_id = message.chat.id
        cidade = message.text
        user = user_dict[chat_id]
        user.cidade = cidade

        msg = bot.send_message(chat_id, 'Agora digite o UF da cidade exemplo => BA, AL, PI')
        bot.register_next_step_handler(msg, process_uf_step)

    except Exception as e:
        bot.reply_to(message, 'oooops! deu ruim refaça tudo amigo! clicando aqui => /start')


def process_uf_step(message):
    try:
        chat_id = message.chat.id
        uf = message.text
        user = user_dict[chat_id]
        user.uf = uf

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('refazer', 'ok!')
        msg = bot.send_message(chat_id, 'Confira as informações: \n '
                                        'Empresa: ' + user.nome_fantasia +
                               '\n segmento: ' + str(user.segmento) +
                               '\n Cidade: ' + user.cidade +
                               '\n Uf: ' + user.uf +
                               '\n Ano do certificado: ' + user.ano,
                               reply_markup=markup
                               )

        bot.register_next_step_handler(msg, process_certificado_step)

    except Exception as e:
        bot.reply_to(message, 'oooops! deu ruim refaça tudo amigo! clicando aqui => /start')


def __config_cert() -> list:
    with open('./utils/config_cert.json') as config_json:
        config_certificado = json.load(config_json)
        return config_certificado


def process_certificado_step(message):
    try:
        chat_id = message.chat.id
        opcao_user = message.text
        user = user_dict[chat_id]

        if opcao_user == u'refazer':
            bot.send_message(chat_id, 'Clique aqui ==> /start para refazer')
        else:
            draw = DesenhaCertificado(user, __config_cert())
            photo = draw.criar_certificado()
            if photo:
                print(photo)
                bot.send_message(chat_id, 'Aguarde...')
                bot.send_photo(chat_id, photo)

    except Exception as e:
        bot.reply_to(message, 'oooops! deu ruim refaça tudo amigo! clicando aqui => /start')


bot.infinity_polling()

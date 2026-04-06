import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from wakeonlan import send_magic_packet

TOKEN = os.environ.get("8707667278:AAHcOq3prZF0p8sH6WN4AIbikyfE7V6acbc")
MAC = "AA:1C:04:19:6B:A2"
PC_IP = "93.124.48.99"
bot = telebot.TeleBot(TOKEN)

def menu():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("⚡️ Включить ПК", callback_data="wake"))
    markup.row(InlineKeyboardButton("⏻ Выключить ПК", callback_data="off"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    bot.send_message(
        message.chat.id,
        "🖥 *Управление ПК*\nВыбери действие:",
        parse_mode="Markdown",
        reply_markup=menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "wake":
        send_magic_packet(MAC, ip_address=PC_IP, port=9)
        bot.answer_callback_query(call.id, "✅ ПК включается!")
        bot.edit_message_text(
            "🖥 *Управление ПК*\n\n✅ Magic packet отправлен!\nПК включается...",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=menu()
        )
    elif call.data == "off":
        bot.answer_callback_query(call.id, "⏻ Выключаю...")
        bot.edit_message_text(
            "🖥 *Управление ПК*\n\n⏻ Команда на выключение отправлена...",
            call.message.chat.id,
            call.message.message_id,
            parse_mode="Markdown",
            reply_markup=menu()
        )

bot.polling()

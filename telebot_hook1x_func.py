# singirella telegram bot handler functions
import telebot
import pymysql
import time
from telebot import types

# cunstruct keyboard sets for a user message, input is like ('Concert', '/event', 'Help me', '/help', 'Call!', '/manager')
def inline_button_constructor(my_tuple):
    my_tuple = tuple(my_tuple.split(', '))
    tuple_len = len(my_tuple)
    keys = types.InlineKeyboardMarkup()
    buttons = []
    for i in range(0, tuple_len, 2):
        buttons.append(
            types.InlineKeyboardButton(my_tuple[i], callback_data=my_tuple[i + 1])
        )
    keys.add(*buttons)
    return keys
    
# send scheduled message with image and keyboard
def send_notification(bot, chat_id, photo_path, message, ukeys):
    try:
        with open(photo_path, 'rb') as photo:
            bot.send_photo(chat_id, photo)
        if ukeys == "None":
            bot.send_message(chat_id, message)
        else:
            bot.send_message(chat_id, message, reply_markup=inline_button_constructor(ukeys))
        time.sleep(1)
    except telebot.apihelper.ApiTelegramException as e:
        if e.result.status_code == 403:
            if "Forbidden: bot was blocked by the user" in str(e):
                print(f"User with chat_id {chat_id} has blocked the bot")
            else:
                print(f"A 403 error occurred for chat_id {chat_id}: {str(e)}")

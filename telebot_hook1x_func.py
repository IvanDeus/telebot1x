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

# fetch all config vars defined in mysql
def fetch_telebot_vars_into_dict(conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT param, value FROM telebot_vars"
            cursor.execute(query)
            result = cursor.fetchall()

            telebot_vars = {}  # Initialize an empty dictionary

            for row in result:
                param, value = row
                telebot_vars[param] = value  # Add data to the dictionary

            return telebot_vars

    except pymysql.Error as e:
        # Handle any database errors here
        print(f"Database error: {e}")
        return {}

# get all variables for admin page
def get_vars_table(conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM telebot_vars Order by param"
            cursor.execute(query)
            results = cursor.fetchall()
        return results
    except Exception as e:
        # Handle any exceptions (e.g., database connection error)
        print(f"Error: {e}")
        return []

# set variables for admin page
def set_vars_table(conn, id_v, value_v):
    try:
        with conn.cursor() as cursor:
            query = "Update telebot_vars set value = %s Where id = %s "
            cursor.execute(query, (value_v, id_v))
            conn.commit()
    except pymysql.Error as e:
        # Handle any database errors here
        print(f"Database error: {e}")

# get all scheduled tasks for admin page
def get_scheduled_table(conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM telebot_sched Order by id"
            cursor.execute(query)
            results = cursor.fetchall()
        return results
    except Exception as e:
        # Handle any exceptions (e.g., database connection error)
        print(f"Error: {e}")
        return []

# set schedule for admin page
def set_scheduled_table(conn, id_v, t_out, simg, message, ukeys):
    try:
        with conn.cursor() as cursor:
            query = "Update telebot_sched set t_out = %s, simg = %s, message = %s, ukeys = %s Where id = %s "
            cursor.execute(query, (t_out, simg, messenge, ukeys, id_v))
            conn.commit()
    except pymysql.Error as e:
        # Handle any database errors here
        print(f"Database error: {e}")


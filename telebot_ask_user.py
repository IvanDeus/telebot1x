# bot, after some time ask user if he likes the first message, put it in crontab!
# */10 * * * * python telebot_ask_user.py > /dev/null
import pymysql
from datetime import datetime, timedelta
import requests
import time
import telebot
from telebot import types
# Config import
from telebot_hook1x_cfg import bot_token, db_host, db_username, db_password, db_name, mysql_unix_socket
from telebot_hook1x_func import *
# my path
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
# Initialize the telebot
bot = telebot.TeleBot(bot_token)
conn = pymysql.connect(unix_socket=mysql_unix_socket, user=db_username, password=db_password, database=db_name)
#### event scheduler
sched_events = get_scheduled_table(conn, 1)
current_datetime = datetime.now()
telebot_vars = fetch_telebot_vars_into_dict(conn)
# main logic, loop thru events, then users who needs notifying
for idx, event in enumerate(sched_events):
    event_id, minutes_until_event, img, message, ukeys, event_date, ev_id = event
    users_to_notify = get_users_to_notify(conn, minutes_until_event, event_id)
    # Check if it's the last event
    is_last_event = idx == len(sched_events) - 1
    for user in users_to_notify:
        chat_id = user[0]
        photo_path = script_directory + '/singirella-files/' + img
        message1 = message
        send_notification(bot, chat_id, photo_path, message1, ukeys)
        change_step_status(chat_id, conn, event_id + 1)
        if is_last_event: # set feedback mode for last step
            change_step_status(chat_id, conn, 111)
# Get users with expired feedback mode
users_to_notify = get_users_to_notify(conn, 48, 111)
for user in users_to_notify:
    chat_id = user[0]
    change_step_status(chat_id, conn, 0)
# Close the database connection
if conn:
    conn.close()
##end

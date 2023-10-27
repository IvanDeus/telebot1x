# telegram bot functions by Ivan Deus
import telebot
import pymysql
import time
from datetime import datetime, timedelta
from telebot import types

# Function to retrieve admin chat ID and hashed password from the database
def find_admin_chatid_and_password(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id, passwd FROM telebot_admins WHERE name = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        admin_chatid, hashed_db_password = result
        return admin_chatid, hashed_db_password
    return None, None

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
        time.sleep(0.5)
    except telebot.apihelper.ApiTelegramException as e:
        if e.result.status_code == 403:
            if "Forbidden: bot was blocked by the user" in str(e):
                print(f"User with chat_id {chat_id} has blocked the bot")
            else:
                print(f"A 403 error occurred for chat_id {chat_id}: {str(e)}")
# one-time mass message to all subbed users
def massmessage(conn, message, bot):
    user_chat_ids = find_subbed_chatids(conn)
    sent_messages = []
    error_messages = []

    for chat_id in user_chat_ids:
        try:
            # Send a message
            bot.send_message(chat_id, message)
            sent_messages.append(f"Sent to: {chat_id}")
            time.sleep(0.5)
        except telebot.apihelper.ApiTelegramException as e:
            if e.result.status_code == 403:
                if "Forbidden: bot was blocked by the user" in str(e):
                    error_messages.append(f"User with chat_id {chat_id} has blocked the bot")
                else:
                    error_messages.append(f"A 403 error occurred for chat_id {chat_id}: {str(e)}")

    return sent_messages, error_messages


# get all scheduled tasks for admin page
def get_scheduled_table(conn, ev_id):
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM telebot_sched Where ev_id = %s Order by id"
            cursor.execute(query, (ev_id))
            results = cursor.fetchall()
        return results
    except Exception as e:
        # Handle any exceptions (e.g., database connection error)
        print(f"Error: {e}")
        return []

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
# get users for scheduler
def get_users_to_notify(conn, hours, step):
    twenty_four_hours_ago = datetime.now() - timedelta(hours=hours)
    twenty_four_hours_ago_str = twenty_four_hours_ago.strftime('%Y-%m-%d %H:%M:%S')
    with conn.cursor() as cursor:
        query = f"SELECT chat_id, first_name FROM telebot_users WHERE lastupd < '{twenty_four_hours_ago_str}' AND step = '{step}' AND Sub = 1"
        cursor.execute(query)
        results = cursor.fetchall()

    return results

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

# set schedule for admin page
def set_scheduled_table(conn, id_v, t_out, simg, message, ukeys, event_date, ev_id):
    try:
        with conn.cursor() as cursor:
            query = "Update telebot_sched set t_out = %s, simg = %s, message = %s, ukeys = %s, event_date = %s, ev_id = %s  Where id = %s "
            cursor.execute(query, (t_out, simg, message, ukeys, event_date, ev_id, id_v))
            conn.commit()
    except pymysql.Error as e:
        # Handle any database errors
        print(f"Database error: {e}")

# change subscription status
def change_sub_status(chat_id, conn, sub):
    try:
        with conn.cursor() as cursor:
            # Use parameterized query to update the subscription status
            query = "UPDATE telebot_users SET Sub = %s WHERE chat_id = %s"
            cursor.execute(query, (sub, chat_id))
            # Commit the changes to the database
            conn.commit()

    except pymysql.Error as e:
        # Handle any database errors here
        print(f"Database error: {e}")

# Function to find all subscribed chat IDs
def find_subbed_chatids(conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT chat_id FROM telebot_users WHERE Sub = 1"
            cursor.execute(query)
            results = cursor.fetchall()  # Fetch all matching chat IDs
            if results:
                return [result[0] for result in results]  # Return a list of chat IDs
            else:
                return []  # Return an empty list if no subscribed users found
    except Exception as e:
        # Handle any exceptions (e.g., database connection error)
        print(f"Error: {e}")
        return []

def change_step_status(chat_id, conn, stp):
    try:
        with conn.cursor() as cursor:
            # Use parameterized query to update the subscription status
            query = "UPDATE telebot_users SET step = %s WHERE chat_id = %s"
            cursor.execute(query, (stp, chat_id))
            # Commit the changes to the database
            conn.commit()
    except pymysql.Error as e:
        # Handle any database errors here
        print(f"Database error: {e}")

def get_manager_chat_id(conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT chat_id FROM telebot_admins WHERE chatmngr = 1 LIMIT 1"
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]  # Return the chat_id if found
            else:
                return None  # Return None if admin user not found
    except Exception as e:
        # Handle any exceptions (e.g., database connection error)
        print(f"Error: {e}")
        return None

# write user chats into table
def update_chat_table(conn, uchat_id, mngmsg):
    try:
        with conn.cursor() as cursor:
            mngmsg = conn.escape_string(mngmsg)
             # Check if the user already exists in the table
            query = f"SELECT id FROM telebot_chats WHERE uchat_id = '{uchat_id}' ORDER BY lastupd DESC LIMIT 1"
            cursor.execute(query)
            result_id = cursor.fetchone()
              # Proceed to update
            if result_id:
               mngmsg = " : "+mngmsg
             # User exists, update the record
               update_query = "UPDATE telebot_chats SET mngmsg = CONCAT(mngmsg, %s) WHERE id = %s"
               cursor.execute(update_query, (mngmsg, result_id[0]))
               conn.commit()
            else:
               print("no chat was found by manager")

    except pymysql.Error as e:
        # Handle any database errors here
        print(f"Database error: {e}")

def insert_into_chat_table(conn, uchat_id, mngchat_id, umsg, mngmsg):
    try:
        with conn.cursor() as cursor:
            # Use parameterized query to update the subscription status
            query = "Insert Into telebot_chats SET uchat_id = %s, mngchat_id = %s, umsg = %s, mngmsg = %s"
            cursor.execute(query, (uchat_id, mngchat_id, umsg, mngmsg))
            # Commit the changes to the database
            conn.commit()
    except pymysql.Error as e:
        # Handle any database errors here
        print(f"Database error: {e}")
        
# set the number of messages in a scheduler
def update_sched_message_nmbr(connection, x, y):
    try:
        with connection.cursor() as cursor:
          # Update rows where id is greater than x and less than or equal to y
            update_sql = "UPDATE telebot_sched SET ev_id = 99 WHERE id > %s AND id <= %s"
            cursor.execute(update_sql, (x, y))
        # Update rows where id is less than or equal to x
            update_sql = "UPDATE telebot_sched SET ev_id = 1 WHERE id <= %s"
            cursor.execute(update_sql, x)
            connection.commit()
    except pymysql.Error as e:
        # Handle any database errors here
        print(f"Database error: {e}")

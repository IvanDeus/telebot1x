# Telebot1x v2...
import telebot
from telebot import types
import pymysql
from datetime import datetime
import time

# Config import
from telebot_hook1x_cfg import bot_token, admin_name, db_host, db_username, db_password, db_name, mysql_unix_socket, imgtosend, pdftosend

# Initialize the bot
bot = telebot.TeleBot(bot_token)

# Function to add or update a user in the 'telebot_users' table
def add_or_update_user(chat_id, name, message, conn, first_name, last_name):
    try:
        with conn.cursor() as cursor:
            # Convert chat_id to a string and then escape it to prevent SQL injection
            chat_id_str = conn.escape_string(str(chat_id))
            name = conn.escape_string(name)
            message = conn.escape_string(message)
            first_name = conn.escape_string(first_name)
            last_name = conn.escape_string(last_name)

            # Check if the user already exists in the table
            query = f"SELECT * FROM telebot_users WHERE chat_id = '{chat_id_str}'"
            cursor.execute(query)

            if cursor.rowcount > 0:
                # User exists, update the record
                current_time = conn.escape_string(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                update_query = f"UPDATE telebot_users SET lastupd = '{current_time}', lastmsg = '{message}' WHERE chat_id = '{chat_id_str}'"
                cursor.execute(update_query)
            else:
                # User does not exist, insert a new record
                current_time = conn.escape_string(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                insert_query = f"INSERT INTO telebot_users (chat_id, name, lastupd, lastmsg, first_name, last_name) VALUES ('{chat_id_str}', '{name}', '{current_time}', '{message}', '{first_name}', '{last_name}')"
                cursor.execute(insert_query)

            # Commit the changes to the database
            conn.commit()

    except pymysql.Error as e:
        # Handle any database errors here
        print(f"Database error: {e}")

# Function to get the last 24 rows with the most recent timestamps
def get_last_24_users(conn):
    # Query to retrieve the last 24 rows with the most recent timestamps
    query = "SELECT * FROM telebot_users ORDER BY lastupd DESC LIMIT 24"

    with conn.cursor() as cursor:
        # Execute the query
        cursor.execute(query)

        # Fetch all rows as a list of tuples
        users = cursor.fetchall()

    return users

def change_sub_status(chat_id, conn, sub):
    try:
        with conn.cursor() as cursor:
            # Use a parameterized query to update the subscription status
            query = "UPDATE telebot_users SET Sub = %s WHERE chat_id = %s"
            cursor.execute(query, (sub, chat_id))
            # Commit the changes to the database
            conn.commit()

    except pymysql.Error as e:
        # Handle any database errors here
        print(f"Database error: {e}")

# Function to handle the '/stat24' command
def handle_stat24_command(chat_id, conn):
    message_lastu = ''
    last_24_users = get_last_24_users(conn)
    # Loop through the last_24_users list of tuples
    for user_data in last_24_users:
        # Access each element in the tuple by index
        id, chat_id2, name, lastupd, lastmsg = user_data

        # Work with each variable as needed
        message_lastu += f"ID: {id}\n"
        message_lastu += f"Chat ID: {chat_id2}\n"
        message_lastu += f"Name: {name}\n"
        message_lastu += f"Last Update: {lastupd}\n"
        message_lastu += f"Last Message: {lastmsg}\n"
        message_lastu += "\n"
    # Send the message to the Telegram bot
    bot.send_message(chat_id, message_lastu)

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

# Function to handle incoming Telegram updates
@bot.message_handler(func=lambda message: True)
def handle_telegram_update(message):
    # Define global variables
    global imgtosend
    global pdftosend
    global admin_name

    chat_id = message.chat.id
    name = message.chat.username

    if message.text:
        message_text = message.text

        # Create a custom keyboard markup
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_button = types.KeyboardButton('/start')
        help_button = types.KeyboardButton('/help')
        guide_button = types.KeyboardButton('/guide')
        markup.row(start_button, help_button, guide_button)

        # Check the message text for specific commands or keywords
        if '/start' in message_text:
            # Send the image right after the welcome message
            send_image(chat_id, 'telebot-h-files/' + imgtosend, 'image/jpeg', imgtosend)

            # Handle the /start command
            bot.send_message(chat_id, 'Ivan Deus bot welcomes you! Type /guide or /help for all available commands', reply_markup=markup)

        elif '/sub' in message_text:
            sub = 1
            change_sub_status(chat_id, conn, sub)
            bot.send_message(chat_id, "You have subscribed", reply_markup=markup)

        elif '/unsub' in message_text:
            sub = 0
            change_sub_status(chat_id, conn, sub)
            bot.send_message(chat_id, "You unsubscribed", reply_markup=markup)

        elif '/forward' in message_text:
            # Find all subscribed chat IDs
            subscribed_chat_ids = find_subbed_chatids(conn)
            message_text = message_text[len('/forward '):]  # cut the command forward
            # Loop through the subscribed chat IDs and send the message
            for chat_id in subscribed_chat_ids:
                bot.send_message(chat_id, message_text)
                time.sleep(1)  # Add a delay

        elif '/help' in message_text:
            # Handle the /help command
            bot.send_message(chat_id, 'This is a help message. You can subscribe with /sub and unsubscribe with /unsub', reply_markup=markup)

        elif '/guide' in message_text:
            # Handle the /guide command to send a PDF file
            send_file(chat_id, 'telebot-h-files/' + pdftosend, 'application/pdf', pdftosend, reply_markup=markup)

        elif '/stat24' in message_text and name == admin_name:
            handle_stat24_command(chat_id, conn)

        else:
            # Handle other user input as needed
            bot.send_message(chat_id, "I do not understand. Type /help for assistance", reply_markup=markup)

    else:
        # Handle non-text messages (e.g., stickers)
        print(f"Received a non-text message")

# Function to send an image to the Telegram bot
def send_image(chat_id, file_path, file_type, file_name):
    try:
        with open(file_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=file_name)
    except Exception as e:
        # Handle any exceptions
        print(f"Error sending image to Telegram: {e}")

# Function to send a file to the Telegram bot
def send_file(chat_id, file_path, file_type, file_name):
    try:
        with open(file_path, 'rb') as document:
            bot.send_document(chat_id, document, caption=file_name)
    except Exception as e:
        # Handle any exceptions
        print(f"Error sending file to Telegram: {e}")

# Telegram bot polling
if __name__ == '__main__':
    # Create a database connection with Unix socket
    conn = pymysql.connect(unix_socket=mysql_unix_socket, user=db_username, password=db_password, database=db_name)

    # Start the bot polling
    bot.polling(none_stop=True)

    # Close the database connection when the bot is stopped
    conn.close()

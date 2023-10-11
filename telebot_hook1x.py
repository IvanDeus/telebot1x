## telegram bot
from flask import Flask, request, jsonify, render_template
import json
import requests
import pymysql
import time
import telebot
from telebot import types

app = Flask(__name__)
# Config import
from telebot_hook1x_cfg import bot_token, admin_name, db_host, db_username, db_password, db_name, mysql_unix_socket, imgtosend, pdftosend

# Initialize the telebot
bot = telebot.TeleBot(bot_token)

# ... Code begins

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
                update_query = f"UPDATE telebot_users SET lastmsg = '{message}' WHERE chat_id = '{chat_id_str}'"
                cursor.execute(update_query)
            else:
                # User does not exist, insert a new record
                insert_query = f"INSERT INTO telebot_users (chat_id, name, lastmsg, first_name, last_name) VALUES ('{chat_id_str}', '{name}', '{message}', '{first_name}', '{last_name}')"
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
            # Use parameterized query to update the subscription status
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
            id = user_data[0]
            chat_id2 = user_data[1]
            name = user_data[2]
            lastupd = user_data[3]
            lastmsg = user_data[4]
            fname = user_data[6]
            lname = user_data[7]
            step = user_data[5]

            # Work with each variable as needed
            message_lastu += f"ID: {id}\n"
            message_lastu += f"Chat ID: {chat_id2}\n"
            message_lastu += f"Name: {name}\n"
            message_lastu += f"Last Update: {lastupd}\n"
            message_lastu += f"Last Message: {lastmsg}\n"
            message_lastu += f"First name: {fname}\n"
            message_lastu += f"Last name: {lname}\n"
            message_lastu += f"Step: {step}\n"
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


@bot.message_handler()
def handle_nostart(message):
    chat_id = message.chat.id
    msg1 = ("I do not understand. Press 'help' for assistance. ")
    # Create an inline keyboard
    keyboard = types.InlineKeyboardMarkup()
    button2 = types.InlineKeyboardButton('Help', callback_data='/help')
    keyboard.add(button2)
    bot.send_message(chat_id, msg1, reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    msg1 = ("Ivan Deus bot welcomes you! "
            "To get file press 'guide' or press 'help' for all available commands")
    # Create an inline keyboard
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Guide', callback_data='/guide')
    button2 = types.InlineKeyboardButton('Help', callback_data='/help')
    # Add the buttons to the keyboard
    keyboard.add(button1, button2)
    ##send_image()
    with open('telebot-h-files/' + imgtosend, 'rb') as photo:
        bot.send_photo(chat_id, photo)
    # Send a message with the inline keyboard
    bot.send_message(chat_id, msg1, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call, conn):
    keyboard2 = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Guide', callback_data='/guide')
    button3 = types.InlineKeyboardButton('Sub', callback_data='/sub')
    button4 = types.InlineKeyboardButton('Unsub', callback_data='/unsub')
    # Add the buttons to the keyboard
    keyboard2.add(button1, button3, button4)

    # Handle button presses
    chat_id = call.message.chat.id
    data = call.data
    msg1 = ("Super guide! Enjoy!")
    msg2 = ("This is a help message. Try /start or 'guide'. "
            "You can subscribe with 'sub' and undo with 'unsub'")

    if data == '/guide':
         # Handle the /guide command to send a PDF file
        with open('telebot-h-files/' + pdftosend, 'rb') as pdf_file:
           bot.send_document(chat_id, pdf_file, caption=msg1)
        add_or_update_user(chat_id, ' ', data, conn, ' ', ' ')
    elif data == '/help':
        bot.send_message(chat_id, msg2, reply_markup=keyboard2)
        add_or_update_user(chat_id, ' ', data, conn, ' ', ' ')
    elif data == '/sub':
        sub = 1
        change_sub_status(chat_id, conn, sub)
        bot.send_message(chat_id, "You have subscribed")
    elif data == '/unsub':
        sub = 0
        change_sub_status(chat_id, conn, sub)
        bot.send_message(chat_id, "You unsubscribed")


# Telegram bot
@app.route('/')
def hello():
    return render_template('hello.html')


# Main logic
@app.route('/telebot-hook1x', methods=['POST'])
def telebothook1x():
    try:
        # Create a database connection with Unix socket
        conn = pymysql.connect(unix_socket=mysql_unix_socket, user=db_username, password=db_password, database=db_name)

        #VERS 2 Get update array
        json_string = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_string)
        # Analyze recived message
        ##print (update.message)
        if (update.message is not None) and (update.message.text is not None):
            message = update.message
            # Access name and chat_id only when there is a message
            name = message.chat.username
            # find first name
            first_name = message.chat.first_name
            if message.chat.last_name:
                last_name = message.chat.last_name
            else:
                last_name = ' '
            # get chat id
            chat_id = message.chat.id
             # Call your add_or_update_user function to add/update the user in the database
            add_or_update_user(chat_id, name, message.text, conn, first_name, last_name)
            # Handle start command
            if message.text == '/start':
                handle_start(message)
            # handle admin commands
            elif '/stat24' in message.text and name == admin_name:
                handle_stat24_command(chat_id, conn)
            elif '/forward' in message.text and name == admin_name:
                 # Find all subscribed chat IDs
                subscribed_chat_ids = find_subbed_chatids(conn)
                message_text = message.text[len('/forward '):] #cut command forward
                if message_text: 
                    # Loop through the subscribed chat IDs and send the message
                   for uchat_id in subscribed_chat_ids:
                       bot.send_message(uchat_id, message_text)
                       time.sleep(1)  # Add a delay
            else:
                handle_nostart(message) # all others imput

        elif update.callback_query is not None:
            call = update.callback_query
            handle_callback(call, conn)  # Call the function to handle the callback query

    except pymysql.Error as e:
        print(f"Database error: {e}")
        return jsonify(error="Database error")

    finally:
        # Close the database connection
        if conn:
            conn.close()

    # If there's no message to handle, return an empty response
    return '', 204  # HTTP 204 No Content

if __name__ == '__main__':
    # Change the host and port here
    app.run(port=1500)

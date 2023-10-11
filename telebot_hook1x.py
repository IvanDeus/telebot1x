## telegram bot
from flask import Flask, request, jsonify, render_template
import json
import requests
import pymysql
import time
import telebot

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
def handle_stat24_command(chat_id, bot_token, conn):
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
def handle_telegram_update(update_data, bot_token, conn):
    # Define global variables
    global imgtosend
    global pdftosend
    global admin_name

    if 'message' in update_data:
        message_data = update_data['message']
        chat_id = message_data['chat']['id']
        name = message_data['chat']['username']

        if 'text' in message_data:
            message_text = message_data['text']

            # Check the message text for specific commands or keywords
            if '/start' in message_text:
                # Send the image as the welcome message
                ##send_image(chat_id, 'telebot-h-files/' + imgtosend, 'image/jpeg', imgtosend, bot_token)
                with open('telebot-h-files/' + imgtosend, 'rb') as photo:
                    bot.send_photo(chat_id, photo)
                # Handle the /start command
                bot.send_message(chat_id, 'Ivan Deus bot welcomes you! Type /guide or /help for all available commands')

            elif '/sub' in message_text:
                 sub = 1
                 change_sub_status(chat_id, conn, sub)
                 bot.send_message(chat_id, "You have subscribed")
            elif '/unsub' in message_text:
                 sub = 0
                 change_sub_status(chat_id, conn, sub)
                 bot.send_message(chat_id, "You unsubscribed")
            elif '/forward' in message_text:
                 # Find all subscribed chat IDs
                 subscribed_chat_ids = find_subbed_chatids(conn)
                 message_text = message_text[len('/forward '):] #cut command forward
                 # Loop through the subscribed chat IDs and send the message
                 for chat_id in subscribed_chat_ids:
                     bot.send_message(chat_id, message_text)
                     time.sleep(1)  # Add a delay

            elif '/help' in message_text:
                # Handle the /help command
                bot.send_message(chat_id, 'This is a help message. Try /start or /guide. You can subscribe with /sub and undo with /unsub')
            elif '/guide' in message_text:
                # Handle the /guide command to send a PDF file
                with open('telebot-h-files/' + pdftosend, 'rb') as pdf_file:
                    bot.send_document(chat_id, pdf_file, caption="An epic guide for you")

            elif '/stat24' in message_text and name == admin_name:
                handle_stat24_command(chat_id, bot_token, conn)
            else:
                # Handle other user input as needed
                bot.send_message(chat_id, "I do not understand. Type /help for assistance.")
        else:
            # Handle non-text messages (e.g., stickers)
            print(f"Received a non-text message")

    elif 'edited_message' in update_data:
        # Handle edited messages if needed
        pass

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

        # Read post input
        update_data = request.get_json()
        # Debug: Print the received update_data
        ##print("Received update_data:", update_data)
        if 'message' in update_data:
            if 'text' in update_data['message']:
               message = update_data['message']['text']
            else:
               message = " "
        elif 'edited_message'  in update_data:
            message = update_data['edited_message']
        else:
            message = " "

        name = update_data['message']['chat']['username']
        chat_id = update_data['message']['chat']['id']


        first_name = update_data['message']['chat']['first_name']
        if 'last_name' in update_data['message']['chat']:
            last_name = update_data['message']['chat']['last_name']
        else:
            last_name = " "

        # Call your add_or_update_user function to add/update the user in the database
        add_or_update_user(chat_id, name, message, conn, first_name, last_name)

        handle_telegram_update(update_data, bot_token, conn)
        # Return a JSON response
        return jsonify(message)

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

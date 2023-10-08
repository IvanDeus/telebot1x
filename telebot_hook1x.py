from flask import Flask, request, jsonify
import json
import requests
import pymysql
from datetime import datetime

app = Flask(__name__)
# Config import
from telebot_hook1x_cfg import bot_token, admin_name, db_host, db_username, db_password, db_name, mysql_unix_socket, imgtosend, pdftosend

# ... Code begins

# Function to add or update a user in the 'telebot_users' table
def add_or_update_user(chat_id, name, message, conn):
    try:
        with conn.cursor() as cursor:
            # Convert chat_id to a string and then escape it to prevent SQL injection
            chat_id_str = conn.escape_string(str(chat_id))
            name = conn.escape_string(name)
            message = conn.escape_string(message)

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
                insert_query = f"INSERT INTO telebot_users (chat_id, name, lastupd, lastmsg) VALUES ('{chat_id_str}', '{name}', '{current_time}', '{message}')"
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
    send_telegram_message(chat_id, message_lastu, bot_token)

# Function to handle incoming Telegram updates
def handle_telegram_update(update_data, bot_token, conn):
    # Define global variables
    global imgtosend
    global pdftosend
    global admin_name
    
    if 'message' in update_data:
        chat_id = update_data['message']['chat']['id']
        name = update_data['message']['chat']['username']
        message_text = update_data['message']['text']

        # Check the message text for specific commands or keywords
        if '/start' in message_text:
            # Send the image right after the welcome message
            send_image(chat_id, 'telebot-h-files/' + imgtosend, 'image/jpeg', imgtosend, bot_token)

            # Handle the /start command
            send_telegram_message(chat_id, 'Ivan Deus bot welcomes you! Type /guide or /help for all available commands', bot_token)
        elif '/help' in message_text:
            # Handle the /help command
            send_telegram_message(chat_id, 'This is a help message. Try /start or /guide', bot_token)
        elif '/guide' in message_text:
            # Handle the /guide command to send a PDF file
            send_file(chat_id, 'telebot-h-files/' + pdftosend, 'application/pdf', pdftosend, bot_token)
        elif '/stat24' in message_text and name == admin_name:
            handle_stat24_command(chat_id, bot_token, conn)
        else:
            # Handle other user input as needed
            send_telegram_message(chat_id, "I do not understand. Type /help for assistance.", bot_token)

# Function to send an image to the Telegram bot
def send_image(chat_id, file_path, file_type, file_name, bot_token):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"

        files = {
            'photo': (file_name, open(file_path, 'rb'), file_type),
        }

        data = {
            'chat_id': chat_id,
        }

        response = requests.post(url, data=data, files=files)

        if response.status_code != 200:
            # Handle the error
            print(f"Telegram API error: {response.status_code} - {response.text}")

    except Exception as e:
        # Handle any exceptions
        print(f"Error sending image to Telegram: {e}")

# Function to send a file to the Telegram bot
def send_file(chat_id, file_path, file_type, file_name, bot_token):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

        files = {
            'document': (file_name, open(file_path, 'rb'), file_type),
        }

        data = {
            'chat_id': chat_id,
        }

        response = requests.post(url, data=data, files=files)

        if response.status_code != 200:
            # Handle the error
            print(f"Telegram API error: {response.status_code} - {response.text}")

    except Exception as e:
        # Handle any exceptions
        print(f"Error sending file to Telegram: {e}")

# Function to send a message to the Telegram bot
def send_telegram_message(chat_id, message, bot_token):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
        }

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code != 200:
            # Handle the error
            print(f"Telegram API error: {response.status_code} - {response.text}")


    except Exception as e:
        # Handle any exceptions
        print(f"Error sending Telegram message: {e}")

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
        # print("Received update_data:", update_data)
        if update_data:
            if 'edited_message' in update_data:
                message = update_data['edited_message']
            else:
                message = update_data['message']['text']
            name = update_data['message']['chat']['username']
            chat_id = update_data['message']['chat']['id']

            # Call your add_or_update_user function to add/update the user in the database
            add_or_update_user(chat_id, name, message, conn)
            # Respond to a user  
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


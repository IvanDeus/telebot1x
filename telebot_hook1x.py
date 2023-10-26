## telegram bot by Ivan Deus
from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, abort
import json
import requests
import pymysql
import time
from passlib.hash import pbkdf2_sha256
import telebot
from telebot import types
from telebot_hook1x_func import *
app = Flask(__name__)
# Config import
from telebot_hook1x_cfg import bot_token, admin_name, db_host, db_username, db_password, db_name, mysql_unix_socket

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

# Build user chats table, last 300 records, template allow to filter them
def get_user_chats_table(conn):
    try:
        with conn.cursor() as cursor:
             query = ("SELECT tc.id AS telebot_chat_id, tc.lastupd AS telebot_chat_lastupd,"
          " tc.uchat_id, tu.name AS user_name, tu.first_name AS user_frstname, tc.umsg, ta.name AS admin_name, tc.mngmsg"
          " FROM telebot_chats tc JOIN telebot_users tu ON tc.uchat_id = tu.chat_id"
          " JOIN telebot_admins ta ON tc.mngchat_id = ta.chat_id ORDER BY telebot_chat_lastupd DESC Limit 300")
             cursor.execute(query)
             results = cursor.fetchall()
        return results
    except Exception as e:
        # Handle any exceptions (e.g., database connection error)
        print(f"Error: {e}")
        return []

def get_step_status(chat_id, conn):
    try:
        with conn.cursor() as cursor:
            # Use parameterized query to select the step status
            query = "SELECT step FROM telebot_users WHERE chat_id = %s"
            cursor.execute(query, (chat_id,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Return the step status if found
            else:
                return None  # Return None if user not found
    except pymysql.Error as e:
        # Handle any database errors here
        print(f"Database error: {e}")
        return None
# find if is there any users who needs manager attention
def find_if_any_user_needs_mngr(conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT id FROM telebot_users WHERE step = 101 LIMIT 1"
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

# telebot hadle user input
def handle_nostart(message, telebot_vars):
    chat_id = message.chat.id
    msg1 = telebot_vars['msg1']
    # Create an inline keyboard
    keyboard = types.InlineKeyboardMarkup()
    button2 = types.InlineKeyboardButton('Help', callback_data='/help')
    keyboard.add(button2)
    bot.send_message(chat_id, msg1, reply_markup=keyboard)

def handle_start(message, telebot_vars):
    chat_id = message.chat.id

    imgtosend = telebot_vars['imgtosend']
    msg2 = telebot_vars['msg2']
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
    bot.send_message(chat_id, msg2, reply_markup=keyboard)

def handle_callback(call, conn, manager_chat_id, telebot_vars):

    pdftosend = telebot_vars['pdftosend']
    keyboard2 = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Guide', callback_data='/guide')
    button3 = types.InlineKeyboardButton('Sub', callback_data='/sub')
    button4 = types.InlineKeyboardButton('Unsub', callback_data='/unsub')
    button5 = types.InlineKeyboardButton('Call Manager', callback_data='/manager')
    # Add the buttons to the keyboard
    keyboard2.add(button1, button3, button4, button5)
    # Handle button presses
    chat_id = call.message.chat.id
    data = call.data
    user_name = call.message.chat.username
    msg3 = telebot_vars['msg3']
    msg4 = telebot_vars['msg4']

    if data == '/guide':
         # Handle the /guide command to send a PDF file
        with open('telebot-h-files/' + pdftosend, 'rb') as pdf_file:
           bot.send_document(chat_id, pdf_file, caption=msg3)
        add_or_update_user(chat_id, ' ', data, conn, ' ', ' ')
        change_step_status(chat_id, conn, 1)
    elif data == '/help':
        bot.send_message(chat_id, msg4, reply_markup=keyboard2)
        add_or_update_user(chat_id, ' ', data, conn, ' ', ' ')
    elif data == '/sub':
        sub = 1
        change_sub_status(chat_id, conn, sub)
        bot.send_message(chat_id, "You have subscribed")
    elif data == '/unsub':
        sub = 0
        change_sub_status(chat_id, conn, sub)
        bot.send_message(chat_id, "You unsubscribed")
    elif data == '/manager':
     # Notify the manager
        if chat_id == int(manager_chat_id):
           bot.send_message(chat_id, "You are the manager, stop with /end")
        else:
           bot.send_message(manager_chat_id, f"{chat_id}: {user_name}: has initiated a chat. Respond via the bot.")
           change_step_status(chat_id, conn, 101)
           insert_into_chat_table(conn, chat_id, manager_chat_id, "Call manager", " ")
           # Notify user
           bot.send_message(chat_id, "Please wait for manager to get back to you")
# Telegram bot
@app.route('/')
def hello():
    # Create a response
    response = make_response(render_template('hello.html'))
    response.headers['X-Content-Type-Options'] = 'nosniff'
    ##response.headers['Server'] = 'server.name'
    response.headers['Cache-Control'] = 'no-cache'
    return response

# chat login route
@app.route('/admin-chat', methods=['GET', 'POST'])
def login_chat():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Get admin chat ID and hashed password from the database
        conn = pymysql.connect(unix_socket=mysql_unix_socket, user=db_username, password=db_password, database=db_name)
        admin_chatid, hashed_db_password = find_admin_chatid_and_password(conn, username)
        conn.close()
        time.sleep(1)
        if admin_chatid and pbkdf2_sha256.verify(password, hashed_db_password):
            try:
                response = make_response(redirect(url_for('chat_page')))
                # Set cookies
                response.set_cookie('chat_cookie_id', f'{admin_chatid}cookie_chat_passed_tst1212')
                response.set_cookie('chat_cookie_name', username)
                return response

            except Exception as e:
                print(f"Error: {e}")
                return "An error occurred."
        else:
            return "Invalid admin credentials. Please try again."

    # Create a response
    response = make_response(render_template('login_chat.html'))
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Cache-Control'] = 'no-cache'
    return response

@app.route('/chat_page', methods=['GET'])
def chat_page():
    # Check if the admin_cookie_id is set
    chat_cookie_id = request.cookies.get('chat_cookie_id')
    chat_cookie_name = request.cookies.get('chat_cookie_name')
    # Create a database connection with Unix socket
    conn = pymysql.connect(unix_socket=mysql_unix_socket, user=db_username, password=db_password, database=db_name)
    # get admin chat id from cookie name
    admin_chatid, hashed_db_password = find_admin_chatid_and_password(conn,chat_cookie_name)
    if chat_cookie_id != f'{admin_chatid}cookie_chat_passed_tst1212':  # cookie check
        abort(403)  # Return a forbidden error if the cookie is not set
    try:
        # get tables
        users = get_user_chats_table(conn)
        params = get_vars_table(conn)
        sched1 = get_scheduled_table(conn, 1)
         # create user table
        response = make_response(render_template('chat_table.html', users=users, params=params, sched1=sched1))
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Cache-Control'] = 'no-cache'
        return response

    except Exception as e:
        # Handle any exceptions here
        print(f"Error: {e}")
        return "An error occurred."
    # Close the database connection
    conn.close()

@app.route('/telebot1xmassmessage', methods=['POST'])
def telebot1xmassmessage():
    # Check if the admin_cookie_id is set
    chat_cookie_id = request.cookies.get('chat_cookie_id')
    chat_cookie_name = request.cookies.get('chat_cookie_name')
    # Create a database connection with Unix socket
    conn = pymysql.connect(unix_socket=mysql_unix_socket, user=db_username, password=db_password, database=db_name)
    # get admin chat id from cookie name
    admin_chatid, hashed_db_password = find_admin_chatid_and_password(conn,chat_cookie_name)
    if chat_cookie_id != f'{admin_chatid}cookie_chat_passed_tst1212':  # cookie check
        abort(403)  # Return a forbidden error if the cookie is not set
    try:
       bot = telebot.TeleBot(bot_token)
       message = request.form['message']
       sent_messages, error_messages = massmessage(conn, message, bot)
       conn.close()
       # Create a response
       response = make_response(render_template('massmessage.html', sent_messages = sent_messages, error_messages = error_messages))
       response.headers['X-Content-Type-Options'] = 'nosniff'
       response.headers['Cache-Control'] = 'no-cache'
       return response

    except Exception as e:
        # Handle any exceptions here
        print(f"Error: {e}")
        return "An error occurred."

# Define the route and function for adding a user
@app.route('/change-v', methods=['POST'])
def change_v():
    # Check if the admin_cookie_id is set
    chat_cookie_id = request.cookies.get('chat_cookie_id')
    chat_cookie_name = request.cookies.get('chat_cookie_name')
    # Create a database connection with Unix socket
    conn = pymysql.connect(unix_socket=mysql_unix_socket, user=db_username, password=db_password, database=db_name)
    # get admin chat id from cookie name
    admin_chatid, hashed_db_password = find_admin_chatid_and_password(conn,chat_cookie_name)
    if chat_cookie_id != f'{admin_chatid}cookie_chat_passed_tst1212':  # cookie check
        abort(403)  # Return a forbidden error if the cookie is not set
    try:
       # Get chat_id and name from the form data
       id_v = request.form['id_v']
       value_v = request.form['field']
       # set variables
       set_vars_table(conn, id_v, value_v)
       conn.close()
       # Redirect to the admin page
       return redirect('/chat_page')
    except Exception as e:
        # Handle any exceptions here
        print(f"Error: {e}")
        return "An error occurred."

# change scheduled events
@app.route('/change-event', methods=['POST'])
def change_event():
    admin_cookie_id = request.cookies.get('chat_cookie_id')
    admin_cookie_name = request.cookies.get('chat_cookie_name')
    conn = pymysql.connect(unix_socket=mysql_unix_socket, user=db_username, password=db_password, database=db_name)
    admin_chatid, hashed_db_password = find_admin_chatid_and_password(conn, admin_cookie_name)
    if admin_cookie_id != f'{admin_chatid}cookie_chat_passed_tst1212':  # cookie check
        abort(403)  # Return a forbidden error if the cookie is not set
    try:
       id_v = request.form['id_v']
       event_date = request.form['event_date']
       t_out = request.form['t_out']
       simg = request.form['image']
       message = request.form['fieldm']
       ukeys = request.form['ukeys']
       ev_id = request.form['ev_id']
       set_scheduled_table(conn, id_v, t_out, simg, message, ukeys, event_date, ev_id)
       conn.close()
       # Redirect to the admin page
       return redirect('/chat_page')
    except Exception as e:
        # Handle any exceptions here
        print(f"Error: {e}")
        return "An error occurred."

###set the number of messages in a scheduler
@app.route('/change-schnum', methods=['GET'])
def change_schnum():
    admin_cookie_id = request.cookies.get('chat_cookie_id')
    admin_cookie_name = request.cookies.get('chat_cookie_name')
    conn = pymysql.connect(unix_socket=mysql_unix_socket, user=db_username, password=db_password, database=db_name)
    admin_chatid, hashed_db_password = find_admin_chatid_and_password(conn, admin_cookie_name)
    if admin_cookie_id != f'{admin_chatid}cookie_chat_passed_tst1212':  # cookie check
        abort(403)  # Return a forbidden error if the cookie is not set
    try:
        msglast = int(request.args.get('msglast'))
        msgcount = int(request.args.get('msgcount'))
        update_sched_message_nmbr(conn, msgcount, msglast)
        conn.close()
        return redirect('/chat_page')
    except Exception as e:
        # Handle any exceptions here
        print(f"Error: {e}")
        return "An error occurred."


# Main logic
@app.route('/telebot-hook1x', methods=['POST'])
def telebothook1x():
    try:
        # Create a database connection with Unix socket
        conn = pymysql.connect(unix_socket=mysql_unix_socket, user=db_username, password=db_password, database=db_name)
        # get config variables
        telebot_vars = fetch_telebot_vars_into_dict(conn)
        #VERS 2 Get update array
        json_string = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_string)
        # Analyze recived message
       ## print (update)
        ##### get manager chat id
        manager_chat_id = get_manager_chat_id(conn)

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
            user_step_stat = get_step_status(chat_id, conn)
            # Handle start command
            if message.text == '/start':
                handle_start(message, telebot_vars)
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
                       #bot.forward_message(uchat_id, chat_id, message.id)
                       bot.send_message(uchat_id, message_text)
                       time.sleep(1)  # Add a delay
            elif user_step_stat == 101:
                # forward user who called manager
                fwd_umsg = str(chat_id) +": "+first_name+": "+ message.text
                bot.send_message(manager_chat_id, fwd_umsg)
                insert_into_chat_table(conn, chat_id, manager_chat_id, fwd_umsg, '  ')
            elif chat_id == int(manager_chat_id):
                        # find if any user flag = 101 (user needs attenction)
                if_any_user_needs_mngr = find_if_any_user_needs_mngr(conn)
                # extract user chat id from replied msg
                if message.reply_to_message is not None:
                   reply_text = message.reply_to_message.text
                   user_chat_id = reply_text.split(': ')
                   if message.text == '/end':
                      change_step_status(user_chat_id[0], conn, 0)
                   else:
                   # admin sends a message to a user who requested mmngr
                      bot.send_message(user_chat_id[0], "Manager: "+ message.text)
                   update_chat_table(conn, user_chat_id[0], message.text)
                else:
                   if if_any_user_needs_mngr:
                      bot.send_message(chat_id, "No message is sent, try 'reply'. To stop chat with user reply /end")
            else:
                handle_nostart(message, telebot_vars) # all others imput

        elif update.callback_query is not None:
            call = update.callback_query
            handle_callback(call, conn, manager_chat_id, telebot_vars)  # handle the callback query

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

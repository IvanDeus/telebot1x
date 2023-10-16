import argparse
import bcrypt
import pymysql

# Import your database credentials
from telebot_hook1x_cfg import db_host, db_username, db_password, db_name, mysql_unix_socket

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("username", help="Username to insert or update")
parser.add_argument("password", help="Password to hash and store")
args = parser.parse_args()

# Define a function to securely hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Connect to the database
connection = pymysql.connect(
    host=db_host,
    user=db_username,
    password=db_password,
    db=db_name,
    unix_socket=mysql_unix_socket
)

try:
    with connection.cursor() as cursor:
        # Check if the username exists
        cursor.execute("SELECT * FROM telebot_admins WHERE name = %s", (args.username,))
        existing_user = cursor.fetchone()

        # Hash the provided password
        hashed_password = hash_password(args.password)

        if existing_user:
            # Update the existing user
            cursor.execute("UPDATE telebot_admins SET passwd = %s WHERE name = %s", (hashed_password, args.username))
            connection.commit()
            print(f"Password for {args.username} updated successfully.")
        else:
            # Insert a new user
            cursor.execute("INSERT INTO telebot_admins (name, passwd) VALUES (%s, %s)", (args.username, hashed_password))
            connection.commit()
            print(f"New user {args.username} inserted successfully.")

finally:
    connection.close()

import pymysql
from passlib.hash import pbkdf2_sha256
from telebot_hook1x_cfg import db_host, db_username, db_password, db_name, mysql_unix_socket

# Function to hash a password using pbkdf2_sha256
def hash_password(password):
    return pbkdf2_sha256.hash(password)

# Function to insert or update a user's password in the database
def update_password(username, password):
    # Connect to the MySQL database
    db = pymysql.connect(
        host=db_host,
        user=db_username,
        password=db_password,
        db=db_name,
        unix_socket=mysql_unix_socket
    )
    cursor = db.cursor()

    # Check if the user exists
    cursor.execute("SELECT id FROM telebot_admins WHERE name = %s", (username,))
    user_id = cursor.fetchone()

    if user_id:
        # User exists, update the password
        user_id = user_id[0]
        hashed_password = hash_password(password)
        cursor.execute("UPDATE telebot_admins SET passwd = %s WHERE id = %s", (hashed_password, user_id))
    else:
        # User doesn't exist, insert a new record
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO telebot_admins (name, passwd) VALUES (%s, %s)", (username, hashed_password))

    db.commit()
    db.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Update user password in the telebot_admins table")
    parser.add_argument("username", type=str, help="Username for the user")
    parser.add_argument("password", type=str, help="Password to be hashed and stored")

    args = parser.parse_args()

    update_password(args.username, args.password)
    print("Password for user '{}' has been hashed and stored in the database.".format(args.username))

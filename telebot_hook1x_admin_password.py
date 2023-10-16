import sys
import pymysql
from passlib.hash import bcrypt

# Database credentials
db_host = "your_db_host"
db_username = "your_db_username"
db_password = "your_db_password"
db_name = "your_db_name"

# Function to create a database connection
def create_db_connection():
    return pymysql.connect(
        host=db_host,
        user=db_username,
        password=db_password,
        db=db_name
    )

# Function to store or update a user's password
def store_or_update_password(username, password):
    conn = create_db_connection()
    cursor = conn.cursor()

    # Check if the user already exists in the table
    cursor.execute("SELECT * FROM telebot_admins WHERE name = %s", (username,))
    user_data = cursor.fetchone()

    if user_data:
        # User exists, update the password
        hashed_password = bcrypt.using(schemes=['bcrypt']).hash(password)
        cursor.execute("UPDATE telebot_admins SET passwd = %s WHERE name = %s", (hashed_password, username))
    else:
        # User doesn't exist, insert a new record
        hashed_password = bcrypt.using(schemes=['bcrypt']).hash(password)
        cursor.execute("INSERT INTO telebot_admins (name, passwd) VALUES (%s, %s)", (username, hashed_password))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <username> <password>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    store_or_update_password(username, password)
    print(f"Password for user '{username}' has been stored or updated.")

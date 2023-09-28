# Ivan Deus telebot py cfg

# DB construction, copy this to MySQL to create a new table
###
'''...
CREATE TABLE telebot_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    lastupd TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    lastmsg TEXT );

'''

# Credentials put here
bot_token = "xxx:xxx"
admin_name = "ivan"
# Database connection parameters
db_host = "localhost"
db_username = "xxx"
db_password = "xxx"
db_name = "xxx"
# MySQL socket path
mysql_unix_socket = "/var/run/mysqld/mysqld.sock"
# Files to send
imgtosend = 'Asya-B-aa250.jpg'
pdftosend = 'guide.pdf'


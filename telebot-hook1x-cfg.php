<?php
// Ivan Deus telebot cfg
// DB construction, copy this to MySQL to create a new table
/*
CREATE TABLE telebot_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    lastupd TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    lastmsg TEXT );

*/

// Replace with your MySQL database credentials
    $db_host = 'localhost';
    $db_username = 'xxx';
    $db_password = 'xxx';
    $db_name = 'xxx';
 // Replace with admin name
    $admin_name='ivan';
 // Replace with your Telegram bot token
    $bot_token = 'xxx:xxx';
 // filenames to send 
 $imgtosend = 'Asya-B-aa250.jpg';
 $pdftosend = 'guide.pdf';
//eof
?>

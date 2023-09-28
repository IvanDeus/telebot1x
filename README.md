# telebot1x (php version) made by IvanDeus (2023)
This is a straightforward Telegram bot built on PHP/MySQL. 
It actively awaits user input, responds to a number of commands and efficiently stores every user chat in a MySQL table. 
The minimum system requirements for this bot are as follows: PHP version 5.3.10, MySQL version 5.5.54, and Apache2.

Installation Steps:

1. Begin by creating a Telegram bot using the @botfather and obtain the bot token.
2. Create the necessary MySQL table by copying the command from the telebot-hook1x-cfg.php file.
3. Insert your bot token and credentials into the telebot-hook1x-cfg.php configuration file.
4. Place all bot files in a publicly accessible folder within your Apache web server.
5. Establish a webhook, ensuring it uses HTTPS, and point it to the following URL: https://your-server/telebot-hook1x.php. All information regarding webhooks can be found here: https://core.telegram.org/bots/webhooks
6. You are now ready to start chatting with your bot.

You can interact with the bot using the following available commands: /start, /help, /guide, and /stat24 (exclusive to admin users).

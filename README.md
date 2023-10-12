# telebot1x (python version) made by IvanDeus (2023)
If you find yourself needing to send text information, images, or PDF files via Telegram to a user, then this bot is the ideal solution for you.

This is a straightforward Telegram bot built on Python/MySQL. 
It actively awaits user input, responds to a number of commands below and efficiently stores every user data in a MySQL table.

User can call a human manager any time by using correspondig command from a menu to start a meaningful conversation inside the bot.
Also, human manager can send to subscribed users a message using /forward command.

The minimum system requirements for this bot are as follows: Python 3.10.12, MySQL version 5.5.54, and Flask.

Installation Steps:

1. Begin by creating a Telegram bot using the @botfather and obtain the bot token.
2. Create the necessary MySQL table by copying the command from the telebot_hook1x_cfg.py file.
3. Insert your bot token and credentials into the telebot_hook1x_cfg.py configuration file.
4. Place all bot files in a publicly accessible folder via https. You can use Flask/gunicorn Python module to listen to user requests.
5. Establish a webhook, ensuring it uses HTTPS, and point it to the following URL: https://your-server/telebot-hook1x. All information regarding webhooks can be found here: https://core.telegram.org/bots/webhooks
6. You are now ready to start chatting with your bot.

You can interact with the bot using the following available commands: /start, /help, /guide, /sub, /unsub and /stat24, /forward, /end (last three are exclusive to admin users).
The bot manager has the option to log in to the following page: https://your-server/admin-chat, providing access to historical user chat data for review and analysis.

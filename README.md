# telebot1x (python version) made by IvanDeus (2024)
If your user care communication needs involve sending text, images, or PDF files via Telegram, this bot provides the perfect solution.

This Python/MySQL-based Telegram bot is designed with simplicity in mind. It's responsive to a variety of user commands, adept at storing all chat data efficiently in a MySQL table, and offers a seamless experience.

Users have the option to initiate a conversation with a human manager at any time using the designated command from the menu. This ensures meaningful interactions right within the bot. Furthermore, our human manager can easily send messages to subscribed users through the /forward command.

For the smooth operation of this bot, the minimum system requirements are as follows: Python 3.10.12, MySQL version 5.5.54, and Flask.

Installation Steps:

1. Begin by creating a Telegram bot using the @botfather and obtain the bot token.
2. Create the necessary MySQL table by copying the command from the telebot_hook1x_cfg_example.py file.
3. Insert your bot token and credentials into the telebot_hook1x_cfg_example.py configuration file and rename it to telebot_hook1x_cfg.py.
4. Place all bot files in a publicly accessible folder via https. Run "python run_telebot1x.py start" to listen to user requests.
5. Establish a webhook, ensuring it uses HTTPS, and point it to the following URL: https://your-server/telebot-hook1x. All information regarding webhooks can be found here: https://core.telegram.org/bots/webhooks
6. Add at least one admin using telebot_hook1x_admin_password.py
7. You are now ready to start chatting with your bot.

You can interact with the bot using the following available commands: /start, /help, /guide, /sub, /unsub and /stat24, /forward, /end (last three are exclusive to admin users).
The bot manager has the option to log in to the following page: https://your-server/admin-chat, providing access to message scheduler, mass messaging and historical user chat data for review and analysis.

To run Telebot1x message scheduler use crontab on your server like this (run script every 10 minutes):
 */10 * * * * python telebot_ask_user.py > /dev/null
 

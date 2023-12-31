# telebot1x (php version) made by IvanDeus (2023)
If you find yourself needing to send text information, images, or PDF files via Telegram to a user, then this bot is the ideal solution for you.

This is a straightforward Telegram bot built on PHP/MySQL. 
It actively awaits user input, responds to a number of commands and efficiently stores every user chat in a MySQL table. 
The minimum system requirements for this bot are as follows: PHP version 8.1.2, MySQL version 8.0.34, and Apache2.

Installation Steps:

1. Begin by creating a Telegram bot using the @botfather and obtain the bot token.
2. Create the necessary MySQL table by copying the command from the telebot-hook1x-cfg-example.php file.
3. Insert your bot token and credentials into the telebot-hook1x-cfg-example.php configuration file and rename it to telebot-hook1x-cfg.php.
4. Place all bot files in a publicly accessible folder within your Apache web server.
5. Establish a webhook, ensuring it uses HTTPS, and point it to the following URL: https://your-server/telebot-hook1x.php. All information regarding webhooks can be found here: https://core.telegram.org/bots/webhooks
6. It is recommended to use Nginx for proxying bot traffic in this manner: location /telebot-hook1x -> proxy_pass http://localhost/telebot-hook1x.php; location /admin-page -> proxy_pass http://localhost/telebot-admin-page.php; for improved security.
7. For a scheduler add into crontab: */8 * * * * php /var/www/html/telebot-ask-user.php > /dev/null
8. Use https://your-server/telebot-hook1x admin panel to set up scheduler and send mass messages if needed.
9. You are now ready to start chatting with your bot.

You can interact with the bot using the following available commands: /start, /help, /guide, and /stat24 (exclusive to admin users).

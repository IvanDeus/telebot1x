<?php
// configuration inclusion
require 'telebot-hook1x-cfg.php';
require 'telebot-hook1x-func.php';
// Check if the admin_cookie_id is set
$chatCookieId = isset($_COOKIE['chat_cookie_id']) ? $_COOKIE['chat_cookie_id'] : null;
$chatCookieName = isset($_COOKIE['chat_cookie_name']) ? $_COOKIE['chat_cookie_name'] : null;

// Create a database connection with Unix socket
$mysqli = new mysqli($db_host, $db_username, $db_password, $db_name);

if ($mysqli->connect_error) {
    die("Database connection failed: " . $mysqli->connect_error);
}

// Get admin chat id from cookie name
list($adminChatId, $hashedDbPassword) = findAdminChatIdAndPassword($mysqli, $chatCookieName);

if ($chatCookieId !== $adminChatId . 'cookie_chat_passed_tst1212') {
    http_response_code(403); // Return a forbidden error if the cookie is not set
} else {
    echo "OK";
}

$mysqli->close();
?>

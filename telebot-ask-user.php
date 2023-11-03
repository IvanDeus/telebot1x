<?php
require 'telebot-hook1x-cfg.php'; 
require 'telebot-hook1x-func.php';
$script_directory = __DIR__; // Get the directory of the current script
// Initialize the bot and the database connection
$bot = new Telebot($bot_token);
$conn = new mysqli($db_host, $db_username, $db_password, $db_name);

if ($conn->connect_error) {
    die("Database connection failed: " . $conn->connect_error);
}
// Event scheduler
$sched_events = getScheduledTable($conn, 1);
$current_datetime = new DateTime();
$telebot_vars = fetchTelebotVarsIntoArray($conn);
// Main logic, loop through events, then users who need notifying
foreach ($sched_events as $event) {
    list($event_id, $minutes_until_event, $img, $message, $ukeys, $event_date, $ev_id) = $event;
    $users_to_notify = getUsersToNotify($conn, $minutes_until_event, $event_id);

    // Check if it's the last event
    $is_last_event = $event === end($sched_events);

    foreach ($users_to_notify as $user) {
        $chat_id = $user['chat_id'];
        $photo_path = $script_directory . '/telebot-h-files/' . $img;
        $message1 = $message;
        sendNotification($bot, $chat_id, $photo_path, $message1, $ukeys);
        changeStepStatus($chat_id, $conn, $event_id + 1);

        if ($is_last_event) {
            // Set feedback mode for the last step
            changeStepStatus($chat_id, $conn, 111);
        }
    }
}
// Get users with expired feedback mode
$users_to_notify = getUsersToNotify($conn, 48, 111);
foreach ($users_to_notify as $user) {
    $chat_id = $user['chat_id'];
    changeStepStatus($chat_id, $conn, 0);
}
// Close the database connection
$conn->close();
?>

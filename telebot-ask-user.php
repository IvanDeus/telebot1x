<?php
// add into crontab: 
// */8 * * * * php /var/www/html/telebot-ask-user.php > /dev/null
require 'telebot-hook1x-cfg.php'; 
require 'telebot-hook1x-func.php';
$script_directory = __DIR__; // Get the directory of the current script
// Initialize the database connection
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
    $users_to_notify = getUsersToNotify($conn, $event['t_out'], $event['id']);
    // Check if it's the last event
    $is_last_event = $event === end($sched_events);
    foreach ($users_to_notify as $user) {
        $chat_id = $user['chat_id'];
        $photo_path = $event['simg'];
        $message1 = $event['message'];
        sendNotification($bot_token, $chat_id, $photo_path, $message1, $event['ukeys']);
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

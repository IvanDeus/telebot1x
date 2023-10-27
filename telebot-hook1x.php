<?php
// Ivan Deus telebot php version 
// configuration inclusion
require 'telebot-hook1x-cfg.php';
require 'telebot-hook1x-func.php';
//This is a main program
    // Create a database connection
    $conn = new mysqli($db_host, $db_username, $db_password, $db_name);

    // Check the database connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

// Function to handle incoming Telegram updates
function handle_telegram_update($update_data,$bot_token,$conn) {
	// call for vars
$telebotVars = fetchTelebotVarsIntoArray($conn);
$imgtosend  = $telebotVars['imgtosend'];
$pdftosend = $telebotVars['pdftosend'];
    if (isset($update_data['message'])) {
        $chat_id = $update_data['message']['chat']['id'];
        $message_text = $update_data['message']['text'];

        // Check the message text for specific commands or keywords
        if (strpos($message_text, '/start') !== false) {

            // Send the image right after the welcome message
            send_image($chat_id, 'telebot-h-files/'.$imgtosend, 'image/jpeg', $imgtosend,$bot_token);

            // Handle the /start command
            send_telegram_message($chat_id, 'Ivan Deus bot welcomes you! Type /guide or /help for all available commands',$bot_token);
        } elseif (strpos($message_text, '/help') !== false) {
            // Handle the /help command
            send_telegram_message($chat_id, 'This is a help message. Try /start or /guide',$bot_token);
        } elseif (strpos($message_text, '/guide') !== false) {
            // Handle the /guide command to send a PDF file
            send_file($chat_id, 'telebot-h-files/'.$pdftosend, 'application/pdf', $pdftosend,$bot_token);
        } else {
            // Handle other user input as needed
            send_telegram_message($chat_id, "I do not understand. Type /help for assistance.",$bot_token);
        }
    }
}


// Get the incoming Telegram update
$update = file_get_contents('php://input');
$update_data = json_decode($update, true);

if ($update_data) {
              //mysql add or upd user
        $name=$update_data['message']['chat']['username'];
        $chat_id=$update_data['message']['chat']['id'];
	$message=$update_data['message']['text'];
 $admin_name = findAdminChatIDAndPassword($conn, $name);
        addOrUpdateUser($chat_id, $name, $message, $conn);
		
		// Check the message text for stat commands and admin name 
        if (strpos($message, '/stat24') !== false && $chat_id == $admin_name['adminChatID']) {
		$last24Users = getLast24Users($conn);
		// no need to decode the JSON string into a PHP array
		// $last24Users = json_decode($last24Users, true);
		$message_lastu = '';
		// Loop through the $last24Users array
		foreach ($last24Users as $userData) {
		// Access each variable in the $userData array
		$id = $userData["id"];
		$chat_id2 = $userData["chat_id"];
		$name = $userData["name"];
		$lastupd = $userData["lastupd"];
		$lastmsg = $userData["lastmsg"];

		// work with each variable as needed
		$message_lastu .= "ID: $id\n";
		$message_lastu .= "Chat ID: $chat_id2\n";
		$message_lastu .=  "Name: $name\n";
		$message_lastu .=  "Last Update: $lastupd\n";
		$message_lastu .=  "Last Message: $lastmsg\n";
		$message_lastu .=  "\n";
		}
		send_telegram_message($chat_id, $message_lastu, $bot_token);		

            } else {
		handle_telegram_update($update_data, $bot_token, $conn);}
} else {
include 'login_chat.html';
// Chat login route
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    $hasharray = findAdminChatIDAndPassword($conn, $username);
    sleep(1);
// Split the stored hash into its components
$hashComponents = explode('$', $hasharray['hashedDBPassword']);
if (count($hashComponents) === 5) {
    list(, $algorithm, $iterations, $salt, $hash) = $hashComponents;
    // Compute the PBKDF2-SHA256 hash of the user input with the stored parameters
    $computedHash = hash_pbkdf2('sha256', $password, base64_decode($salt), (int)$iterations, 0, true);
    $computedHash = base64_encode($computedHash);
    // for some reason add = at the end?
    $hash = $hash."=";
    // Compare the computed hash with the stored hash
    if (hash_equals($hash, $computedHash)) {
        try {
            // Create a response object and set cookies
            header("Location: admin-page"); // Redirect
            setcookie('chat_cookie_id', $adminChatID . 'cookie_chat_passed_tst1212', time() + 3 * 24 * 3600);
            setcookie('chat_cookie_name', $username, time() + 3 * 24 * 3600);
            exit; // Redirect to the admin page
        } catch (Exception $e) {
            echo "An error occurred: " . $e->getMessage();
        }
    } else {
        echo "Invalid admin credentials. Please try again.";
    }
}
}
}
// Close the database connection
$conn->close();
?>


<?php
// Ivan Deus telebot v05
// configuration inclusion
require 'telebot-hook1x-cfg.php';

//This is a main program
    // Create a database connection
    $conn = new mysqli($db_host, $db_username, $db_password, $db_name);

    // Check the database connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

// Function to add or update a user in the 'telebot_users' table
function addOrUpdateUser($chat_id, $name, $message, $conn) {

    // Escape user input to prevent SQL injection
    $chat_id = $conn->real_escape_string($chat_id);
    $name = $conn->real_escape_string($name);
    $message = $conn->real_escape_string($message);

    // Check if the user already exists in the table
    $query = "SELECT * FROM telebot_users WHERE chat_id = '$chat_id'";
    $result = $conn->query($query);

    if ($result->num_rows > 0) {
        // User exists, update the record
        $query = "UPDATE telebot_users SET lastmsg = '$message' WHERE chat_id = '$chat_id'";
        if ($conn->query($query) === TRUE) {
            // Successfully updated the user
        } else {
            // Handle the update error
            echo "Error updating user: " . $conn->error;
        }
    } else {
        // User does not exist, insert a new record
        $query = "INSERT INTO telebot_users (chat_id, name, lastmsg) VALUES ('$chat_id', '$name', '$message')";
        if ($conn->query($query) === TRUE) {
            // Successfully inserted the new user
        } else {
            // Handle the insert error
            echo "Error inserting user: " . $conn->error;
        }
    }

}

// Function to get the last 24 rows with the most recent timestamps
function getLast24Users($conn) {

    // Query to retrieve the last 24 rows with the most recent timestamps
    $query = "SELECT * FROM telebot_users ORDER BY lastupd DESC LIMIT 24";

    // Execute the query
    $result = $conn->query($query);

    // Check if there are results
    if ($result->num_rows > 0) {
        $users = array();

        // Fetch each row as an associative array
        while ($row = $result->fetch_assoc()) {
            $users[] = $row;
        }
        return $users;
    } else {
        // No results found
        return array();
    }
}

// Function to handle incoming Telegram updates
function handle_telegram_update($update_data,$bot_token) {
// call for global vars
Global $imgtosend;
Global $pdftosend;
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


// Function to send an image to the Telegram bot
function send_image($chat_id, $file_path, $file_type, $file_name, $bot_token) {
    // Initialize cURL session
    $ch = curl_init("https://api.telegram.org/bot$bot_token/sendPhoto");

    // Create a cURL file object for the image
    if (function_exists('curl_file_create')) {
        $cFile = curl_file_create($file_path, $file_type, $file_name);
    } else {
        $cFile = '@' . realpath($file_path);
    }

    // Set cURL options for sending the image
    $data = array(
        'chat_id' => $chat_id,
        'photo' => $cFile,
    );

    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

    // Execute cURL session to send the image
    $result = curl_exec($ch);

    if ($result === false) {
        // Handle the error
        $error_message = curl_error($ch);
        error_log('Telegram API error: ' . $error_message);
    } else {
        // Image sent successfully
    }

    // Close cURL session
    curl_close($ch);
}


// Function to send a file to the Telegram bot
function send_file($chat_id, $file_path, $file_type, $file_name, $bot_token) {
    // Initialize cURL session
    $ch = curl_init("https://api.telegram.org/bot$bot_token/sendDocument");

    // Create a cURL file object for the file
    if (function_exists('curl_file_create')) {
        $cFile = curl_file_create($file_path, $file_type, $file_name);
    } else {
        $cFile = '@' . realpath($file_path);
    }

    // Set cURL options for sending the file
    $data = array(
        'chat_id' => $chat_id,
        'document' => $cFile,
    );

    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

    // Execute cURL session to send the file
    $result = curl_exec($ch);

    if ($result === false) {
        // Handle the error
        $error_message = curl_error($ch);
        error_log('Telegram API error: ' . $error_message);
    } else {
        // File sent successfully
    }

    // Close cURL session
    curl_close($ch);
}


// Function to send a message to the Telegram bot
function send_telegram_message($chat_id, $message, $bot_token) {
    $url = "https://api.telegram.org/bot$bot_token/sendMessage";
    $data = array(
        'chat_id' => $chat_id,
        'text' => $message,
    );

    $options = array(
        'http' => array(
            'header' => "Content-Type: application/json\r\n",
            'method' => 'POST',
            'content' => json_encode($data),
        ),
    );

    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);

    if ($result === false) {
        // Handle the error
        $error_last = error_get_last();
        error_log('Telegram API error: ' . $error_last['message']);
    } else {
        // Message sent successfully
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
        addOrUpdateUser($chat_id, $name, $message, $conn);
		
		// Check the message text for stat commands and admin name 
        if (strpos($message, '/stat24') !== false && $name == $admin_name) {
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
		handle_telegram_update($update_data, $bot_token);}
} else {
header("HTTP/1.1 400 Bad Request");
echo "Bad Request";
}
// Close the database connection
$conn->close();
?>


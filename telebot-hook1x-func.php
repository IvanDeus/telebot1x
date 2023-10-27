<?php
// Ivan Deus telebot v05
// configuration inclusion
function fetchTelebotVarsIntoArray($conn) {
    try {
        $query = "SELECT param, value FROM telebot_vars";
        $result = $conn->query($query);
        
        $telebotVars = []; // Initialize an empty array

        while ($row = $result->fetch_assoc()) {
            $param = $row['param'];
            $value = $row['value'];
            $telebotVars[$param] = $value; // Add data to the array
        }

        return $telebotVars;
    } catch (Exception $e) {
        // Handle any exceptions, e.g., database connection error
        return [];
    }
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

// tables for admin page
function getVarsTable($conn) {
    try {
        $query = "SELECT * FROM telebot_vars ORDER BY param";
        $result = $conn->query($query);

        if ($result === false) {
            throw new Exception("Query execution failed: " . $conn->error);
        }

        $results = [];

        while ($row = $result->fetch_assoc()) {
            $results[] = $row;
        }

        return $results;
    } catch (Exception $e) {
        // Handle any exceptions (e.g., database connection error)
        echo "Error: " . $e->getMessage();
        return [];
    }
}

function getScheduledTable($conn, $ev_id) {
    try {
        $query = "SELECT * FROM telebot_sched WHERE ev_id = ? ORDER BY id";
        $stmt = $conn->prepare($query);
        $stmt->bind_param("i", $ev_id);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($result === false) {
            throw new Exception("Query execution failed: " . $stmt->error);
        }

        $results = [];

        while ($row = $result->fetch_assoc()) {
            $results[] = $row;
        }

        return $results;
    } catch (Exception $e) {
        // Handle any exceptions (e.g., database connection error)
        echo "Error: " . $e->getMessage();
        return [];
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

// for login
function findAdminChatIDAndPassword($conn, $username) {
    $stmt = $conn->prepare("SELECT chat_id, passwd FROM telebot_admins WHERE name = ?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $stmt->bind_result($adminChatID, $hashedDBPassword);
    $stmt->fetch();
    $stmt->close();
    return ["adminChatID" => $adminChatID, "hashedDBPassword" => $hashedDBPassword];

}

?>


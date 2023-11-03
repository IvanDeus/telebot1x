<?php
// Ivan Deus telebot php version 
// send scheduled message with image and keyboard
function sendNotification($bot_token, $chat_id, $photo, $message, $ukeys) {
	try {
$script_directory = __DIR__; 
send_image($chat_id, $script_directory.'/telebot-h-files/'.$photo, 'image/jpeg', $photo, $bot_token);
send_telegram_message($chat_id, $message, $bot_token);
/*        
        if ($ukeys === "None") {
            $bot->sendMessage($chat_id, $message);
        } else {
            $keyboard = inlineButtonConstructor($ukeys);
            $bot->sendMessage($chat_id, $message, null, false, null, $keyboard);
        }
*/      
        sleep(0.5);
    } catch (Exception $e) {
        if ($e->getCode() === 403) {
            if (strpos($e->getMessage(), "Forbidden: bot was blocked by the user") !== false) {
                echo "User with chat_id $chat_id has blocked the bot";
            } else {
                echo "A 403 error occurred for chat_id $chat_id: " . $e->getMessage();
            }
        }
    }
}

//# change step for scheduler
function changeStepStatus($chat_id, $conn, $stp) {
    $query = "UPDATE telebot_users SET step = ? WHERE chat_id = ?";
    if ($stmt = $conn->prepare($query)) {
        $stmt->bind_param("ss", $stp, $chat_id);
        $stmt->execute();
        $stmt->close();
    } else {
        // Handle any database errors here
        echo "Database error: " . $conn->error;
    }
}

// for ask user scheduler
function getUsersToNotify($conn, $hours, $step) {
    $twentyFourHoursAgo = new DateTime();
    $twentyFourHoursAgo->sub(new DateInterval("PT{$hours}H")); 
    $twentyFourHoursAgoStr = $twentyFourHoursAgo->format('Y-m-d H:i:s');
    $query = "SELECT chat_id, first_name FROM telebot_users WHERE lastupd < '{$twentyFourHoursAgoStr}' AND step = '{$step}' AND Sub = 1";
    $users = array();
    if ($result = $conn->query($query)) {
        while ($row = $result->fetch_assoc()) {
            $users[] = $row;
        }
        $result->free();
    }
    return $users;
}

// retrieve variables 
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
        $query = "SELECT * FROM telebot_vars ORDER BY param";
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
// fetch message scheduler for admin 
function getScheduledTable($conn, $ev_id) {
        $query = "SELECT * FROM telebot_sched WHERE ev_id = $ev_id ORDER BY id";
    $result = $conn->query($query);
    if ($result->num_rows > 0) {
        $urs = array();
        while ($row = $result->fetch_assoc()) {
            $urs[] = $row;
	}
        return $urs;
    } else {
        // No results found
        return array();
    }
}
// Set variables for admin page
function setVarsTable($conn, $id_v, $value_v) {
    try {
        $query = "UPDATE telebot_vars SET value = ? WHERE id = ?";
        $stmt = $conn->prepare($query);
        $stmt->bind_param("si", $value_v, $id_v);
        $stmt->execute();
        $stmt->close();
        $conn->commit();
    } catch (mysqli_sql_exception $e) {
        // Handle any database errors here
        echo "Database error: " . $e->getMessage();
    }
}
// update scheduler 
function setScheduledTable($conn, $id_v, $t_out, $simg, $message, $ukeys, $event_date, $ev_id) {
    try {
        $query = "UPDATE telebot_sched SET t_out = ?, simg = ?, message = ?, ukeys = ?, event_date = ?, ev_id = ? WHERE id = ?";
        $stmt = $conn->prepare($query);
        $stmt->bind_param("ssssssi", $t_out, $simg, $message, $ukeys, $event_date, $ev_id, $id_v);
        $stmt->execute();
        $stmt->close();
        $conn->commit();
    } catch (mysqli_sql_exception $e) {
        // Handle any database errors
        echo "Database error: " . $e->getMessage();
    }
}

function updateSchedMessageNumber($connection, $x, $y) {
    try {
        $updateSql = "UPDATE telebot_sched SET ev_id = 99 WHERE id > ? AND id <= ?";
        $stmt = $connection->prepare($updateSql);
        $stmt->bind_param("ii", $x, $y);
        $stmt->execute();

        $updateSql = "UPDATE telebot_sched SET ev_id = 1 WHERE id <= ?";
        $stmt = $connection->prepare($updateSql);
        $stmt->bind_param("i", $x);
        $stmt->execute();

        $connection->commit();
    } catch (mysqli_sql_exception $e) {
        // Handle any database errors here
        echo "Database error: " . $e->getMessage();
    }
}
// Function to send a one-time mass message to all subscribed users
function massMessage($conn, $message, $bot_token) {
    $userChatIDs = findSubscribedChatIDs($conn);
    $sentMessages = [];
    $errorMessages = [];

    foreach ($userChatIDs as $chatID) {
	    try {
            // Send a message
	send_telegram_message($chatID, $message, $bot_token);
            $sentMessages[] = $chatID . " : ";
            usleep(500000); // Sleep for 0.5 seconds
        } catch (TelegramError $e) {
            if ($e->getCode() == 403) {
                if (strpos($e->getMessage(), "Forbidden: bot was blocked by the user") !== false) {
                    $errorMessages[] = "User with chat_id $chatID has blocked the bot";
                } else {
                    $errorMessages[] = "A 403 error occurred for chat_id $chatID: " . $e->getMessage();
                }
            }
        }
    }
    return [$sentMessages, $errorMessages];
}

// Function to find all subscribed chat IDs
function findSubscribedChatIDs($conn) {
    try {
        $query = "SELECT chat_id FROM telebot_users WHERE Sub = 1";
        $result = $conn->query($query);

        if ($result->num_rows > 0) {
            $chatIDs = [];
            while ($row = $result->fetch_assoc()) {
                $chatIDs[] = $row['chat_id'];
            }
            return $chatIDs;
        } else {
            return [];
        }
    } catch (Exception $e) {
        // Handle any exceptions (e.g., database connection error)
        echo "Error: " . $e->getMessage();
        return [];
    }
}

// get the last 24 rows with the most recent timestamps
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

// send an image to the Telegram bot
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


// send a file to the Telegram bot
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


// send a message to the Telegram bot
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


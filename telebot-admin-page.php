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

// Retrieve variables from the database
$vars = getVarsTable($mysqli);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Bot Admin Page</title>
 <style>
        table {
            border-collapse: collapse;
            width: 100%;
            border: 1px solid #ddd;
            font-size: 14px;
        }
        th, td {
            text-align: left;
            padding: 8px;
            font-size: 14px;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .pagination {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .page-link {
            padding: 5px 10px;
            margin: 0 5px;
            background-color: #007bff;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
        }
        .page-link:hover {
            background-color: #0056b3;
        }
        .infomessage {
            background-color: #1480b1;
            text-align: left;
            font-size: 10px;
        }
        .infomessage2 {
            background-color: #f180a1;
            text-align: left;
            font-size: 10px;
        }

        .infomessage3 {
            background-color: #f180a1;
            text-align: center;
            font-size: 20px;
            padding: 10px;
        }

        .infomessage4 {
            background-color: #80f1a1;
            text-align: left;
            font-size: 10px;
        }

        .infomessage5 {
            background-color: #80f1a1;
            text-align: center;
            font-size: 20px;
            padding: 10px;
        }
.modal {
  display: none;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 90%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fff;
  padding: 20px;
  text-align: center;
  width: 90%;
  height: 80%;
  margin-left: 55px;
  position: relative;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 40px;
  height: 40px;
  cursor: pointer;
  background-color: #ff0000;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%; 
  font-size: 24px;
}
        .collapsible-button {
            cursor: pointer;
        }

        .collapsible-content {
            display: none;
        }
        .rounded-block {
            border: 2px solid #000;
            border-radius: 10px;
            padding: 10px;
            margin: 5px;
            background-color: #ddddff;
        }
        .muted-block {
            border: 2px solid #000;
            border-radius: 10px;
            padding: 10px;
            margin: 5px;
            background-color: #202022;
        }
        .rounded-block2 {
          width: 48ch;
          height: 18em;
            border: 1px solid #000;
            border-radius: 10px;
            padding: 5px;
            margin: 5px;
            background-color: #f5f5ff;
            overflow: auto;
        }
        .checkbox {
            display: block;
        }
    </style>
</head>
<body>
    <h1>Admin Variables</h1>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Param</th>
            <th>Value</th>
            <th>Action</th>
        </tr>

        <?php
        foreach ($vars as $var) {
	echo "<tr>";
 	echo "<td>" . $var['id'] . "</td>";
            echo "<td>" . $var['param'] . "</td>";
            echo "<td>" . $var['value'] . "</td>";
            echo "<td>Action</td>";
            echo "</tr>";
        }
        ?>
    </table>
</body>
</html>


<?php
}
$mysqli->close();
?>

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
	// Checking if any table shoyuld be updated
	// sheduler and variables
	// then messaging
	//
$changevarform = 0;    
$changeshedform = 0;    
$changeMessageCount = 0;    
$MMform = 0;    
// Get chat_id and name from the form data
//
if (isset($_POST['id_v'])) {
 $id_v = $_POST['id_v'];
 $changevarform = $_POST['changevarform'];
 $value_v = $_POST['field'];}
// Set variables in the database
if ($changevarform == 1) {
$value_v = str_replace('"', "'", $value_v);
  setVarsTable($mysqli, $id_v, $value_v);
    $changevarform = 0;
}
if (isset($_POST['t_out'])) {
    $t_out = $_POST['t_out'];
    $event_date = $_POST['event_date'];
    $simg = $_POST['image'];
    $changeshedform = $_POST['changeshedform'];
    $message = $_POST['fieldm'];
    $ukeys = $_POST['ukeys'];
    $ev_id = $_POST['ev_id'];}
    if ($changeshedform == 1) {
$message = str_replace('"', "'", $message);
 setScheduledTable($mysqli, $id_v, $t_out, $simg, $message, $ukeys, $event_date, $ev_id);
 $changeshedform = 0;
    }
if (isset($_GET['changeMessageCount'])) {
    $changeMessageCount = $_GET['changeMessageCount'];
    $msglast = $_GET['msglast'];
    $msgcount = $_GET['msgcount'];}
  if ($changeMessageCount == 1) {
 updateSchedMessageNumber($mysqli, $msgcount, $msglast);	    
	$changeMessageCount = 0; } 

if (isset($_POST['mmessage'])) {
    $mmessage = $_POST['mmessage'];
    $MMform = $_POST['MMform'];}
  if ($MMform == 1) {
// Call the massMessage function to send the message
list($sentMessages, $errorMessages) = massMessage($mysqli, $mmessage, $bot_token);
 $MMform = 0;
// Display the results
echo "Messages sent:\n";
foreach ($sentMessages as $sentMessage) {
    echo $sentMessage . "\n";
}
echo "\nError messages:\n";
foreach ($errorMessages as $errorMessage) {
    echo $errorMessage . "\n";
  } 
  }  
    // Retrieve variables from the database
	$vars = getVarsTable($mysqli);
	$scvars = getScheduledTable($mysqli, 1);

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
#massMessageButton {
        background-color: red;
        color: white;
        text-align: center;
        display: block;
        margin: 0 auto;
        padding: 10px 20px; /* Adjust padding as needed */
        border: none;
        cursor: pointer;
    }
    </style>
</head>
<body>
<h1>Bot Scheduler</h1>


<table id="sch1" >
<?php $counter = 0;
   foreach ($scvars as $sch1) : 
    if ($counter % 4 == 0) : ?>
            <tr>
        <?php endif; ?>
        <td>
            <div class="rounded-block">
                <h3>Message #<?= $sch1['id'] ?> &nbsp; Timeout: <?= $sch1['t_out'] ?>h.</h3>
                <p>Image to send: <?= $sch1['simg'] ?></p>
                <p class="rounded-block2" id="sch1im"><?= $sch1['message'] ?></p>
                <p>User keys: <?= $sch1['ukeys'] ?></p>
 <button onclick="openModalSch1(<?= $sch1['id'] ?>,`<?= $sch1['message'] ?>`, <?= $sch1['t_out'] ?>, '<?= $sch1['simg'] ?>', '<?= $sch1['ukeys'] ?>')">Modify</button>
                <script> var sch1IDValue = <?= $sch1['id'] ?>; </script>
            </div>
        </td>
        <?php if ($counter % 4 == 3) : ?>
            </tr>
        <?php endif; ?>
        <?php $counter++; ?>
    <?php endforeach; ?>
    <tr>
        <td>
            <h3>&nbsp;<label for="messageCount">Number of messages: </label>
                <select name="msgcnt" id="messageCount" onchange="window.location.href='?changeMessageCount=1&msglast=8&msgcount='+this.value;">
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                    <option value="6">6</option>
                    <option value="7">7</option>
                    <option value="8">8</option>
                </select>
            </h3>
        </td>
    </tr>
</table>


 <h1>Admin Variables</h1>
    <table id="var1" >
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
 echo '<td> <button onclick="openModal(`'. $var['id'] .'`, `'. $var['param'].'`, `'. $var['value'] .'`)">Change value</button> </td>';
            echo "</tr>";
        }
        ?>
    </table>

<script>document.getElementById("messageCount").value = sch1IDValue;</script>

<div id="modalSch1" class="modal" style="display: none;">
    <div class="modal-content">
        <span class="close" onclick="closeSch1Modal()">&times;</span>
        <h2 class="infomessage5" id="modalSch1Title">Modify Message</h2>
        <form method="POST" action="/admin-page">
           <p>
                <label for="modalSch1Timeout">Timeout:</label>
                <input type="text" name="t_out" id="modalSch1Timeout"> &nbsp;
                <label for="modalSch1Image">Image to Send:</label>
                <input type="text" name="image" id="modalSch1Image">
            </p>
        <input type="hidden" name="id_v" id="modalSch1Id">
                <input type="hidden" name="ev_id" id="ev_idm" value=1>
            <input type="hidden" name="changeshedform" id="changeshedform" value=1>
                <input type="hidden" name="event_date" id="event_datem" value="2023-10-20">
            <p>
                <label for="modalSch1Value">Message:</label><br>
                <textarea name="fieldm" cols="80" rows="30" required id="modalSch1Value"></textarea>
            </p>
            <p><label for="ukeys1">User keys:</label>
        <input type="text" name="ukeys" id="ukeys1"></p>
            <br><input type="submit" value=" Change ">
        </form>
    </div>
</div>
<div id="myModal" class="modal" style="display: none;">
    <div class="modal-content">
        <span class="close" onclick="closeModal()">&times;</span>
        <p id="modalContent">"paramValue"</p>
        <form method="POST" action="/admin-page">
            <input type="hidden" name="id_v" id="paramId">
            <input type="hidden" name="changevarform" id="changevarform" value=1>
            <textarea title="afldx" name="field" cols="80" rows="30" required id="paramValue"></textarea>
            <br>
            <input type="submit" value="Change">
        </form>
	<p>
        <form method="POST" action="/admin-page" id="massMessageForm" style="display: none;">
            <input type="hidden" name="mmessage" id="massMessageInput">
            <input type="hidden" name="MMform" id="MMform" value=1>
        </form>
        <button id="massMessageButton" onclick="triggerMassMessage()" style="display: none;">Mass Message!</button>
	</p>  </div>
</div>

<script>
function openModalSch1(messageId, messageValue, timeout, image, ukeys) {
    var modal = document.getElementById("modalSch1");
    var modalTitle = document.getElementById("modalSch1Title");
    var modalIdField = document.getElementById("modalSch1Id");
    var modalValueField = document.getElementById("modalSch1Value");
    var modalTimeoutField = document.getElementById("modalSch1Timeout");
    var modalImageField = document.getElementById("modalSch1Image");
    var modalUkeysField = document.getElementById("ukeys1");
    modalTitle.textContent = "Modify Message #" + messageId;
    modalIdField.value = messageId;
    modalValueField.value = messageValue;
    modalTimeoutField.value = timeout;
    modalImageField.value = image;
    modalUkeysField.value = ukeys;
    modal.style.display = "block";
}

function closeSch1Modal() {
    var modal = document.getElementById("modalSch1");
    modal.style.display = "none";
}

function openModal(paramId, paramParam, paramValue) {
    var modal = document.getElementById("myModal");
    var modalContent = document.getElementById("modalContent");
    var paramIdField = document.getElementById("paramId");
    var paramValueField = document.getElementById("paramValue");
    var massMessageForm = document.getElementById("massMessageForm");
    var massMessageInput = document.getElementById("massMessageInput");
    var massMessageButton = document.getElementById("massMessageButton");
    modalContent.innerHTML = paramParam;
    paramIdField.value = paramId;
    paramValueField.value = paramValue;
    if (paramParam === "massmessage1") {
        massMessageForm.style.display = "block";
        massMessageInput.value = paramValue;
        massMessageButton.style.display = "block";
    } else {
        massMessageForm.style.display = "none";
        massMessageButton.style.display = "none";
    }

    modal.style.display = "block";
}
function triggerMassMessage() {
    var massMessageForm = document.getElementById("massMessageForm");
    massMessageForm.submit();
}
function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}
</script>
</body>
</html>
<?php

}
$mysqli->close();
?>

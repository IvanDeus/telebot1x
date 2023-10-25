# Ivan Deus telebot py cfg
# DB construction, copy this into MySQL to create a new table
###
'''
-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
-- ------------------
DROP TABLE IF EXISTS `telebot_admins`;
CREATE TABLE `telebot_admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chat_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `message_id` varchar(255) DEFAULT NULL,
  `pendingmsg` tinyint(1) NOT NULL DEFAULT '0',
  `chatmngr` smallint DEFAULT '0',
  `passwd` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
;
--
-- Table structure for table `telebot_chats`
--
DROP TABLE IF EXISTS `telebot_chats`;
CREATE TABLE `telebot_chats` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uchat_id` varchar(255) NOT NULL,
  `mngchat_id` varchar(255) NOT NULL,
  `umsg` varchar(1500) NOT NULL,
  `mngmsg` varchar(1500) NOT NULL,
  `lastupd` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
;

-- Table structure for table `telebot_sched`
--
DROP TABLE IF EXISTS `telebot_sched`;
CREATE TABLE `telebot_sched` (
  `id` int NOT NULL AUTO_INCREMENT,
  `t_out` smallint DEFAULT '0',
  `simg` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `message` varchar(3800) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `ukeys` varchar(200) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  `event_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `ev_id` smallint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
;
--
-- Dumping data for table `telebot_sched`
--
LOCK TABLES `telebot_sched` WRITE;
/*!40000 ALTER TABLE `telebot_sched` DISABLE KEYS */;
INSERT INTO `telebot_sched` VALUES (1,24,'mini.jpg','This is a first message from series of scheduled messages from bot','Help, /help','2023-10-20 00:00:00',1),(2,4,'mini.jpg','Should you stay or should you go?','Subscribe, /sub, Unsubscribe, /unsub, Call manager, /manager','2023-10-20 00:00:00',1),(3,24,'mini.jpg','If you need human touch please call our manager','Help, /help, Call manager, /manager','2023-10-20 00:00:00',1),(4,60,'mini.jpg','Шалом!\r\nЮные и почтенные эмансипе должны знать об изобретениях, их освободивших. Как раз о таковом вам расскажет Ася. Вы узнаете:\r\n\r\n- что общего у микрофона и презервативов?\r\n- как изобретение микрофона повлияло на вокал, жанры и стили музыки и остановило дискриминацию?\r\n','None','2023-10-20 00:00:00',1),(5,60,'mini.jpg','Зачем нужна РАСПЕВКА? Расскажет #Асяпишет\r\n(Посты от Аси я, Ботесса Сингирелла, отмечаю под хэштегом #АсяПишет )\r\n\r\nВы, наверняка, слышали о таком понятии как \"распевка\" или \"warm-up\". Прежде, чем исполнитель(ница) начинает репетицию или выступление, он(а) обязательно распевается!\r\n','None','2023-10-20 00:00:00',1),(6,120,'mini.jpg','Доброго дня!\r\n“Желаю научиться импровизировать и впечатлять слушателей своей импровизацией. Как это сделать?” Ася расскажет, как научиться этой науке. (Посты от Аси я отмечаю под хэштегом #АсяПишет)\r\n\r\n\r\n','None','2023-10-20 00:00:00',1),(7,120,'mini.jpg','How are you doing today?\r\n','Help, /help, Call manager, /manager','2023-10-20 00:00:00',1),(8,1,'mini.jpg','Give me some feedback please','None','2023-10-20 00:00:00',1),(9,1440,' ','Концерт состоится завтра, 4 ноября в 19 ч 00 м (GMT+3)',' ','2023-11-04 16:00:00',2),(10,45,' ','Концерт начинается через 45 минут!\r\nСсылка на концерт: https://meet.google.com/',' ','2023-11-04 16:00:00',2),(11,5,' ','Концерт уже почти здесь, присоединяйтесь!\r\nСсылка на концерт: https://meet.google.com/',' ','2023-11-04 16:00:00',2),(12,5,'mini_sin.jpg','Концерт окончен, но музыка вечна!\r\nПриходите к нам на вокал!','None','2023-10-04 18:00:00',2);
/*!40000 ALTER TABLE `telebot_sched` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Table structure for table `telebot_users`
--
DROP TABLE IF EXISTS `telebot_users`;
CREATE TABLE `telebot_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chat_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `lastupd` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `lastmsg` text,
  `Sub` tinyint(1) NOT NULL DEFAULT '0',
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `step` smallint DEFAULT '0',
  `email` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
;
--
-- Table structure for table `telebot_vars`
--
DROP TABLE IF EXISTS `telebot_vars`;
CREATE TABLE `telebot_vars` (
  `id` int NOT NULL AUTO_INCREMENT,
  `param` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `value` varchar(3800) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
;
--
-- Dumping data for table `telebot_vars`
--
LOCK TABLES `telebot_vars` WRITE;
/*!40000 ALTER TABLE `telebot_vars` DISABLE KEYS */;
INSERT INTO `telebot_vars` VALUES (1,'imgtosend','Asya-B-aa250.jpg'),(2,'pdftosend','guide.pdf'),(3,'msg1','I do not understand. Press \'help\' for assistance.'),(4,'msg2','Ivan Deus bot welcomes you! To get file press \'guide\' or press \'help\' for all available commands '),(5,'msg3','Super guide! Enjoy! It is the best.'),(6,'msg4','This is a help message. Try /start or \'guide\'. \r\nYou can subscribe with \'sub\' and undo with \'unsub\'.\r\n');
/*!40000 ALTER TABLE `telebot_vars` ENABLE KEYS */;
UNLOCK TABLES;
-- Dump completed on 2023-10-25 23:22:23
 
'''

# Credentials put here
bot_token = "xxx:xxx"
admin_name = "ivan"
# Database connection parameters
db_host = "localhost"
db_username = "xxx"
db_password = "xxx"
db_name = "xxx"
# MySQL socket path
mysql_unix_socket = "/var/run/mysqld/mysqld.sock"


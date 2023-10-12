# Ivan Deus telebot py cfg

# DB construction, copy this to MySQL to create a new table
###
'''...
-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
-- Table structure for table `telebot_admins`

DROP TABLE IF EXISTS `telebot_admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telebot_admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `chat_id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `message_id` varchar(255) DEFAULT NULL,
  `pendingmsg` tinyint(1) NOT NULL DEFAULT '0',
  `chatmngr` smallint DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `telebot_chats`
--
DROP TABLE IF EXISTS `telebot_chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telebot_chats` (
  `id` int NOT NULL AUTO_INCREMENT,
  `uchat_id` varchar(255) NOT NULL,
  `mngchat_id` varchar(255) NOT NULL,
  `umsg` varchar(1500) NOT NULL,
  `mngmsg` varchar(1500) NOT NULL,
  `lastupd` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Table structure for table `telebot_users`
--
DROP TABLE IF EXISTS `telebot_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
-- Dump completed 
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
# Files to send
imgtosend = 'Asya-B-aa250.jpg'
pdftosend = 'guide.pdf'


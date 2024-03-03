# Ivan Deus telebot py cfg
# DB construction, copy this into MySQL to create a new tables:
###
'''
-- MySQL dump 10.13  Distrib 8.0.34, for Linux (x86_64)
-- ------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `telebot_admins`
--

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
  `passwd` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

-- Table structure for table `telebot_sched`
--

DROP TABLE IF EXISTS `telebot_sched`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telebot_sched`
--

LOCK TABLES `telebot_sched` WRITE;
/*!40000 ALTER TABLE `telebot_sched` DISABLE KEYS */;
INSERT INTO `telebot_sched` VALUES (1,1,'mini.jpg','This is a first message from series of scheduled messages from bot','Help, /help','2023-10-20 00:00:00',1),(2,4,'mini.jpg','Should you stay or should you go?','Subscribe, /sub, Unsubscribe, /unsub, Call manager, /manager','2023-10-20 00:00:00',1),(3,24,'mini.jpg','Please stay with me...','Help, /help, Call manager, /manager','2023-10-20 00:00:00',1),(4,6,'mini.jpg','4th time is the churm!\r\nHey~\r\nHow are you?','Help!, /help','2023-10-20 00:00:00',1),(5,60,'mini.jpg','This is the message number 5','None','2023-10-20 00:00:00',1),(6,120,'mini.jpg','Доброго дня!\r\n“Желаю научиться импровизировать и впечатлять слушателей своей импровизацией. Как это сделать?” Ася расскажет, как научиться этой науке. \'#АсяПишет\'\r\n\r\n','None','2023-10-20 00:00:00',99),(7,120,'mini.jpg','How are you doing today?\r\n','Help, /help, Call manager, /manager','2023-10-20 00:00:00',99),(8,1,'mini.jpg','Give me some feedback please','None','2023-10-20 00:00:00',99),(9,1440,' ','Концерт состоится завтра, 4 ноября в 19 ч 00 м (GMT+3)',' ','2023-11-04 16:00:00',2),(10,45,' ','Концерт начинается через 45 минут!\r\nСсылка на концерт: https://meet.google.com/',' ','2023-11-04 16:00:00',2),(11,5,' ','Концерт уже почти здесь, присоединяйтесь!\r\nСсылка на концерт: https://meet.google.com/',' ','2023-11-04 16:00:00',2),(12,5,'mini_sin.jpg','Концерт окончен, но музыка вечна!\r\nПриходите к нам на вокал!','None','2023-10-04 18:00:00',2);
/*!40000 ALTER TABLE `telebot_sched` ENABLE KEYS */;
UNLOCK TABLES;

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
  `email` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

-- Table structure for table `telebot_vars`
--

DROP TABLE IF EXISTS `telebot_vars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telebot_vars` (
  `id` int NOT NULL AUTO_INCREMENT,
  `param` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  `value` varchar(3800) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Dumping data for table `telebot_vars`
--

LOCK TABLES `telebot_vars` WRITE;
/*!40000 ALTER TABLE `telebot_vars` DISABLE KEYS */;
INSERT INTO `telebot_vars` VALUES (1,'imgtosend','Asya-B-aa250.jpg'),(2,'pdftosend','guide.pdf'),(3,'msg1','I do not understand. Press \'help\' for assistance :/\r\nI am truly deeply terribly sorry.'),(4,'msg2','Ivan Deus bot welcomes you! To get file press \'guide\' or press \'help\' for all available commands '),(5,'msg3','Super guide! Enjoy! It is the best.'),(6,'msg4','This is a help message. Try /start or \'guide\'. \r\nYou can subscribe with \'sub\' and undo with \'unsub\'.\r\n'),(15,'massmessage1','This is it, you got a fortune! \r\nIt is your lucky day :)\r\nDon\'t worry, be happy!'),(16,'poll_inform','Thanks for voting!'),(17,'poll_option','Red; Green; Blue'),(18,'poll_question','What is your favorite color?');
/*!40000 ALTER TABLE `telebot_vars` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed
 
'''

# Credentials put here
bot_token = "xxx:xxx"
# define local port for webhook
bot_lport = 1005
# Database connection parameters
db_host = "localhost"
db_username = "xxx"
db_password = "xxx"
db_name = "xxx"
# MySQL socket path
mysql_unix_socket = "/var/run/mysqld/mysqld.sock"
#paths
install_path = "/var/www"
logfpath = "/var/log/telebot1x.log"


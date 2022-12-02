-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: helpinghands
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `chats`
--

DROP TABLE IF EXISTS `chats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chats` (
  `chat_id` int NOT NULL AUTO_INCREMENT,
  `chat_name` varchar(40) DEFAULT NULL,
  `chat_admin_id` int DEFAULT NULL,
  `chat_creator_id` int DEFAULT NULL,
  `participants` int DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`chat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chats`
--

LOCK TABLES `chats` WRITE;
/*!40000 ALTER TABLE `chats` DISABLE KEYS */;
INSERT INTO `chats` VALUES (1,'Donation Logistics group - chat',1,1,NULL,'2022-04-05 20:30:18','2022-04-06 10:46:50'),(2,'Medicine Delivery group - chat',1,1,NULL,'2022-04-05 20:37:28','2022-04-05 20:37:28'),(3,'Driving Paitents to Appoi group - chat',1,1,NULL,'2022-04-05 20:43:50','2022-04-05 20:43:50'),(4,'Soup Kitchen Chef group - chat',2,2,NULL,'2022-04-05 20:52:30','2022-04-05 20:52:30'),(5,'Lunch Server group - chat',2,2,NULL,'2022-04-05 20:59:03','2022-04-05 20:59:03'),(6,'Kitchen Porter group - chat',2,2,NULL,'2022-04-05 21:03:05','2022-04-06 10:46:15'),(7,'Red Cross - Matty Cash',1,1,NULL,'2022-04-06 10:01:01','2022-04-06 10:21:51'),(8,'Food Stop - Matty Cash',2,2,NULL,'2022-04-06 10:07:21','2022-04-06 10:26:58'),(9,'Red Cross - Tyrone Mings',1,1,NULL,'2022-04-06 10:11:10','2022-04-06 10:11:10'),(10,'Red Cross - Emi Martinez',1,1,NULL,'2022-04-06 10:14:48','2022-04-06 10:22:06'),(11,'Red Cross - Carla Ward',1,1,NULL,'2022-04-06 10:18:49','2022-04-06 10:18:49'),(12,'Red Cross - lehmann',1,1,NULL,'2022-04-06 10:21:17','2022-04-06 10:22:09');
/*!40000 ALTER TABLE `chats` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-06 10:49:20

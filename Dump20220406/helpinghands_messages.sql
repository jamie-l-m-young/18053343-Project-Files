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
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `message_id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int DEFAULT NULL,
  `chat_id` int DEFAULT NULL,
  `content` longtext,
  `message_time` datetime DEFAULT NULL,
  PRIMARY KEY (`message_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,3,7,'cafu1982 has applied to opportinity: Medicine Delivery','2022-04-06 10:01:01'),(2,3,7,'cafu1982 has withdrawn from your opportinity: Donation Logistics','2022-04-06 10:01:17'),(3,3,7,'cafu1982 has withdrawn from your opportinity: Driving Paitents to Appointments','2022-04-06 10:01:18'),(4,3,7,'cafu1982 has withdrawn from your opportinity: Medicine Delivery','2022-04-06 10:01:19'),(5,3,7,'cafu1982 has applied to opportinity: Donation Logistics','2022-04-06 10:06:04'),(6,3,7,'cafu1982 has applied to opportinity: Driving Paitents to Appointments','2022-04-06 10:06:43'),(7,3,8,'cafu1982 has applied to opportinity: Lunch Server','2022-04-06 10:07:21'),(8,3,8,'cafu1982 has applied to opportinity: Kitchen Porter','2022-04-06 10:07:37'),(9,4,9,'tm05 has applied to opportinity: Donation Logistics','2022-04-06 10:11:10'),(10,5,10,'dibu has applied to opportinity: Donation Logistics','2022-04-06 10:14:48'),(11,6,11,'wardie has applied to opportinity: Donation Logistics','2022-04-06 10:18:49'),(12,7,12,'Alisha Lehmann has applied to opportinity: Donation Logistics','2022-04-06 10:21:17'),(13,1,7,'redcross has been enrolled into: Donation Logistics','2022-04-06 10:21:51'),(14,1,1,'Welcome Matty Cash','2022-04-06 10:21:51'),(15,1,10,'redcross has been enrolled into: Donation Logistics','2022-04-06 10:22:06'),(16,1,1,'Welcome Emi Martinez','2022-04-06 10:22:06'),(17,1,12,'redcross has been enrolled into: Donation Logistics','2022-04-06 10:22:09'),(18,1,1,'Welcome lehmann','2022-04-06 10:22:09'),(19,7,1,'Alisha Lehmann has requested reference for Donation Logistics','2022-04-06 10:25:14'),(20,3,1,'cafu1982 has requested reference for Donation Logistics','2022-04-06 10:26:07'),(21,2,8,'foodstop has been enrolled into: Kitchen Porter','2022-04-06 10:26:58'),(22,2,6,'Welcome Matty Cash','2022-04-06 10:26:58'),(23,1,1,'redcross has writen a reference for Donation Logistics','2022-04-06 10:28:07'),(24,1,1,'redcross has writen a reference for Donation Logistics','2022-04-06 10:28:37'),(25,3,6,'cafu1982 has requested reference for Kitchen Porter','2022-04-06 10:45:41'),(26,2,6,'foodstop has writen a reference for Kitchen Porter','2022-04-06 10:46:15'),(27,7,1,'Alisha Lehmann has requested reference for Donation Logistics','2022-04-06 10:46:50');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-06 10:49:21

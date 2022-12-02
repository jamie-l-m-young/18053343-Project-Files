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
-- Table structure for table `opportunity`
--

DROP TABLE IF EXISTS `opportunity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `opportunity` (
  `opportunity_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `discription` text,
  `has_dbs` bit(1) DEFAULT NULL,
  `day_needed` varchar(15) DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `finish_time` time DEFAULT NULL,
  `address_id` int DEFAULT NULL,
  `poster_id` int DEFAULT NULL,
  PRIMARY KEY (`opportunity_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opportunity`
--

LOCK TABLES `opportunity` WRITE;
/*!40000 ALTER TABLE `opportunity` DISABLE KEYS */;
INSERT INTO `opportunity` VALUES (1,'Donation Logistics','We need people to help manage the distribution of food and medicine. We need people on monday between 11:00 - 15:00. The ideal volunteer would have some experiance with management and orginsation within a business setting.',_binary '\0','Monday','11:00:00','15:00:00',1,1),(2,'Medicine Delivery','We are looking for a volunteer to deliver medicine to people who can\'t leave there houses. We are looking for people between 13:00 - 18:00 on monday. You will need to be DBS checked as the people you will be helping may be vulnerable. You must have a drivers licence.',_binary '','Monday','13:00:00','18:00:00',2,1),(3,'Driving Paitents to Appointments','Many people are unable to take public transport and don\'t access to a car. You will be taking people to their doctors appointments and back home. You will need to have access to a car and be DBS checked as some of the people you are helping may be vulnerable. This will take place on Friday from 09:00 - 13:00',_binary '','Friday','13:00:00','18:00:00',3,1),(4,'Soup Kitchen Chef','We need a chef to prep the ingredents for the day. This would be great expirence for any young chef looking to get expirence within the cooking industry. We need you from 07:00 - 09:00 on wednesdays',_binary '\0','Wednesday','07:00:00','09:00:00',4,2),(5,'Lunch Server','We need someone to help set up for the thursday midday serving and serve the food.',_binary '\0','Thursday','11:00:00','14:00:00',5,2),(6,'Kitchen Porter','We need a volunteer to clean the dishes and pans used by the kitchen and help with the clean down after the friday afternoon serving.',_binary '\0','Friday','17:00:00','19:00:00',5,2);
/*!40000 ALTER TABLE `opportunity` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-06 10:49:19

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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `hash` blob,
  `is_charity` bit(1) DEFAULT NULL,
  `address_id` int DEFAULT NULL,
  `phone` varchar(12) DEFAULT NULL,
  `has_dbs` bit(1) DEFAULT NULL,
  `real_name` varchar(100) DEFAULT NULL,
  `max_distance` int DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'redcross','redcross@redcross.com',_binary '$5$rounds=535000$ktHIW7dAv8IQhERt$UcMHenYolmKOmk4T7xaXLiCCVzr3K8oLXKeYo2wcBD9',_binary '',NULL,'07883756482',_binary '\0','Red Cross',0),(2,'foodstop','foodstop@foodstop.com',_binary '$5$rounds=535000$YFxg5TT0YvK363wy$0cvqc5WceYRRaAOmg/sHxxoXAbgXGaaqylNj91mqOu2',_binary '',NULL,'07463548562',_binary '\0','Food Stop',0),(3,'cafu1982','cafu1982@cafu1982.com',_binary '$5$rounds=535000$xYq6R1zZHDcyfxi4$MrI9dwIUJiv1kqOheeodlLG40LMMSJRBbrp93x74UG8',_binary '\0',6,'07880438956',_binary '','Matty Cash',25),(4,'tm05','tm05@tm05park.com',_binary '$5$rounds=535000$91gwnDPgBUZzMPWI$Af4n5DEKmWopX6OdqBnESDyR8V4B1kzocdX6lQ.98/9',_binary '\0',NULL,'08446375843',_binary '','Tyrone Mings',29),(5,'dibu','dibu@holtendbibu.com',_binary '$5$rounds=535000$oShxJZH9khLwN.j7$LkWfv9jOqDV00JT5fd/FDjBthAX9Jl8G.6JHddjYtUC',_binary '\0',NULL,'08774638563',_binary '','Emi Martinez',11),(6,'wardie','wardie@wardiesword.com',_binary '$5$rounds=535000$uLqEHfLB52xBsl.B$GI8eNOnphKBG8P0vvk2ILGouQWttfAdJNtIZN6ERc61',_binary '\0',NULL,'07884038574',_binary '','Carla Ward',13),(7,'Alisha Lehmann','ehmann@imalehmann',_binary '$5$rounds=535000$.kfmjLpwDIlpfGmE$jnGNunLxALR92BacZjGYf7v38SYl/Fo5t79rCGNOFb9',_binary '\0',NULL,'07884037583',_binary '','lehmann',16);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
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

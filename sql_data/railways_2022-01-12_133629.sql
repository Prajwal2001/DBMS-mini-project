-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: railways
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Temporary view structure for view `all_train_info`
--

DROP TABLE IF EXISTS `all_train_info`;
/*!50001 DROP VIEW IF EXISTS `all_train_info`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `all_train_info` AS SELECT 
 1 AS `train_no`,
 1 AS `train_name`,
 1 AS `stat_name`,
 1 AS `arrival_time`,
 1 AS `depart_time`,
 1 AS `seq_no`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `covers`
--

DROP TABLE IF EXISTS `covers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `covers` (
  `stat_id` int NOT NULL,
  `train_no` int NOT NULL,
  `arrival_time` time NOT NULL,
  `depart_time` time NOT NULL,
  `days` int NOT NULL DEFAULT '0',
  `seq_no` int NOT NULL,
  KEY `stat_id` (`stat_id`),
  KEY `train_no` (`train_no`),
  CONSTRAINT `covers_ibfk_1` FOREIGN KEY (`stat_id`) REFERENCES `stations` (`stat_id`) ON DELETE CASCADE,
  CONSTRAINT `covers_ibfk_2` FOREIGN KEY (`train_no`) REFERENCES `trains` (`train_no`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `covers`
--

/*!40000 ALTER TABLE `covers` DISABLE KEYS */;
INSERT INTO `covers` VALUES (200,1000,'00:30:00','00:31:00',0,1),(201,1000,'01:00:00','01:01:00',0,2),(202,1000,'02:00:00','02:01:00',0,3),(203,1000,'03:00:00','03:01:00',0,4),(204,1000,'04:00:00','04:01:00',0,5),(205,1000,'05:00:00','05:01:00',0,6),(206,1000,'06:00:00','06:01:00',0,7),(208,1002,'08:00:00','08:01:00',0,1),(206,1002,'09:00:00','09:01:00',0,2),(205,1002,'10:00:00','10:01:00',0,3),(203,1002,'11:00:00','11:01:00',0,4),(202,1002,'12:00:00','12:01:00',0,5),(201,1002,'13:00:00','13:01:00',0,6),(200,1002,'14:00:00','14:01:00',0,7),(200,1003,'20:00:00','20:01:00',0,1),(201,1003,'21:00:00','21:01:00',0,2),(202,1003,'22:00:00','22:01:00',0,3),(203,1003,'23:00:00','23:01:00',0,4),(204,1003,'00:00:00','00:01:00',1,5),(205,1003,'01:00:00','01:01:00',1,6),(206,1003,'02:00:00','02:01:00',1,7);
/*!40000 ALTER TABLE `covers` ENABLE KEYS */;

--
-- Table structure for table `passengers`
--

DROP TABLE IF EXISTS `passengers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passengers` (
  `p_id` int NOT NULL AUTO_INCREMENT,
  `p_name` varchar(25) NOT NULL,
  `p_age` int NOT NULL,
  `seat_no` int NOT NULL,
  `pnr` int NOT NULL,
  PRIMARY KEY (`p_id`),
  KEY `pnr` (`pnr`),
  CONSTRAINT `passengers_ibfk_1` FOREIGN KEY (`pnr`) REFERENCES `tickets` (`pnr`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=140 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passengers`
--

/*!40000 ALTER TABLE `passengers` DISABLE KEYS */;
INSERT INTO `passengers` VALUES (118,'Prajwal',21,365,558),(119,'Parashuram',52,366,558),(120,'Veena',46,367,558),(121,'Shreesha S',21,173,559),(122,'Prajwal Kulkarni',21,174,559),(128,'Prajwal Kulkarni',21,1,562),(129,'Prajwal G',20,2,562),(137,'Veena',46,425,567),(138,'Bhoomika Kulkarni',11,426,567),(139,'Prajwal',21,387,568);
/*!40000 ALTER TABLE `passengers` ENABLE KEYS */;

--
-- Table structure for table `stations`
--

DROP TABLE IF EXISTS `stations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stations` (
  `stat_id` int NOT NULL AUTO_INCREMENT,
  `stat_name` varchar(25) NOT NULL,
  `stat_loc` varchar(25) NOT NULL,
  PRIMARY KEY (`stat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=209 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stations`
--

/*!40000 ALTER TABLE `stations` DISABLE KEYS */;
INSERT INTO `stations` VALUES (200,'A','A'),(201,'B','B'),(202,'C','C'),(203,'D','D'),(204,'E','E'),(205,'F','F'),(206,'G','G'),(207,'H','H'),(208,'I','I');
/*!40000 ALTER TABLE `stations` ENABLE KEYS */;

--
-- Table structure for table `tickets`
--

DROP TABLE IF EXISTS `tickets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tickets` (
  `pnr` int NOT NULL AUTO_INCREMENT,
  `from_station` int NOT NULL,
  `to_station` int NOT NULL,
  `booking_date` date NOT NULL,
  `travel_date` date NOT NULL,
  `user_id` int NOT NULL,
  `train_no` int NOT NULL,
  `price` int DEFAULT NULL,
  PRIMARY KEY (`pnr`),
  KEY `user_id` (`user_id`),
  KEY `train_no` (`train_no`),
  KEY `from_station` (`from_station`),
  KEY `to_station` (`to_station`),
  CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `tickets_ibfk_2` FOREIGN KEY (`train_no`) REFERENCES `trains` (`train_no`) ON DELETE CASCADE,
  CONSTRAINT `tickets_ibfk_3` FOREIGN KEY (`from_station`) REFERENCES `stations` (`stat_id`) ON DELETE CASCADE,
  CONSTRAINT `tickets_ibfk_4` FOREIGN KEY (`to_station`) REFERENCES `stations` (`stat_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=569 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (558,200,206,'2022-01-10','2022-01-26',7,1003,180),(559,200,206,'2022-01-10','2022-01-20',8,1003,120),(562,200,205,'2022-01-10','2022-01-20',9,1003,100),(567,201,206,'2022-01-11','2022-01-20',6,1003,100),(568,200,203,'2022-01-11','2022-01-20',6,1000,30);
/*!40000 ALTER TABLE `tickets` ENABLE KEYS */;

--
-- Table structure for table `trains`
--

DROP TABLE IF EXISTS `trains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trains` (
  `train_no` int NOT NULL AUTO_INCREMENT,
  `train_name` varchar(25) NOT NULL,
  PRIMARY KEY (`train_no`)
) ENGINE=InnoDB AUTO_INCREMENT=1005 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trains`
--

/*!40000 ALTER TABLE `trains` DISABLE KEYS */;
INSERT INTO `trains` VALUES (1000,'A-train'),(1002,'C-train'),(1003,'B-train');
/*!40000 ALTER TABLE `trains` ENABLE KEYS */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(25) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_name` (`user_name`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (6,'prajwal k','kulkarniprajwal.01@gmail.com','e99a18c428cb38d5f260853678922e03'),(7,'parashuram','kulkarniparashuram@gmail.com','e99a18c428cb38d5f260853678922e03'),(8,'Shreesha S','shreesha.082@gmail.com','e99a18c428cb38d5f260853678922e03'),(9,'Prajwal G','prajwalvallabha06@gmail.com','e99a18c428cb38d5f260853678922e03');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

--
-- Final view structure for view `all_train_info`
--

/*!50001 DROP VIEW IF EXISTS `all_train_info`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `all_train_info` AS select `t`.`train_no` AS `train_no`,`t`.`train_name` AS `train_name`,`s`.`stat_name` AS `stat_name`,`c`.`arrival_time` AS `arrival_time`,`c`.`depart_time` AS `depart_time`,`c`.`seq_no` AS `seq_no` from ((`trains` `t` join `stations` `s`) join `covers` `c` on(((`t`.`train_no` = `c`.`train_no`) and (`s`.`stat_id` = `c`.`stat_id`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-01-12 13:37:08

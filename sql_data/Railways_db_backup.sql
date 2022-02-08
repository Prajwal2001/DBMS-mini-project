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
-- Temporary view structure for view `available_seats`
--

DROP TABLE IF EXISTS `available_seats`;
/*!50001 DROP VIEW IF EXISTS `available_seats`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `available_seats` AS SELECT 
 1 AS `pnr`,
 1 AS `travel_date`,
 1 AS `train_no`,
 1 AS `no_of_seats`,
 1 AS `seats_reserved`*/;
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
INSERT INTO `covers` VALUES (210,1000,'05:30:00','06:00:00',0,1),(211,1000,'06:12:00','06:20:00',0,2),(212,1000,'07:02:00','07:10:00',0,3),(213,1000,'08:15:00','08:20:00',0,4),(214,1000,'10:15:00','10:20:00',0,5),(215,1000,'10:27:00','10:30:00',0,6),(216,1000,'10:48:00','10:55:00',0,7),(217,1000,'12:00:00','12:30:00',0,8),(210,1001,'21:30:00','22:05:00',0,1),(211,1001,'22:17:00','22:20:00',0,2),(212,1001,'23:07:00','23:10:00',0,3),(213,1001,'00:30:00','00:35:00',1,4),(214,1001,'02:35:00','02:40:00',1,5),(215,1001,'02:55:00','03:00:00',1,6),(216,1001,'03:15:00','03:20:00',1,7),(217,1001,'05:45:00','06:15:00',1,8),(217,1002,'13:00:00','13:40:00',0,1),(216,1002,'15:07:00','15:09:00',0,2),(215,1002,'15:29:00','15:31:00',0,3),(214,1002,'15:45:00','15:47:00',0,4),(213,1002,'17:45:00','17:50:00',0,5),(212,1002,'19:08:00','19:10:00',0,6),(211,1002,'20:15:00','20:17:00',0,7),(210,1002,'21:00:00','21:30:00',0,8),(217,1003,'22:20:00','22:30:00',0,1),(216,1003,'00:08:00','00:10:00',1,2),(215,1003,'00:29:00','00:31:00',1,3),(214,1003,'00:48:00','00:50:00',1,4),(213,1003,'03:03:00','03:05:00',1,5),(212,1003,'04:28:00','04:30:00',1,6),(211,1003,'05:50:00','05:52:00',1,7),(210,1003,'06:30:00','06:45:00',1,8),(210,1004,'18:00:00','18:05:00',0,1),(219,1004,'18:14:00','18:16:00',0,2),(220,1004,'18:26:00','18:28:00',0,3),(221,1004,'18:32:00','18:34:00',0,4),(222,1004,'19:02:00','19:04:00',0,5),(223,1004,'19:51:00','19:55:00',0,6),(224,1004,'20:18:00','20:20:00',0,7),(225,1004,'21:10:00','21:30:00',0,8),(210,1005,'19:00:00','19:05:00',0,1),(219,1005,'19:14:00','19:16:00',0,2),(220,1005,'19:26:00','19:28:00',0,3),(221,1005,'19:32:00','19:34:00',0,4),(222,1005,'20:02:00','20:04:00',0,5),(223,1005,'20:51:00','20:55:00',0,6),(224,1005,'21:18:00','21:20:00',0,7),(225,1005,'22:10:00','22:30:00',0,8),(210,1006,'21:00:00','21:05:00',0,8),(219,1006,'21:14:00','21:16:00',0,7),(220,1006,'21:26:00','21:28:00',0,6),(221,1006,'21:32:00','21:34:00',0,5),(222,1006,'22:02:00','22:04:00',0,4),(223,1006,'22:51:00','22:55:00',0,3),(224,1006,'23:18:00','23:20:00',0,2),(225,1006,'00:10:00','00:30:00',1,1),(210,1007,'23:00:00','23:05:00',0,8),(219,1007,'23:14:00','23:16:00',0,7),(220,1007,'23:26:00','23:28:00',0,6),(221,1007,'23:32:00','23:34:00',0,5),(222,1007,'00:02:00','00:04:00',1,4),(223,1007,'00:51:00','00:55:00',1,3),(224,1007,'01:18:00','01:20:00',1,2),(225,1007,'02:10:00','02:30:00',1,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=200 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passengers`
--

/*!40000 ALTER TABLE `passengers` DISABLE KEYS */;
INSERT INTO `passengers` VALUES (196,'Prajwal Kulkarni',21,1,598),(197,'Prajwal G',20,2,598),(198,'Parashuram',52,1,599),(199,'Veena',46,2,599);
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
) ENGINE=InnoDB AUTO_INCREMENT=226 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stations`
--

/*!40000 ALTER TABLE `stations` DISABLE KEYS */;
INSERT INTO `stations` VALUES (210,'KSR Bengaluru','Bengaluru'),(211,'YPR Yesvantapur','Yesvantapur'),(212,'Tumkur','Tumkuru'),(213,'Arsikere Jn','Arsikere'),(214,'Davangere','Davangere'),(215,'Harihara','Harihara'),(216,'Ranibennur','RaniBennur'),(217,'Hubli Jn','Hubli'),(219,'Bengaluru Cant','Bengaluru Cant'),(220,'Baiyyappanahalli','Baiyyappanahalli'),(221,'KR Puram','KR Puram'),(222,'Malur','Malur'),(223,'Bangarpete','Bangarpete'),(224,'Champion','Champion Reef'),(225,'Oorgaum','Oorgaum');
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
) ENGINE=InnoDB AUTO_INCREMENT=600 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tickets`
--

/*!40000 ALTER TABLE `tickets` DISABLE KEYS */;
INSERT INTO `tickets` VALUES (598,210,217,'2022-02-07','2022-02-16',6,1000,140),(599,210,213,'2022-02-07','2022-02-16',6,1001,60);
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
) ENGINE=InnoDB AUTO_INCREMENT=1008 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trains`
--

/*!40000 ALTER TABLE `trains` DISABLE KEYS */;
INSERT INTO `trains` VALUES (1000,'Janshatabdi Express'),(1001,'Rani Chennamma Express'),(1002,'Janshatabdi Exp'),(1003,'Rani Chennamma'),(1004,'Lalbagh Express'),(1005,'Brindavan Express'),(1006,'Lalbagh Exp'),(1007,'Brindavan Exp');
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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (6,'prajwal k','kulkarniprajwal.01@gmail.com','e99a18c428cb38d5f260853678922e03'),(7,'parashuram','kulkarniparashuram@gmail.com','e99a18c428cb38d5f260853678922e03'),(8,'Shreesha S','shreesha.082@gmail.com','e99a18c428cb38d5f260853678922e03'),(9,'Prajwal G','prajwalvallabha06@gmail.com','e99a18c428cb38d5f260853678922e03'),(10,'sakshi k','sakshiak111@gmail.com','e99a18c428cb38d5f260853678922e03'),(11,'abcde','abcd@gmail.com','e99a18c428cb38d5f260853678922e03');
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

--
-- Final view structure for view `available_seats`
--

/*!50001 DROP VIEW IF EXISTS `available_seats`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_unicode_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `available_seats` AS select `t`.`pnr` AS `pnr`,`t`.`travel_date` AS `travel_date`,`tr`.`train_no` AS `train_no`,count(`p`.`p_id`) AS `no_of_seats`,max(`p`.`seat_no`) AS `seats_reserved` from (`trains` `tr` left join (`tickets` `t` join `passengers` `p` on((`t`.`pnr` = `p`.`pnr`))) on((`t`.`train_no` = `tr`.`train_no`))) group by `t`.`pnr` order by `t`.`pnr` */;
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

-- Dump completed on 2022-02-08 11:25:29

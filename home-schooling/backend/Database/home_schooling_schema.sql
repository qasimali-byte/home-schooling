CREATE DATABASE  IF NOT EXISTS `home_schooling` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `home_schooling`;
-- MySQL dump 10.13  Distrib 8.0.34, for macos13 (arm64)
--
-- Host: 127.0.0.1    Database: home_schooling
-- ------------------------------------------------------
-- Server version	8.1.0

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
-- Table structure for table `child`
--

DROP TABLE IF EXISTS `child`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `child` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `address` varchar(255) NOT NULL,
  `state` varchar(45) NOT NULL,
  `post_code` varchar(45) NOT NULL,
  `age` varchar(45) NOT NULL,
  `school_year` varchar(45) NOT NULL,
  `start_date` date NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id_idx` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `child`
--

LOCK TABLES `child` WRITE;
/*!40000 ALTER TABLE `child` DISABLE KEYS */;
INSERT INTO `child` VALUES (2,'Junaid','Baluoch','Street Dr.Captain Fazal Elahi  Attock Road Fateh Jang ,District Attock','Punjab','43350','12','Foundation Year','2023-12-14',2),(3,'JHON','Baluoch','Street Dr.Captain Fazal Elahi  Attock Road Fateh Jang ,District Attock','Punjab','43350','23','1 YEAR','2023-12-21',2);
/*!40000 ALTER TABLE `child` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `invoice`
--

DROP TABLE IF EXISTS `invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `invoice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subscription_id` int NOT NULL,
  `price` varchar(45) NOT NULL,
  `date_created` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_subscription_id_idx` (`subscription_id`),
  CONSTRAINT `fk_subscription_id` FOREIGN KEY (`subscription_id`) REFERENCES `subscriptions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `invoice`
--

LOCK TABLES `invoice` WRITE;
/*!40000 ALTER TABLE `invoice` DISABLE KEYS */;
INSERT INTO `invoice` VALUES (1,1,'15','2023-12-21'),(2,2,'12','2023-12-21'),(3,3,'12','2023-12-21'),(4,4,'15','2023-12-28'),(5,5,'15','2023-12-28'),(6,6,'130','2023-12-28'),(7,7,'15','2023-12-28'),(8,8,'15','2023-12-28'),(9,9,'15','2023-12-29'),(10,10,'15','2023-12-30'),(11,11,'15','2024-01-01');
/*!40000 ALTER TABLE `invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plan`
--

DROP TABLE IF EXISTS `plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `duration` varchar(45) NOT NULL,
  `price` float NOT NULL,
  `isActive` tinyint NOT NULL,
  `date_created` date NOT NULL,
  `name` varchar(45) NOT NULL,
  `extra_data` json NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plan`
--

LOCK TABLES `plan` WRITE;
/*!40000 ALTER TABLE `plan` DISABLE KEYS */;
INSERT INTO `plan` VALUES (1,'30',12.99,1,'2023-12-21','Basic Package','{\"features\": [\"Online Dashboard\", \"AI-driven reporting\", \"Export to PDF or DOC\"]}'),(2,'30',15.99,1,'2023-12-21','Premium Package','{\"features\": [\"Online Dashboard\", \"AI-driven reporting\", \"Export to PDF or DOC\", \"AI-driven Insights & Recommendations\"]}'),(3,'365',161.88,1,'2023-12-21','Elite Package','{\"features\": [\"Online Dashboard\", \"AI-driven reporting\", \"Export to PDF or DOC\", \"AI-driven Insights & Recommendations\"]}');
/*!40000 ALTER TABLE `plan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscriptions`
--

DROP TABLE IF EXISTS `subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subscriptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `plan_id` int NOT NULL,
  `isActive` tinyint NOT NULL,
  `date_created` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id_idx` (`user_id`),
  KEY `fk_plan_id_idx` (`plan_id`),
  CONSTRAINT `fk_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `plan` (`id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscriptions`
--

LOCK TABLES `subscriptions` WRITE;
/*!40000 ALTER TABLE `subscriptions` DISABLE KEYS */;
INSERT INTO `subscriptions` VALUES (1,2,2,1,'2023-12-21'),(2,3,1,1,'2023-12-21'),(3,4,1,1,'2023-12-21'),(4,5,2,1,'2023-12-28'),(5,6,2,1,'2023-12-28'),(6,7,3,1,'2023-12-28'),(7,8,2,1,'2023-12-28'),(8,9,2,1,'2023-12-28'),(9,10,2,1,'2023-12-29'),(10,11,2,1,'2023-12-30'),(11,12,2,1,'2024-01-01');
/*!40000 ALTER TABLE `subscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `address` varchar(255) NOT NULL,
  `state` varchar(45) NOT NULL,
  `post_code` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `date_created` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'Junaid','Baluoch','Street Dr.Captain Fazal Elahi  Attock Road Fateh Jang ,District Attock','Punjab','43350','junaiddaud767@gmail.com','scrypt:32768:8:1$9aeqcbHRcAIoDi9t$57065f0ce7e41cf0df3d7c2a03a3b3321624b9bdadd3afbcd80fc3616fd5edc261c3e516b2eaef4c290ec4f5ba4a9c79d9f1045a0ea4f599c3f60bcef54a902d','2023-12-21'),(3,'Junaid','Baluoch','Street Dr.Captain Fazal Elahi  Attock Road Fateh Jang ,District Attock','Punjab','43350','junaiddaud@gmail.com','scrypt:32768:8:1$I600lnBjrPq3iD2w$1d65d4c58143ee198358d2f344e7852f154c32c65a51afed32874a1235e7f1987d2844427f69e6e160b6cbf286f26b19ff18b01b77d23f6e1262737a2b4edcd7','2023-12-21'),(4,'Junaid','daus','asdf','sadf','asdf','admin@gmail.com','scrypt:32768:8:1$PY8QkMvN9U2BA7QJ$8c2be629826be968a1578793ff32de58bca5fda0bc09e527fb65bfc5636bb7ac4c55627608f5dfe72d2ea7da2f29d4c231b21392ce8af872c46892b7614d1b7f','2023-12-21'),(5,'Junaid','Baluoch','Street Dr.Captain Fazal Elahi  Attock Road Fateh Jang ,District Attock','Punjab','43350','junaiddaud76777@gmail.com','scrypt:32768:8:1$AUGOOfezNd2AKd3w$3f8939b4a3b72edcc7946ba35a7101f723fbdaaf4c05a029b6e513b13cf6add5508893e480de92cec7455c923667da8e61dee6b9117790b41b6b2c276c8db542','2023-12-28'),(6,'Junaid','Baluoch','Street Dr.Captain Fazal Elahi  Attock Road Fateh Jang ,District Attock','Punjab','43350','junaiddaud7676@gmail.com','scrypt:32768:8:1$whjk4O7LW1UQchxm$73809b6ab2eab85ad4f6ec437b2bf6c7eec7ff1fbd2e58c2589c7a1d9a439c027c860fb9d40f2060fda5bef410ca5bffbd0ea3b847a4bccb8d1ed8169014bda5','2023-12-28'),(7,'Junaid','Baluoch','Street Dr.Captain Fazal Elahi  Attock Road Fateh Jang ,District Attock','Punjab','43350','junaiddaud4767@gmail.com','scrypt:32768:8:1$6LGepsKF2uVGcUwK$ade289005e66ea3489528ccd58574bae917de5e1e1242eac54633884085fb6b399c673ea6ad0ad86232e1289b3ded029a27c2ecece7049f73d371d37bdc431df','2023-12-28'),(8,'Junaid','Daud','saldkfj','WA','12345','junaid@gmail.com','scrypt:32768:8:1$nSlpyP9FCoFn1nj4$247d9d6be83773e388c584060f2ad5e55a8c186924453d8eba54e85180bd8ab1f1ea314dd12d80e538bd035b97c7311bc1ed499466e899c27cb9d375031636c7','2023-12-28'),(9,'Junaid','Baluoch','Street Dr.Captain Fazal Elahi  Attock Road Fateh Jang ,District Attock','Punjab','43350','junaiddaud7674@gmail.com','scrypt:32768:8:1$mZLq9NTGpFglWR7b$cf52cc69f6913e1cc720133341038df5f697e90c35ed5ea5c2b92bbece752ed5437213fe3f643b2a724a8b67de96e78e3882a51a8cfd5433dff0f7d822851b3c','2023-12-28'),(10,'Junaid','Baluoch','Street Dr.Captain Fazal Elahi  Attock Road Fateh Jang ,District Attock','Punjab','43350','junaiddaud76d7@gmail.com','scrypt:32768:8:1$CcKegk42tPComM0t$fdc70fd57b3080618fe234365cea42fd4cc4ffe261fbcc18b7d91d018e1e9f83136a619b68923bd8a4d09a2297b4dc997fd96291c46560fa07dcd2caf366ba2b','2023-12-29'),(11,'Junaid','Baluoch','Street Dr.Captain Fazal Elahi  Attock Road Fateh Jang ,District Attock','Queensland','43350','junaiddaud1767@gmail.com','scrypt:32768:8:1$3Vm5LSMCn8uDV15I$8da5340fc5f41fb5538e13c130edeca7219fde4556db283bd51b68a70dbd0d76c9f8f2601db89fea689b55c9482f11c0b6b0e0059a8fc62e7a277386fb22696a','2023-12-30'),(12,'Junaid','Daud','saldkfj','','','admin12@gmail.com','scrypt:32768:8:1$OvpWSNfg0icVqFNH$9f5b8a7756f6038ae4bc12f0a1d13c989e1598f7fbcd4d890baf8ed2ddb602b229d61c2e83513e74bd676c99766d9407d5b4cf750afecdd719db5498f3dc691b','2024-01-01');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-01 16:11:02

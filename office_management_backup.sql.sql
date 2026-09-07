-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: office_management
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `accounts_app_user`
--

DROP TABLE IF EXISTS `accounts_app_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_app_user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `profile_picture` varchar(100) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `designation` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `joining_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_app_user`
--

LOCK TABLES `accounts_app_user` WRITE;
/*!40000 ALTER TABLE `accounts_app_user` DISABLE KEYS */;
INSERT INTO `accounts_app_user` VALUES (3,'pbkdf2_sha256$1000000$te4ZM3AZIm2MNG9q3B8NLz$+gNCsDpn1AZxQ1nscdyyoFYzjitOxxIqkloB0GBu7q8=','2026-09-05 12:35:05.946714',1,'Admin@7005','','',1,1,'2026-08-17 04:44:34.718308','webcodeft@gmail.com',NULL,'','admin',NULL,NULL,'2026-08-17 04:44:35.156102',NULL),(4,'pbkdf2_sha256$1000000$BcNGlvAfSb8W80FBi0sUem$gjbwadtaWFrTCHs/V7EAOyQSln5RDnbHb4WwLRg3K+0=','2026-09-05 12:34:28.398183',0,'Palaksharma@27','Palak','Sharma',0,1,'2026-08-17 05:53:27.755408','palaksharmaa2004@gmail.com','98050 37005','','employee','Development','Software Developer','2026-08-17 05:53:28.196961','2026-08-01'),(5,'pbkdf2_sha256$1000000$KdROLuo4VLA6aFdBFMjytt$2jIP5ZTNKx687+vTpAs3ASVKUse9mPYAoqr9+ftpSCE=','2026-09-01 05:26:51.681410',0,'Pulkitjalani@123','Pulkit','Jalani',0,1,'2026-08-29 08:05:36.852076','pulkit@gmail.com','98286 18452','','employee','Development','Developer','2026-08-29 08:05:37.305610','2026-08-01'),(6,'pbkdf2_sha256$1000000$9DaCBBbSAikBEGNvyRLsoV$WLoM9vd2Tjmvh5jWQhG4b/teMHBryhM6t2ckZq40FEk=','2026-09-05 05:38:01.180462',0,'Sarikarangra@123','Sarika','Rangra',0,1,'2026-08-29 08:09:29.211262','sarikawebcodeft@gmail.com','62840 93876','','employee','SEO and Digital Marketing','SEO and Digital Marketing Executive','2026-08-29 08:09:29.654836','2025-04-01'),(7,'pbkdf2_sha256$1000000$XVNBjApgHRdF5Jr3kEmwhQ$bFkdEbLxjWZKI9n1aJAfzOT8UR4yAWK/Meb1J2PXZds=','2026-09-03 04:57:59.741774',0,'Anishamehta@123','Anisha','Mehta',0,1,'2026-08-29 08:12:50.726440','anishawebcodeft@gmail.com','78071 20880','','employee','Training, Designer','HR Executive','2026-08-29 08:12:51.165550','2021-12-01'),(8,'pbkdf2_sha256$1000000$v1CiyYAtPlq88piniOVm4O$4mGr+Gxb3K1YyOamb69KQrx00JXkSXQ+TIfBZDMlPUg=','2026-09-01 05:28:52.937365',0,'Seemasharma@123','Seema','Sharma',0,1,'2026-08-29 08:29:20.086691','seema@gmail.com','82190 32259','','employee','Software Development','Team Lead','2026-08-29 08:29:20.524790','2026-08-01');
/*!40000 ALTER TABLE `accounts_app_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_app_user_groups`
--

DROP TABLE IF EXISTS `accounts_app_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_app_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_app_user_groups_user_id_group_id_a88a51c1_uniq` (`user_id`,`group_id`),
  KEY `accounts_app_user_groups_group_id_c425a521_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_app_user_gr_user_id_131ad085_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_app_user` (`id`),
  CONSTRAINT `accounts_app_user_groups_group_id_c425a521_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_app_user_groups`
--

LOCK TABLES `accounts_app_user_groups` WRITE;
/*!40000 ALTER TABLE `accounts_app_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_app_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_app_user_user_permissions`
--

DROP TABLE IF EXISTS `accounts_app_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_app_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_app_user_user_p_user_id_permission_id_6ed1d9b0_uniq` (`user_id`,`permission_id`),
  KEY `accounts_app_user_us_permission_id_e4d2d1d9_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_app_user_us_permission_id_e4d2d1d9_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `accounts_app_user_us_user_id_b54f455d_fk_accounts_` FOREIGN KEY (`user_id`) REFERENCES `accounts_app_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_app_user_user_permissions`
--

LOCK TABLES `accounts_app_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_app_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_app_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_user'),(22,'Can change user',6,'change_user'),(23,'Can delete user',6,'delete_user'),(24,'Can view user',6,'view_user'),(25,'Can add student',7,'add_student'),(26,'Can change student',7,'change_student'),(27,'Can delete student',7,'delete_student'),(28,'Can view student',7,'view_student'),(29,'Can add task',8,'add_task'),(30,'Can change task',8,'change_task'),(31,'Can delete task',8,'delete_task'),(32,'Can view task',8,'view_task'),(33,'Can add attendance',9,'add_attendance'),(34,'Can change attendance',9,'change_attendance'),(35,'Can delete attendance',9,'delete_attendance'),(36,'Can view attendance',9,'view_attendance'),(37,'Can add project',10,'add_project'),(38,'Can change project',10,'change_project'),(39,'Can delete project',10,'delete_project'),(40,'Can view project',10,'view_project'),(41,'Can add client',11,'add_client'),(42,'Can change client',11,'change_client'),(43,'Can delete client',11,'delete_client'),(44,'Can view client',11,'view_client'),(45,'Can add Leave',12,'add_leave'),(46,'Can change Leave',12,'change_leave'),(47,'Can delete Leave',12,'delete_leave'),(48,'Can view Leave',12,'view_leave'),(49,'Can add Task Comment',13,'add_taskcomment'),(50,'Can change Task Comment',13,'change_taskcomment'),(51,'Can delete Task Comment',13,'delete_taskcomment'),(52,'Can view Task Comment',13,'view_taskcomment'),(53,'Can add student fee payment',14,'add_studentfeepayment'),(54,'Can change student fee payment',14,'change_studentfeepayment'),(55,'Can delete student fee payment',14,'delete_studentfeepayment'),(56,'Can view student fee payment',14,'view_studentfeepayment'),(57,'Can add todo',15,'add_todo'),(58,'Can change todo',15,'change_todo'),(59,'Can delete todo',15,'delete_todo'),(60,'Can view todo',15,'view_todo'),(61,'Can add Holiday',16,'add_holiday'),(62,'Can change Holiday',16,'change_holiday'),(63,'Can delete Holiday',16,'delete_holiday'),(64,'Can view Holiday',16,'view_holiday'),(65,'Can add chat message',17,'add_chatmessage'),(66,'Can change chat message',17,'change_chatmessage'),(67,'Can delete chat message',17,'delete_chatmessage'),(68,'Can view chat message',17,'view_chatmessage'),(69,'Can add user status',18,'add_userstatus'),(70,'Can change user status',18,'change_userstatus'),(71,'Can delete user status',18,'delete_userstatus'),(72,'Can view user status',18,'view_userstatus'),(73,'Can add Invoice',19,'add_invoice'),(74,'Can change Invoice',19,'change_invoice'),(75,'Can delete Invoice',19,'delete_invoice'),(76,'Can view Invoice',19,'view_invoice'),(77,'Can add Invoice Item',20,'add_invoiceitem'),(78,'Can change Invoice Item',20,'change_invoiceitem'),(79,'Can delete Invoice Item',20,'delete_invoiceitem'),(80,'Can view Invoice Item',20,'view_invoiceitem');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_attendance`
--

DROP TABLE IF EXISTS `core_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_attendance` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `status` varchar(20) NOT NULL,
  `remarks` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `employee_id` bigint NOT NULL,
  `check_in` time(6) DEFAULT NULL,
  `check_out` time(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_employee_attendance_per_day` (`employee_id`,`date`),
  KEY `core_attend_employe_7ab622_idx` (`employee_id`,`date`),
  KEY `core_attend_date_801bf5_idx` (`date`),
  KEY `core_attend_employe_9c61d1_idx` (`employee_id`,`status`),
  CONSTRAINT `core_attendance_employee_id_6327f987_fk_accounts_app_user_id` FOREIGN KEY (`employee_id`) REFERENCES `accounts_app_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_attendance`
--

LOCK TABLES `core_attendance` WRITE;
/*!40000 ALTER TABLE `core_attendance` DISABLE KEYS */;
INSERT INTO `core_attendance` VALUES (1,'2026-08-20','present','','2026-08-20 05:12:55.957934','2026-08-20 05:12:55.957934',4,NULL,NULL),(2,'2026-08-29','present','','2026-08-29 07:07:50.234193','2026-08-29 07:07:50.234193',4,NULL,NULL),(3,'2026-08-30','present','','2026-08-30 15:42:04.176471','2026-08-30 15:42:14.896111',7,'21:12:04.171943','21:12:14.896111'),(4,'2026-09-01','leave','Leave applied by employee.','2026-08-30 16:44:45.489035','2026-08-30 17:50:02.794017',7,NULL,NULL),(5,'2026-08-31','present','Checked out during normal checkout hours.','2026-08-31 05:28:48.560626','2026-08-31 10:33:10.960505',7,'10:58:00.000000','16:03:00.000000'),(6,'2026-08-31','present','Checked in.','2026-08-31 05:29:14.784709','2026-08-31 05:29:14.784709',4,'10:59:00.000000',NULL),(7,'2026-08-31','present','Checked in.','2026-08-31 05:29:26.731557','2026-08-31 05:29:26.731557',5,'10:59:00.000000',NULL),(8,'2026-08-31','present','Checked out during normal checkout hours.','2026-08-31 05:29:39.124718','2026-08-31 10:33:48.443732',6,'10:59:00.000000','16:03:00.000000'),(9,'2026-09-01','present','Checked in.','2026-09-01 05:25:25.232665','2026-09-01 05:25:25.232665',4,'10:55:00.000000',NULL),(10,'2026-09-01','present','Checked in.','2026-09-01 05:26:21.290664','2026-09-01 05:26:21.290664',6,'10:56:00.000000',NULL),(11,'2026-09-01','present','Checked in.','2026-09-01 05:27:13.374714','2026-09-01 05:27:13.374714',5,'10:57:00.000000',NULL),(12,'2026-09-01','present','Checked in.','2026-09-01 05:28:58.558052','2026-09-01 05:28:58.558052',8,'10:58:00.000000',NULL),(13,'2026-09-03','present','Checked in.','2026-09-03 04:56:37.090592','2026-09-03 04:56:37.090592',4,'10:26:00.000000',NULL),(14,'2026-09-03','absent','Automatically marked Absent after 11:00 AM.','2026-09-03 05:35:41.519550','2026-09-03 05:35:41.519550',5,NULL,NULL),(15,'2026-09-03','absent','Automatically marked Absent after 11:00 AM.','2026-09-03 05:35:41.526825','2026-09-03 05:35:41.526825',6,NULL,NULL),(16,'2026-09-03','absent','Automatically marked Absent after 11:00 AM.','2026-09-03 05:35:41.533179','2026-09-03 05:35:41.533179',7,NULL,NULL),(17,'2026-09-03','absent','Automatically marked Absent after 11:00 AM.','2026-09-03 05:35:41.538408','2026-09-03 05:35:41.538408',8,NULL,NULL),(18,'2026-09-05','absent','Automatically marked Absent after 11:00 AM.','2026-09-05 05:38:26.812987','2026-09-05 05:38:26.812987',4,NULL,NULL),(19,'2026-09-05','absent','Automatically marked Absent after 11:00 AM.','2026-09-05 05:38:26.827785','2026-09-05 05:38:26.827785',5,NULL,NULL),(20,'2026-09-05','absent','Automatically marked Absent after 11:00 AM.','2026-09-05 05:38:26.834280','2026-09-05 05:38:26.834280',6,NULL,NULL),(21,'2026-09-05','absent','Automatically marked Absent after 11:00 AM.','2026-09-05 05:38:26.849870','2026-09-05 05:38:26.849870',7,NULL,NULL),(22,'2026-09-05','absent','Automatically marked Absent after 11:00 AM.','2026-09-05 05:38:26.860294','2026-09-05 05:38:26.860294',8,NULL,NULL);
/*!40000 ALTER TABLE `core_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_chatmessage`
--

DROP TABLE IF EXISTS `core_chatmessage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_chatmessage` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `receiver_id` bigint NOT NULL,
  `sender_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_chatmessage_receiver_id_1d89b788_fk_accounts_app_user_id` (`receiver_id`),
  KEY `core_chatmessage_sender_id_c9992722_fk_accounts_app_user_id` (`sender_id`),
  CONSTRAINT `core_chatmessage_receiver_id_1d89b788_fk_accounts_app_user_id` FOREIGN KEY (`receiver_id`) REFERENCES `accounts_app_user` (`id`),
  CONSTRAINT `core_chatmessage_sender_id_c9992722_fk_accounts_app_user_id` FOREIGN KEY (`sender_id`) REFERENCES `accounts_app_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_chatmessage`
--

LOCK TABLES `core_chatmessage` WRITE;
/*!40000 ALTER TABLE `core_chatmessage` DISABLE KEYS */;
INSERT INTO `core_chatmessage` VALUES (1,'Hello sir','2026-09-04 07:41:16.714366',1,3,4),(2,'hii','2026-09-04 07:42:01.762858',1,4,3),(3,'hi did you complte this task','2026-09-04 07:44:42.774520',1,4,3),(4,'Hello','2026-09-05 05:36:39.214544',1,6,3),(5,'Good Morning Sir','2026-09-05 05:38:44.717101',1,3,6),(6,'hii','2026-09-05 12:34:17.314300',1,4,3),(7,'hlo','2026-09-05 12:34:55.722911',1,3,4);
/*!40000 ALTER TABLE `core_chatmessage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_client`
--

DROP TABLE IF EXISTS `core_client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_client` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `client_type` varchar(20) NOT NULL,
  `country` varchar(100) NOT NULL,
  `company_name` varchar(200) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `address` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `notes` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_client`
--

LOCK TABLES `core_client` WRITE;
/*!40000 ALTER TABLE `core_client` DISABLE KEYS */;
INSERT INTO `core_client` VALUES (1,'Frando','foreigner','Foreign','Hotelwaze','frando@gmail.com','9808457839','USA','active','Testing','2026-08-24 08:21:22.261555','2026-08-25 05:52:45.967162'),(6,'palak','indian','India','','palak.webcodeft@gmail.com','9808457839','','active','','2026-08-25 05:58:18.718694','2026-08-25 05:58:59.711949'),(7,'Padham Prabhu','indian','India','','test@gmail.com','9876543212','','active','','2026-08-29 07:38:54.358394','2026-08-29 07:38:54.358394');
/*!40000 ALTER TABLE `core_client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_holiday`
--

DROP TABLE IF EXISTS `core_holiday`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_holiday` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `name` varchar(150) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_holiday`
--

LOCK TABLES `core_holiday` WRITE;
/*!40000 ALTER TABLE `core_holiday` DISABLE KEYS */;
INSERT INTO `core_holiday` VALUES (1,'2026-08-15','independance day','','2026-09-03 06:19:51.779264'),(2,'2026-09-02','abc','','2026-09-03 06:21:04.987690'),(3,'2026-09-04','janamsshtami','','2026-09-03 06:24:50.888935');
/*!40000 ALTER TABLE `core_holiday` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_invoice`
--

DROP TABLE IF EXISTS `core_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_invoice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `invoice_number` varchar(50) NOT NULL,
  `invoice_date` date NOT NULL,
  `due_date` date DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `currency` varchar(10) NOT NULL,
  `tax_type` varchar(10) NOT NULL,
  `client_gstin` varchar(20) NOT NULL,
  `reference_number` varchar(100) NOT NULL,
  `payment_terms` varchar(255) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `discount` decimal(12,2) NOT NULL,
  `tax_amount` decimal(12,2) NOT NULL,
  `cgst_amount` decimal(12,2) NOT NULL,
  `sgst_amount` decimal(12,2) NOT NULL,
  `igst_amount` decimal(12,2) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `amount_paid` decimal(12,2) NOT NULL,
  `balance_due` decimal(12,2) NOT NULL,
  `notes` longtext NOT NULL,
  `terms` longtext NOT NULL,
  `payment_method` varchar(100) NOT NULL,
  `payment_reference` varchar(150) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `client_id` bigint NOT NULL,
  `project_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_number` (`invoice_number`),
  KEY `core_invoic_invoice_aef6bc_idx` (`invoice_number`),
  KEY `core_invoic_client__f81038_idx` (`client_id`),
  KEY `core_invoic_project_720086_idx` (`project_id`),
  KEY `core_invoic_status_3d8780_idx` (`status`),
  KEY `core_invoic_invoice_2f1348_idx` (`invoice_date`),
  KEY `core_invoic_due_dat_a17de6_idx` (`due_date`),
  CONSTRAINT `core_invoice_client_id_5b95bdaf_fk_core_client_id` FOREIGN KEY (`client_id`) REFERENCES `core_client` (`id`),
  CONSTRAINT `core_invoice_project_id_2f8fbf0f_fk_core_project_id` FOREIGN KEY (`project_id`) REFERENCES `core_project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_invoice`
--

LOCK TABLES `core_invoice` WRITE;
/*!40000 ALTER TABLE `core_invoice` DISABLE KEYS */;
INSERT INTO `core_invoice` VALUES (1,'INV-0001','2026-09-05',NULL,'draft','INR','gst','','','Payment due within 30 days.',10000.00,0.00,0.00,0.00,0.00,0.00,10000.00,0.00,10000.00,'','','','','2026-09-05 08:07:04.448988','2026-09-05 08:07:04.462391',6,7),(2,'INV-0002','2026-09-05',NULL,'draft','INR','gst','','','Payment due within 30 days.',1000.00,0.00,0.00,0.00,0.00,0.00,1000.00,0.00,1000.00,'','','','','2026-09-05 08:08:41.880587','2026-09-05 08:08:41.890778',6,7),(3,'INV-0003','2026-09-05',NULL,'draft','INR','gst','','','Payment due within 30 days.',1000.00,0.00,180.00,90.00,90.00,0.00,1180.00,0.00,1180.00,'','','','','2026-09-05 10:25:58.722953','2026-09-05 10:25:58.733539',7,6),(4,'INV-0004','2026-09-05','2026-09-17','draft','INR','gst','fds','','Payment due within 30 days.',10000.00,0.00,0.00,0.00,0.00,0.00,10000.00,0.00,10000.00,'','','','','2026-09-05 10:51:55.991843','2026-09-05 10:51:56.002507',6,5),(5,'INV-0005','2026-09-05',NULL,'draft','INR','gst','','','Payment due within 30 days.',123.00,0.00,22.14,11.07,11.07,0.00,145.14,0.00,145.14,'Thank You for doing Business With Us. Our Support Team will be with you by 24 x 7 x 365 Days.','Invoice Terms :\r\n(1) Services once sold will not be taken back.\r\n(2) Interest @10% p.m. will be charged if payment delayed after due date.\r\n(3) This is a computer generated invoice and doesn’t require signature.','','','2026-09-05 10:54:40.618549','2026-09-05 10:54:40.627264',7,6),(6,'INV-0006','2026-09-05','2026-09-14','draft','INR','gst','8765','','Payment due within 30 days.',1000.00,0.00,180.00,90.00,90.00,0.00,1180.00,0.00,1180.00,'Thank You for doing Business With Us. Our Support Team will be with you by 24 x 7 x 365 Days.','Invoice Terms :\r\n(1) Services once sold will not be taken back.\r\n(2) Interest @10% p.m. will be charged if payment delayed after due date.\r\n(3) This is a computer generated invoice and doesn’t require signature.','','','2026-09-05 10:57:39.076772','2026-09-05 10:57:39.085827',6,5),(8,'INV-0007','2026-09-05','2026-09-24','draft','INR','gst','8765','','Payment due within 30 days.',76543.00,0.00,13777.74,6888.87,6888.87,0.00,90320.74,0.00,90320.74,'Thank You for doing Business With Us. Our Support Team will be with you by 24 x 7 x 365 Days.','Invoice Terms :\r\n(1) Services once sold will not be taken back.\r\n(2) Interest @10% p.m. will be charged if payment delayed after due date.\r\n(3) This is a computer generated invoice and doesn’t require signature.','','','2026-09-05 11:50:39.483082','2026-09-05 11:50:39.493148',6,7),(9,'INV-0009','2026-09-05',NULL,'draft','INR','gst','','','Payment due within 30 days.',13.00,0.00,2.34,1.17,1.17,0.00,15.34,0.00,15.34,'Thank You for doing Business With Us. Our Support Team will be with you by 24 x 7 x 365 Days.','Invoice Terms :\r\n(1) Services once sold will not be taken back.\r\n(2) Interest @10% p.m. will be charged if payment delayed after due date.\r\n(3) This is a computer generated invoice and doesn’t require signature.','','','2026-09-05 11:51:35.030298','2026-09-05 11:51:35.041756',7,6),(10,'INV-0010','2026-09-05',NULL,'draft','INR','gst','','','Payment due within 30 days.',12.00,0.00,2.16,1.08,1.08,0.00,14.16,0.00,14.16,'Thank You for doing Business With Us. Our Support Team will be with you by 24 x 7 x 365 Days.','Invoice Terms :\r\n(1) Services once sold will not be taken back.\r\n(2) Interest @10% p.m. will be charged if payment delayed after due date.\r\n(3) This is a computer generated invoice and doesn’t require signature.','','','2026-09-05 11:52:24.503471','2026-09-05 11:52:24.513343',7,6),(11,'INV-0011','2026-09-05',NULL,'draft','INR','gst','','','Payment due within 30 days.',653.97,0.00,117.71,58.86,58.86,0.00,771.68,0.00,771.68,'Thank You for doing Business With Us. Our Support Team will be with you by 24 x 7 x 365 Days.','Invoice Terms :\r\n(1) Services once sold will not be taken back.\r\n(2) Interest @10% p.m. will be charged if payment delayed after due date.\r\n(3) This is a computer generated invoice and doesn’t require signature.','','','2026-09-05 11:55:41.531217','2026-09-05 11:55:41.541353',7,6),(12,'INV-0012','2026-09-05','2026-09-09','draft','INR','gst','8765','','Payment due within 30 days.',123.00,0.00,0.00,0.00,0.00,0.00,123.00,0.00,123.00,'Thank You for doing Business With Us. Our Support Team will be with you by 24 x 7 x 365 Days.','Invoice Terms :\r\n(1) Services once sold will not be taken back.\r\n(2) Interest @10% p.m. will be charged if payment delayed after due date.\r\n(3) This is a computer generated invoice and doesn’t require signature.','','','2026-09-05 12:33:32.868611','2026-09-05 12:33:32.884265',6,5);
/*!40000 ALTER TABLE `core_invoice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_invoiceitem`
--

DROP TABLE IF EXISTS `core_invoiceitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_invoiceitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` varchar(500) NOT NULL,
  `hsn_sac` varchar(50) NOT NULL,
  `quantity` decimal(10,2) NOT NULL,
  `unit` varchar(50) NOT NULL,
  `unit_price` decimal(12,2) NOT NULL,
  `discount_percent` decimal(5,2) NOT NULL,
  `tax_percent` decimal(5,2) NOT NULL,
  `line_subtotal` decimal(12,2) NOT NULL,
  `discount_amount` decimal(12,2) NOT NULL,
  `taxable_amount` decimal(12,2) NOT NULL,
  `tax_amount` decimal(12,2) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `order` int unsigned NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `invoice_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_invoic_invoice_2fc0f6_idx` (`invoice_id`),
  CONSTRAINT `core_invoiceitem_invoice_id_ed095f3b_fk_core_invoice_id` FOREIGN KEY (`invoice_id`) REFERENCES `core_invoice` (`id`),
  CONSTRAINT `core_invoiceitem_chk_1` CHECK ((`order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_invoiceitem`
--

LOCK TABLES `core_invoiceitem` WRITE;
/*!40000 ALTER TABLE `core_invoiceitem` DISABLE KEYS */;
INSERT INTO `core_invoiceitem` VALUES (1,'abcdefghi','',1.00,'1',10000.00,0.00,0.00,10000.00,0.00,10000.00,0.00,10000.00,0,'2026-09-05 08:07:04.453279','2026-09-05 08:07:04.453279',1),(2,'abcdefghi','',1.00,'1',1000.00,0.00,0.00,1000.00,0.00,1000.00,0.00,1000.00,0,'2026-09-05 08:08:41.882601','2026-09-05 08:08:41.882601',2),(3,'jnhbvgfd','',1.00,'Unit',1000.00,0.00,18.00,1000.00,0.00,1000.00,180.00,1180.00,0,'2026-09-05 10:25:58.724044','2026-09-05 10:25:58.724044',3),(4,'poitrewqq','',1.00,'Unit',10000.00,0.00,0.00,10000.00,0.00,10000.00,0.00,10000.00,0,'2026-09-05 10:51:55.993938','2026-09-05 10:51:55.993938',4),(5,'xz','',1.00,'Unit',123.00,0.00,18.00,123.00,0.00,123.00,22.14,145.14,0,'2026-09-05 10:54:40.619553','2026-09-05 10:54:40.619553',5),(6,'kjhgfds','',1.00,'Unit',1000.00,0.00,18.00,1000.00,0.00,1000.00,180.00,1180.00,0,'2026-09-05 10:57:39.079257','2026-09-05 10:57:39.079257',6),(8,'sxz','',1.00,'Unit',76543.00,0.00,18.00,76543.00,0.00,76543.00,13777.74,90320.74,0,'2026-09-05 11:50:39.484336','2026-09-05 11:50:39.484336',8),(9,'xs','',1.00,'Unit',13.00,0.00,18.00,13.00,0.00,13.00,2.34,15.34,0,'2026-09-05 11:51:35.032310','2026-09-05 11:51:35.032310',9),(10,'xs','',1.00,'Unit',12.00,0.00,18.00,12.00,0.00,12.00,2.16,14.16,0,'2026-09-05 11:52:24.505746','2026-09-05 11:52:24.505746',10),(11,'jn','',1.00,'Unit',653.97,0.00,18.00,653.97,0.00,653.97,117.71,771.68,0,'2026-09-05 11:55:41.533225','2026-09-05 11:55:41.533225',11),(12,'jhgfd','',1.00,'Unit',123.00,0.00,0.00,123.00,0.00,123.00,0.00,123.00,0,'2026-09-05 12:33:32.871617','2026-09-05 12:33:32.871617',12);
/*!40000 ALTER TABLE `core_invoiceitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_leave`
--

DROP TABLE IF EXISTS `core_leave`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_leave` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `leave_date` date NOT NULL,
  `reason` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `admin_remarks` longtext NOT NULL,
  `applied_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `employee_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_leave_employe_0ba228_idx` (`employee_id`,`leave_date`),
  KEY `core_leave_leave_d_429fa2_idx` (`leave_date`),
  KEY `core_leave_employe_8ef93e_idx` (`employee_id`,`status`),
  CONSTRAINT `core_leave_employee_id_70e37b16_fk_accounts_app_user_id` FOREIGN KEY (`employee_id`) REFERENCES `accounts_app_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_leave`
--

LOCK TABLES `core_leave` WRITE;
/*!40000 ALTER TABLE `core_leave` DISABLE KEYS */;
INSERT INTO `core_leave` VALUES (1,'2026-08-31','','pending','','2026-08-30 16:37:27.504367','2026-08-30 16:37:27.504367',7),(2,'2026-09-01','Leave applied by employee.','approved','','2026-08-30 17:50:02.799259','2026-08-30 17:50:02.799259',7);
/*!40000 ALTER TABLE `core_leave` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_project`
--

DROP TABLE IF EXISTS `core_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_project` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `project_name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `start_date` date DEFAULT NULL,
  `actual_end_date` date DEFAULT NULL,
  `status` varchar(30) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `client_id` bigint NOT NULL,
  `designer_id` bigint DEFAULT NULL,
  `designer_cost` decimal(12,2) NOT NULL,
  `developer_id` bigint DEFAULT NULL,
  `estimated_days` int unsigned DEFAULT NULL,
  `expected_end_date` date DEFAULT NULL,
  `notes` longtext NOT NULL,
  `priority` varchar(20) NOT NULL,
  `progress` int unsigned NOT NULL,
  `project_code` varchar(50) DEFAULT NULL,
  `project_type` varchar(50) NOT NULL,
  `requirements` longtext NOT NULL,
  `technology_stack` longtext NOT NULL,
  `tester_id` bigint DEFAULT NULL,
  `tester_cost` decimal(12,2) NOT NULL,
  `total_cost` decimal(12,2) NOT NULL,
  `development_cost` decimal(12,2) NOT NULL,
  `project_manager_id` bigint DEFAULT NULL,
  `paid_development_cost` decimal(12,2) NOT NULL,
  `development_payment_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_code` (`project_code`),
  KEY `core_project_client_id_4ba9e455_fk_core_client_id` (`client_id`),
  KEY `core_project_designer_id_b59394d9_fk_accounts_app_user_id` (`designer_id`),
  KEY `core_project_developer_id_f423b742_fk_accounts_app_user_id` (`developer_id`),
  KEY `core_project_tester_id_c881d0d3_fk_accounts_app_user_id` (`tester_id`),
  KEY `core_project_project_manager_id_c0fc2d72_fk_accounts_app_user_id` (`project_manager_id`),
  CONSTRAINT `core_project_client_id_4ba9e455_fk_core_client_id` FOREIGN KEY (`client_id`) REFERENCES `core_client` (`id`),
  CONSTRAINT `core_project_designer_id_b59394d9_fk_accounts_app_user_id` FOREIGN KEY (`designer_id`) REFERENCES `accounts_app_user` (`id`),
  CONSTRAINT `core_project_developer_id_f423b742_fk_accounts_app_user_id` FOREIGN KEY (`developer_id`) REFERENCES `accounts_app_user` (`id`),
  CONSTRAINT `core_project_project_manager_id_c0fc2d72_fk_accounts_app_user_id` FOREIGN KEY (`project_manager_id`) REFERENCES `accounts_app_user` (`id`),
  CONSTRAINT `core_project_tester_id_c881d0d3_fk_accounts_app_user_id` FOREIGN KEY (`tester_id`) REFERENCES `accounts_app_user` (`id`),
  CONSTRAINT `core_project_chk_1` CHECK ((`estimated_days` >= 0)),
  CONSTRAINT `core_project_chk_2` CHECK ((`progress` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_project`
--

LOCK TABLES `core_project` WRITE;
/*!40000 ALTER TABLE `core_project` DISABLE KEYS */;
INSERT INTO `core_project` VALUES (5,'Smart office system','testing','2026-08-01',NULL,'in_progress','2026-08-27 10:00:56.092078','2026-09-01 05:48:32.568814',6,4,10000.00,4,NULL,'2026-09-01','testings should be done today','medium',50,NULL,'web_application','testing','python',4,10000.00,50000.00,20000.00,NULL,10000.00,NULL),(6,'E-hundi Android and ios app for murgan temple','e-hundi mobile application for murgan temple mumbai, app needs to develop in flutter for both android and ios platforms. Gateway needs to add rozer pay. Admin can see all type of donations with advance search daily, weekly, monthly and custom dates. Admin can see the users edit and update their passwords as well. User can register using mobile number. Apps neends to follow the ux/ui from the previous apps.','2026-08-29',NULL,'planning','2026-08-29 07:46:00.670046','2026-09-02 07:23:42.362922',7,4,0.00,4,NULL,'2026-09-05','Need to finalize with dev to start asap.','high',0,NULL,'mobile_application','Flutter, Rozer pay, Android and ios, user mobile no. registration, advance search for admin','flutter',4,0.00,51000.00,10000.00,NULL,5000.00,NULL),(7,'abc','poiuytrewq','2026-08-29',NULL,'on_hold','2026-08-29 11:10:37.163575','2026-09-02 07:23:21.231180',6,7,2000.00,5,2,'2026-08-31','poiuytrewqasdfghjkl','high',30,NULL,'website','poiuytrewq','python',4,1000.00,10000.00,2000.00,NULL,1000.00,NULL);
/*!40000 ALTER TABLE `core_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_student`
--

DROP TABLE IF EXISTS `core_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_student` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `course` varchar(150) NOT NULL,
  `batch` varchar(100) NOT NULL,
  `joining_date` date DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `assigned_employee_id` bigint DEFAULT NULL,
  `fee_paid` decimal(10,2) NOT NULL,
  `learning_mode` varchar(20) NOT NULL,
  `notes` longtext NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `total_fee` decimal(10,2) NOT NULL,
  `aadhaar_card` varchar(100) DEFAULT NULL,
  `address` longtext NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `course_duration_months` int unsigned NOT NULL,
  `certificate_status` varchar(20) NOT NULL,
  `course_duration_days` int unsigned NOT NULL,
  `monthly_fee` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `core_student_assigned_employee_id_cb809667_fk_accounts_` (`assigned_employee_id`),
  CONSTRAINT `core_student_assigned_employee_id_cb809667_fk_accounts_` FOREIGN KEY (`assigned_employee_id`) REFERENCES `accounts_app_user` (`id`),
  CONSTRAINT `core_student_chk_1` CHECK ((`course_duration_months` >= 0)),
  CONSTRAINT `core_student_chk_2` CHECK ((`course_duration_days` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_student`
--

LOCK TABLES `core_student` WRITE;
/*!40000 ALTER TABLE `core_student` DISABLE KEYS */;
INSERT INTO `core_student` VALUES (2,'Aditi','sharma','aditi@gmail.com','9808457839','web development','morning','2026-09-01','active','2026-08-20 06:03:25.616992','2026-09-01 10:42:23.137868',4,5000.00,'offline','','paid',5000.00,'','','',0,'not_issued',45,0.00),(3,'aishvi','Sharma','aishvi@gmail.com','9865432345','web development','morning','2026-08-03','active','2026-08-20 06:04:33.328605','2026-09-01 10:54:50.637471',4,10000.00,'offline','','paid',10000.00,'','','',2,'issued',0,0.00),(4,'Aastha','','aastha@gmail.com','9808457839','Web Designing','morning','2026-05-01','active','2026-09-01 06:46:00.957966','2026-09-01 10:39:27.081591',7,25000.00,'offline','','partial',30000.00,'','','',6,'not_issued',0,10000.00),(5,'ridhi','','ridhi@gmail.com','9856274567','Web Designing','evening','2026-08-07','active','2026-09-01 07:26:55.581680','2026-09-01 10:35:46.820720',4,2000.00,'offline','','partial',5000.00,'','hamirpur','',3,'not_issued',0,1000.00);
/*!40000 ALTER TABLE `core_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_studentfeepayment`
--

DROP TABLE IF EXISTS `core_studentfeepayment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_studentfeepayment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_month` date NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_date` date DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_studen_student_a26c8d_idx` (`student_id`,`payment_month`),
  KEY `core_studen_student_5a848d_idx` (`student_id`,`status`),
  CONSTRAINT `core_studentfeepayment_student_id_3f600d26_fk_core_student_id` FOREIGN KEY (`student_id`) REFERENCES `core_student` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_studentfeepayment`
--

LOCK TABLES `core_studentfeepayment` WRITE;
/*!40000 ALTER TABLE `core_studentfeepayment` DISABLE KEYS */;
INSERT INTO `core_studentfeepayment` VALUES (1,'2026-08-01',1000.00,'2026-08-17','paid','2026-09-01 07:26:55.593032',5),(2,'2026-09-01',1000.00,'2026-09-01','paid','2026-09-01 10:35:46.815841',5),(3,'2026-05-01',5000.00,'2026-05-04','paid','2026-09-01 10:39:27.054764',4),(4,'2026-06-01',5000.00,'2026-06-01','paid','2026-09-01 10:39:27.060838',4),(5,'2026-07-01',5000.00,'2026-07-01','paid','2026-09-01 10:39:27.068208',4),(6,'2026-08-01',5000.00,'2026-08-03','paid','2026-09-01 10:39:27.072625',4),(7,'2026-09-01',5000.00,'2026-09-01','paid','2026-09-01 10:39:27.075921',4),(8,'2026-08-01',5000.00,'2026-08-04','paid','2026-09-01 10:40:42.329674',3),(9,'2026-09-01',5000.00,'2026-09-01','paid','2026-09-01 10:40:42.336233',3),(10,'2026-09-01',5000.00,'2026-09-01','paid','2026-09-01 10:42:23.129867',2);
/*!40000 ALTER TABLE `core_studentfeepayment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_task`
--

DROP TABLE IF EXISTS `core_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `task_date` date NOT NULL,
  `due_time` time(6) DEFAULT NULL,
  `priority` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `assigned_to_id` bigint NOT NULL,
  `project_id` bigint DEFAULT NULL,
  `employee_comment` longtext NOT NULL,
  `remaining_days` int unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_task_project_id_877ce78a_fk_core_project_id` (`project_id`),
  KEY `core_task_assigne_5f3995_idx` (`assigned_to_id`),
  KEY `core_task_assigne_5bfa1c_idx` (`assigned_to_id`,`status`),
  KEY `core_task_task_da_656a32_idx` (`task_date`),
  CONSTRAINT `core_task_assigned_to_id_4a4e0391_fk_accounts_app_user_id` FOREIGN KEY (`assigned_to_id`) REFERENCES `accounts_app_user` (`id`),
  CONSTRAINT `core_task_project_id_877ce78a_fk_core_project_id` FOREIGN KEY (`project_id`) REFERENCES `core_project` (`id`),
  CONSTRAINT `core_task_chk_1` CHECK ((`remaining_days` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_task`
--

LOCK TABLES `core_task` WRITE;
/*!40000 ALTER TABLE `core_task` DISABLE KEYS */;
INSERT INTO `core_task` VALUES (2,'SCO','testing des.','2026-08-27','18:00:00.000000','low','pending','2026-08-27 11:09:51.026792','2026-08-29 08:34:19.271426',6,5,'',NULL),(4,'video editing','edit a video of student','2026-08-29','17:00:00.000000','medium','completed','2026-08-29 07:01:46.327442','2026-08-30 07:49:00.037231',7,5,'editting will be done by tomorrow',2),(5,'Need to test the app on android once the build is ready','testing jhk jugjgjgjyg','2026-08-29','17:20:00.000000','medium','completed','2026-08-29 07:51:09.698040','2026-08-31 02:38:58.653418',5,6,'Development should take 5 days more',5),(6,'banner for e-hundi','create a banner for e-hundi','2026-08-30',NULL,'urgent','completed','2026-08-30 07:55:42.032458','2026-09-01 11:35:04.875130',7,6,'i will create it tomorrow',2),(7,'Need to fix issues on the PMS','Check the issues discussed','2026-08-31',NULL,'high','completed','2026-08-31 02:44:54.722277','2026-08-31 06:52:35.737787',4,5,'',NULL),(8,'hotelwaze testing on android','testing should be done today','2026-09-02',NULL,'high','in_progress','2026-09-02 07:24:57.880956','2026-09-02 08:47:15.367655',4,7,'',NULL),(9,'banner foe hotelwaze','poiuytrewq','2026-09-02',NULL,'low','pending','2026-09-02 08:46:49.448018','2026-09-02 08:46:49.448018',5,5,'',NULL);
/*!40000 ALTER TABLE `core_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_taskcomment`
--

DROP TABLE IF EXISTS `core_taskcomment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_taskcomment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `task_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_taskco_task_id_7084f1_idx` (`task_id`),
  KEY `core_taskco_user_id_cc3c51_idx` (`user_id`),
  KEY `core_taskco_task_id_b10483_idx` (`task_id`,`created_at`),
  CONSTRAINT `core_taskcomment_task_id_c5deeb7d_fk_core_task_id` FOREIGN KEY (`task_id`) REFERENCES `core_task` (`id`),
  CONSTRAINT `core_taskcomment_user_id_254500e5_fk_accounts_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_app_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_taskcomment`
--

LOCK TABLES `core_taskcomment` WRITE;
/*!40000 ALTER TABLE `core_taskcomment` DISABLE KEYS */;
INSERT INTO `core_taskcomment` VALUES (1,'need to fix today','2026-08-31 06:22:14.413517','2026-08-31 06:22:14.413517',7,3),(2,'add banners','2026-08-31 06:36:12.132675','2026-08-31 06:36:12.132675',6,3),(3,'driver error is still present','2026-09-01 11:23:59.048390','2026-09-01 11:23:59.048390',5,3),(4,'error solved','2026-09-01 11:34:12.191537','2026-09-01 11:34:12.191537',5,3),(5,'hey','2026-09-02 09:26:09.470078','2026-09-02 09:26:09.470078',8,3);
/*!40000 ALTER TABLE `core_taskcomment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_todo`
--

DROP TABLE IF EXISTS `core_todo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_todo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext,
  `due_date` date DEFAULT NULL,
  `priority` varchar(10) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `is_completed` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_todo_user_id_9708b156_fk_accounts_app_user_id` (`user_id`),
  CONSTRAINT `core_todo_user_id_9708b156_fk_accounts_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_app_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_todo`
--

LOCK TABLES `core_todo` WRITE;
/*!40000 ALTER TABLE `core_todo` DISABLE KEYS */;
INSERT INTO `core_todo` VALUES (7,'send project proposal','poiuytrewqasdfghjkl,mnbvcx','2026-09-03','high','jhgfds',0,'2026-09-02 10:22:49.005548','2026-09-02 10:24:30.899875',3),(10,'call developer','',NULL,'medium','',0,'2026-09-02 10:34:15.385691','2026-09-02 10:34:15.385691',3),(11,'Draft emails','','2026-09-03','medium','',1,'2026-09-02 10:35:18.643141','2026-09-02 10:37:38.087371',3),(12,'finish assignments','','2026-09-03','low','',0,'2026-09-02 10:35:28.123778','2026-09-02 10:37:17.802509',3),(13,'review hotelwaze documents','','2026-09-02','medium','',1,'2026-09-02 10:35:42.570467','2026-09-02 10:37:35.434136',3),(14,'check pending requests','','2026-09-02','high','',1,'2026-09-02 10:36:49.255743','2026-09-02 10:39:51.013103',3),(15,'schedule an appointment','','2026-09-01','medium','',0,'2026-09-02 10:38:27.134579','2026-09-02 10:38:34.387957',3),(16,'Test','',NULL,'medium','',0,'2026-09-02 10:43:08.421118','2026-09-02 10:43:08.421118',3);
/*!40000 ALTER TABLE `core_todo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_userstatus`
--

DROP TABLE IF EXISTS `core_userstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_userstatus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` bigint NOT NULL,
  `is_online` tinyint(1) NOT NULL,
  `last_seen` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `core_userstatus_user_id_3d502ce2_fk_accounts_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_app_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_userstatus`
--

LOCK TABLES `core_userstatus` WRITE;
/*!40000 ALTER TABLE `core_userstatus` DISABLE KEYS */;
INSERT INTO `core_userstatus` VALUES (1,3,1,'2026-09-05 12:35:06.200283'),(2,4,1,'2026-09-05 12:34:41.776221'),(3,6,1,'2026-09-05 08:01:34.220009');
/*!40000 ALTER TABLE `core_userstatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_app_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_app_user_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_app_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (6,'accounts_app','user'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(9,'core','attendance'),(17,'core','chatmessage'),(11,'core','client'),(16,'core','holiday'),(19,'core','invoice'),(20,'core','invoiceitem'),(12,'core','leave'),(10,'core','project'),(7,'core','student'),(14,'core','studentfeepayment'),(8,'core','task'),(13,'core','taskcomment'),(15,'core','todo'),(18,'core','userstatus'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-08-14 05:28:05.088517'),(2,'contenttypes','0002_remove_content_type_name','2026-08-14 05:28:05.189741'),(3,'auth','0001_initial','2026-08-14 05:28:05.488738'),(4,'auth','0002_alter_permission_name_max_length','2026-08-14 05:28:05.556965'),(5,'auth','0003_alter_user_email_max_length','2026-08-14 05:28:05.568152'),(6,'auth','0004_alter_user_username_opts','2026-08-14 05:28:05.578862'),(7,'auth','0005_alter_user_last_login_null','2026-08-14 05:28:05.591809'),(8,'auth','0006_require_contenttypes_0002','2026-08-14 05:28:05.595764'),(9,'auth','0007_alter_validators_add_error_messages','2026-08-14 05:28:05.604712'),(10,'auth','0008_alter_user_username_max_length','2026-08-14 05:28:05.614972'),(11,'auth','0009_alter_user_last_name_max_length','2026-08-14 05:28:05.625981'),(12,'auth','0010_alter_group_name_max_length','2026-08-14 05:28:05.647538'),(13,'auth','0011_update_proxy_permissions','2026-08-14 05:28:05.660159'),(14,'auth','0012_alter_user_first_name_max_length','2026-08-14 05:28:05.668952'),(15,'accounts_app','0001_initial','2026-08-14 05:28:06.007619'),(16,'admin','0001_initial','2026-08-14 05:28:06.165593'),(17,'admin','0002_logentry_remove_auto_add','2026-08-14 05:28:06.179428'),(18,'admin','0003_logentry_add_action_flag_choices','2026-08-14 05:28:06.194823'),(19,'sessions','0001_initial','2026-08-14 05:28:06.241382'),(20,'accounts_app','0002_alter_user_username','2026-08-14 05:30:15.086150'),(21,'accounts_app','0003_user_joining_date_alter_user_department_and_more','2026-08-17 04:40:57.549135'),(22,'core','0001_initial','2026-08-17 05:57:01.325705'),(23,'core','0002_task','2026-08-19 06:02:11.895068'),(24,'core','0003_alter_task_description_attendance','2026-08-19 07:06:54.368057'),(25,'core','0004_student_assigned_employee_student_fee_paid_and_more','2026-08-20 05:25:35.076328'),(26,'core','0005_student_aadhaar_card_student_address_student_photo','2026-08-20 07:18:11.363572'),(27,'core','0006_client_project','2026-08-20 11:27:17.359326'),(28,'core','0007_project_currency_project_project_cost_and_more','2026-08-24 08:37:28.725024'),(29,'core','0008_alter_client_client_type','2026-08-24 09:28:12.131598'),(30,'core','0009_alter_client_options_alter_project_options_and_more','2026-08-25 06:06:53.215526'),(31,'core','0010_rename_end_date_project_actual_end_date_and_more','2026-08-25 11:33:22.468693'),(32,'core','0011_task_project','2026-08-27 10:30:03.405551'),(33,'core','0012_project_development_cost_project_project_manager','2026-08-29 09:04:25.885018'),(34,'core','0013_remove_project_developer_cost','2026-08-29 16:20:14.665174'),(35,'core','0014_alter_task_options_alter_task_assigned_to_and_more','2026-08-29 16:56:46.952679'),(36,'core','0015_task_employee_comment_task_remaining_days','2026-08-30 06:56:17.159550'),(37,'core','0016_attendance_check_in_attendance_check_out_and_more','2026-08-30 14:03:37.677888'),(38,'core','0017_alter_attendance_options_leave','2026-08-30 16:01:18.259574'),(39,'core','0018_taskcomment','2026-08-31 06:04:38.962170'),(40,'core','0019_project_paid_development_cost','2026-09-01 05:24:24.759711'),(41,'core','0020_project_development_payment_date','2026-09-01 05:33:19.454503'),(42,'core','0021_student_course_duration_months_studentfeepayment','2026-09-01 07:14:22.403039'),(43,'core','0022_alter_studentfeepayment_options_and_more','2026-09-01 08:03:02.738498'),(44,'core','0023_todo','2026-09-02 10:02:33.212872'),(45,'core','0024_holiday','2026-09-03 06:00:12.694087'),(46,'core','0025_chatmessage_userstatus','2026-09-03 11:26:18.945225'),(47,'core','0026_userstatus_is_online_userstatus_last_seen','2026-09-03 12:18:55.969301'),(48,'core','0027_remove_chatmessage_is_online_and_more','2026-09-04 07:30:25.156092'),(49,'core','0028_invoice_invoiceitem_and_more','2026-09-05 05:48:18.710720');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('rb9xip280hhdvi45qtnov6ea6sbee3kb','.eJxVjMEOwiAQRP-FsyGUdqF49O43kIVdpGogKe3J-O9K0oPeJvPezEt43Lfs98arX0icxShOv13A-ODSAd2x3KqMtWzrEmRX5EGbvFbi5-Vw_w4yttzXmlA5hsElFR2AihMwJ03amFHNHBFn-01oQZmQaIREGKwOifUQ7CTeH-8VOFo:1wvpmM:iEaCmA5xpsYnqf3MscMoSwBQXixcJE6SQOmfoI5OWPk','2026-08-31 05:20:58.318882'),('z0t5ufwla7f17rx05edfswh79sei0xii','.eJxVjMEOwiAQBf-FsyFAKbAevfcbyLKAVA0kpT0Z_9026UGvb2bem3nc1uK3nhY_R3Zlhl1-t4D0TPUA8YH13ji1ui5z4IfCT9r51GJ63U7376BgL3uNwo1IwgUNLqiQIUatQCogS2A0ZplyGnUCuRMycQjKSIk0WCGspYF9vvLzOAo:1x2j6H:g3d5xkoEl1QQ4aimZDfViAZOjkokWRAbjbFaa-NohLg','2026-09-19 05:38:01.184539');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'office_management'
--

--
-- Dumping routines for database 'office_management'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-06 13:08:04

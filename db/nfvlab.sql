-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: db_nfv
-- ------------------------------------------------------
-- Server version	5.7.17-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `t_flow`
--

DROP TABLE IF EXISTS `t_flow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_flow` (
  `flow_id` int(10) unsigned NOT NULL,
  `chain` varchar(255) NOT NULL,
  `match_field` varchar(100) NOT NULL,
  PRIMARY KEY (`flow_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_flow`
--

LOCK TABLES `t_flow` WRITE;
/*!40000 ALTER TABLE `t_flow` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_flow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_function`
--

DROP TABLE IF EXISTS `t_function`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_function` (
  `fe_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `image_id` int(10) unsigned NOT NULL,
  `host_id` int(10) unsigned NOT NULL,
  `func_local_id` char(40) NOT NULL,
  `ip` char(16) NOT NULL,
  `pwd` varchar(100) NOT NULL,
  `cpu` tinyint(3) unsigned NOT NULL,
  `ram` smallint(5) unsigned NOT NULL,
  `type` tinyint(3) unsigned NOT NULL,
  `size` smallint(5) unsigned NOT NULL,
  `ref_count` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`fe_id`),
  KEY `image_id` (`image_id`),
  KEY `host_id` (`host_id`),
  KEY `ref_count` (`ref_count`),
  CONSTRAINT `host_id` FOREIGN KEY (`host_id`) REFERENCES `t_host` (`host_id`),
  CONSTRAINT `image_id` FOREIGN KEY (`image_id`) REFERENCES `t_image` (`image_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_function`
--

LOCK TABLES `t_function` WRITE;
/*!40000 ALTER TABLE `t_function` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_function` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_host`
--

DROP TABLE IF EXISTS `t_host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_host` (
  `host_id` int(10) unsigned NOT NULL,
  `ip` char(16) NOT NULL,
  `pwd` varchar(100) NOT NULL,
  `cpu` tinyint(3) unsigned NOT NULL,
  `ram` smallint(5) unsigned NOT NULL,
  `disk` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`host_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_host`
--

LOCK TABLES `t_host` WRITE;
/*!40000 ALTER TABLE `t_host` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_image`
--

DROP TABLE IF EXISTS `t_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_image` (
  `image_id` int(10) unsigned NOT NULL,
  `func` varchar(255) DEFAULT NULL,
  `type` tinyint(4) NOT NULL,
  PRIMARY KEY (`image_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_image`
--

LOCK TABLES `t_image` WRITE;
/*!40000 ALTER TABLE `t_image` DISABLE KEYS */;
/*!40000 ALTER TABLE `t_image` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-12-17 20:42:31

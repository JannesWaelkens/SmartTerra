CREATE DATABASE  IF NOT EXISTS `SmartTerradb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `SmartTerradb`;
-- MySQL dump 10.13  Distrib 8.0.15, for Win64 (x86_64)
--
-- Host: localhost    Database: projectdbv2
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `acties`
--

DROP TABLE IF EXISTS `acties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `acties` (
  `idacties` int(11) NOT NULL AUTO_INCREMENT,
  `idhardware` varchar(20) DEFAULT NULL,
  `tijdstip` datetime DEFAULT NULL,
  PRIMARY KEY (`idacties`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acties`
--

LOCK TABLES `acties` WRITE;
/*!40000 ALTER TABLE `acties` DISABLE KEYS */;
/*!40000 ALTER TABLE `acties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hardware`
--

DROP TABLE IF EXISTS `hardware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `hardware` (
  `idhardware` varchar(20) NOT NULL,
  `beschrijving` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idhardware`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hardware`
--

LOCK TABLES `hardware` WRITE;
/*!40000 ALTER TABLE `hardware` DISABLE KEYS */;
INSERT INTO `hardware` VALUES ('D1','deur'),('L1','heatlamp'),('L2','uvlamp'),('S1','warmtesensor1'),('S2','warmtesensor2'),('S3','warmtesensor3'),('S4','uvsensor'),('V1','Groente'),('V2','Korrel'),('V3','Krekel'),('V4','Sprinkhaan'),('V5','Meelworm'),('VL','voederluik');
/*!40000 ALTER TABLE `hardware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_histogram`
--

DROP TABLE IF EXISTS `sensor_histogram`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `sensor_histogram` (
  `idsensor_histogram` int(11) NOT NULL AUTO_INCREMENT,
  `idhardware` varchar(20) DEFAULT NULL,
  `tijdstip` datetime DEFAULT NULL,
  `waarde` int(11) DEFAULT NULL,
  PRIMARY KEY (`idsensor_histogram`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_histogram`
--

LOCK TABLES `sensor_histogram` WRITE;
/*!40000 ALTER TABLE `sensor_histogram` DISABLE KEYS */;
/*!40000 ALTER TABLE `sensor_histogram` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `voedselschema`
--

DROP TABLE IF EXISTS `voedselschema`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `voedselschema` (
  `idvoedselschema` int(11) NOT NULL AUTO_INCREMENT,
  `idhardware` varchar(20) DEFAULT NULL,
  `dag` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idvoedselschema`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voedselschema`
--

LOCK TABLES `voedselschema` WRITE;
/*!40000 ALTER TABLE `voedselschema` DISABLE KEYS */;
INSERT INTO `voedselschema` VALUES (1,'V2','maandag'),(2,'V1','dinsdag'),(3,'V4','woensdag'),(4,'V5','donderdag'),(5,'V4','vrijdag'),(6,'V3','zaterdag'),(7,'V1','zondag');
/*!40000 ALTER TABLE `voedselschema` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'projectdbv2'
--

--
-- Dumping routines for database 'projectdbv2'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-16 15:55:38

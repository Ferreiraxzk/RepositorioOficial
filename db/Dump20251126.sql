-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: projeto
-- ------------------------------------------------------
-- Server version	8.0.37

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
-- Table structure for table `agendamentos`
--

DROP TABLE IF EXISTS `agendamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agendamentos` (
  `IDagendamentos` int NOT NULL AUTO_INCREMENT,
  `IDusuario` int DEFAULT NULL,
  `IDchromebooks` int DEFAULT NULL,
  `professor` varchar(45) NOT NULL,
  `turma` varchar(10) NOT NULL,
  `data` date NOT NULL,
  `horario_inicio` time NOT NULL,
  `horario_fim` time NOT NULL,
  `quantidade` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`IDagendamentos`),
  UNIQUE KEY `idagendamentos_UNIQUE` (`IDagendamentos`),
  KEY `idusuario_idx` (`IDusuario`),
  KEY `IDchromebooks_idx` (`IDchromebooks`),
  CONSTRAINT `IDchromebooks` FOREIGN KEY (`IDchromebooks`) REFERENCES `kits_chromebooks` (`IDchromebooks`),
  CONSTRAINT `IDusuario` FOREIGN KEY (`IDusuario`) REFERENCES `usuario` (`IDusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agendamentos`
--

LOCK TABLES `agendamentos` WRITE;
/*!40000 ALTER TABLE `agendamentos` DISABLE KEYS */;
/*!40000 ALTER TABLE `agendamentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kits_chromebooks`
--

DROP TABLE IF EXISTS `kits_chromebooks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `kits_chromebooks` (
  `IDchromebooks` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(25) NOT NULL,
  `quantidade` int NOT NULL,
  PRIMARY KEY (`IDchromebooks`),
  UNIQUE KEY `idchromebooks_UNIQUE` (`IDchromebooks`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kits_chromebooks`
--

LOCK TABLES `kits_chromebooks` WRITE;
/*!40000 ALTER TABLE `kits_chromebooks` DISABLE KEYS */;
INSERT INTO `kits_chromebooks` VALUES (1,'lote',1),(2,'lote teste',30),(6,'Lote teste 2',35);
/*!40000 ALTER TABLE `kits_chromebooks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `IDusuario` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `senha` varchar(50) NOT NULL,
  `login` varchar(45) DEFAULT NULL,
  `perfil` varchar(20) NOT NULL DEFAULT 'professor',
  PRIMARY KEY (`IDusuario`),
  UNIQUE KEY `idusuario_UNIQUE` (`IDusuario`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `login_UNIQUE` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'teste','teste123@gmail.com','123456','adm','adm'),(2,'aaa','joao@gmail.com','11111111','adsss','professor'),(3,'jv','jv123@gmail.com','123789','JOAO','professor'),(4,'a','a@gmail.com','a','a','professor'),(6,'vini','vini123@gmail.com','12345','us','professor'),(8,'teste da silva','testesilva@gmail.com','1234','teste','professor'),(9,'vinicius rodrigues','vn.pjlll999@gmail.com','12345','Vinicius','professor'),(11,'434kkk','ferreiramourajoaovictor4@gmail.com','147114','lll','professor'),(13,'teste j','teste567@gmail.com','teste','Teste jm','professor'),(16,'aaaaaaaaaa','aaaa@gmail.com','123456','teste aa','professor'),(17,'joao victor','joaovictor@gmail.com','111','João Victor','professor'),(19,'Testeprofessor','professor@gmail.com','333','Professor','professor'),(22,'Professor1','professor1@gmail.com','123456','professor1','professor'),(23,'Coordenador1','coordenador1@gmail.com','123456','coordenador1','adm');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-26 21:21:34

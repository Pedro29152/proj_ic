-- MySQL dump 10.13  Distrib 8.0.12, for Win64 (x86_64)
--
-- Host: localhost    Database: proj_ic
-- ------------------------------------------------------
-- Server version	8.0.12

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
-- Table structure for table `autores`
--

DROP TABLE IF EXISTS `autores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `autores` (
  `codAutor` int(11) NOT NULL AUTO_INCREMENT,
  `raAutor` varchar(13) NOT NULL,
  `nomeAutor` varchar(200) NOT NULL,
  PRIMARY KEY (`codAutor`),
  UNIQUE KEY `raAutor_UNIQUE` (`raAutor`),
  UNIQUE KEY `codAutor_UNIQUE` (`codAutor`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autores`
--

LOCK TABLES `autores` WRITE;
/*!40000 ALTER TABLE `autores` DISABLE KEYS */;
INSERT INTO `autores` VALUES (48,'1231231123444','aut 1'),(49,'123123332313','aut 2');
/*!40000 ALTER TABLE `autores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cursos`
--

DROP TABLE IF EXISTS `cursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `cursos` (
  `codCurso` int(11) NOT NULL AUTO_INCREMENT,
  `descricaoCurso` varchar(50) NOT NULL,
  `ativo` int(11) NOT NULL,
  `abreviacao` varchar(5) NOT NULL,
  PRIMARY KEY (`codCurso`),
  UNIQUE KEY `abreviacao_UNIQUE` (`abreviacao`),
  UNIQUE KEY `descricaoCurso_UNIQUE` (`descricaoCurso`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cursos`
--

LOCK TABLES `cursos` WRITE;
/*!40000 ALTER TABLE `cursos` DISABLE KEYS */;
INSERT INTO `cursos` VALUES (1,'Jogos Digitais',1,'JD'),(2,'Analise e Desenvolvimento de Sistemas',1,'ADS');
/*!40000 ALTER TABLE `cursos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orientadores`
--

DROP TABLE IF EXISTS `orientadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `orientadores` (
  `codOrientador` int(11) NOT NULL AUTO_INCREMENT,
  `nomeOrientador` varchar(200) NOT NULL,
  `raOrientador` varchar(20) NOT NULL,
  PRIMARY KEY (`codOrientador`),
  UNIQUE KEY `raOrientador_UNIQUE` (`raOrientador`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orientadores`
--

LOCK TABLES `orientadores` WRITE;
/*!40000 ALTER TABLE `orientadores` DISABLE KEYS */;
INSERT INTO `orientadores` VALUES (1,'nome ori','1237816283'),(2,'nome ori 2','0000000122'),(3,'orientador B ay','12345678912345678900');
/*!40000 ALTER TABLE `orientadores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `palavras_chave`
--

DROP TABLE IF EXISTS `palavras_chave`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `palavras_chave` (
  `codPalavra` int(11) NOT NULL AUTO_INCREMENT,
  `palavraChave` varchar(50) NOT NULL,
  `codProjeto` int(11) NOT NULL,
  PRIMARY KEY (`codPalavra`),
  KEY `FK_PROJETO_idx` (`codProjeto`),
  CONSTRAINT `FK_PALAVRA_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codprojeto`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `palavras_chave`
--

LOCK TABLES `palavras_chave` WRITE;
/*!40000 ALTER TABLE `palavras_chave` DISABLE KEYS */;
INSERT INTO `palavras_chave` VALUES (14,'pal',64),(15,'pal kkkkkkkkk',65);
/*!40000 ALTER TABLE `palavras_chave` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projeto_autor`
--

DROP TABLE IF EXISTS `projeto_autor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `projeto_autor` (
  `codProjeto` int(11) NOT NULL,
  `codAutor` int(11) NOT NULL,
  PRIMARY KEY (`codProjeto`,`codAutor`),
  KEY `FK_AUTOR_idx` (`codAutor`),
  CONSTRAINT `FK_AUTOR` FOREIGN KEY (`codAutor`) REFERENCES `autores` (`codautor`) ON DELETE CASCADE,
  CONSTRAINT `FK_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codprojeto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projeto_autor`
--

LOCK TABLES `projeto_autor` WRITE;
/*!40000 ALTER TABLE `projeto_autor` DISABLE KEYS */;
INSERT INTO `projeto_autor` VALUES (64,48),(65,48),(64,49),(65,49);
/*!40000 ALTER TABLE `projeto_autor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projeto_orientador`
--

DROP TABLE IF EXISTS `projeto_orientador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `projeto_orientador` (
  `codOrientador` int(11) NOT NULL,
  `codProjeto` int(11) NOT NULL,
  PRIMARY KEY (`codOrientador`,`codProjeto`),
  KEY `FK_PROJETO_ORI_idx` (`codProjeto`),
  CONSTRAINT `FK_ORIENTADOR` FOREIGN KEY (`codOrientador`) REFERENCES `orientadores` (`codorientador`) ON DELETE CASCADE,
  CONSTRAINT `FK_PROJETO_ORI` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codprojeto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projeto_orientador`
--

LOCK TABLES `projeto_orientador` WRITE;
/*!40000 ALTER TABLE `projeto_orientador` DISABLE KEYS */;
INSERT INTO `projeto_orientador` VALUES (3,64),(3,65);
/*!40000 ALTER TABLE `projeto_orientador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projetos`
--

DROP TABLE IF EXISTS `projetos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `projetos` (
  `codProjeto` int(11) NOT NULL AUTO_INCREMENT,
  `tituloProjeto` varchar(100) NOT NULL,
  `descricao` longtext NOT NULL,
  `nomeArquivo` varchar(90) NOT NULL,
  `likes` int(11) NOT NULL DEFAULT '0',
  `deslikes` int(11) NOT NULL DEFAULT '0',
  `numVisitas` int(11) NOT NULL DEFAULT '0',
  `numDownloads` int(11) NOT NULL DEFAULT '0',
  `dataAvaliacao` date NOT NULL,
  `dataEnvio` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codCurso` int(11) NOT NULL,
  `ativo` int(11) NOT NULL,
  `subTitulo` longtext NOT NULL,
  PRIMARY KEY (`codProjeto`),
  UNIQUE KEY `nomeArquivo_UNIQUE` (`nomeArquivo`),
  UNIQUE KEY `codProjeto_UNIQUE` (`codProjeto`),
  KEY `FK_CURSO_idx` (`codCurso`),
  CONSTRAINT `FK_CURSO` FOREIGN KEY (`codCurso`) REFERENCES `cursos` (`codcurso`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projetos`
--

LOCK TABLES `projetos` WRITE;
/*!40000 ALTER TABLE `projetos` DISABLE KEYS */;
INSERT INTO `projetos` VALUES (64,'proj teste','oaisdn','JD-PROJ-TESTE-2019-11-20-A6C7FE.pdf',0,0,0,0,'2019-12-12','2019-11-20 22:56:09',1,1,'owansdn'),(65,'Projeto Bom Msm','aaaaaaaaaaaaaa','JD-PROJETO-BOM-MSM-2019-11-20-D82A35.pdf',0,0,0,0,'2019-12-12','2019-11-20 23:01:03',1,1,'sub ne');
/*!40000 ALTER TABLE `projetos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `usuarios` (
  `codUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `nomeUsuario` varchar(50) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `tipoUsuario` int(11) NOT NULL,
  `ativo` int(11) NOT NULL DEFAULT '1',
  `nome` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  PRIMARY KEY (`codUsuario`),
  UNIQUE KEY `nomeUsuario_UNIQUE` (`nomeUsuario`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','pbkdf2:sha256:50000$ugKk3qk8$a68e58926f85dff54dd23416597dff7465f9855ff94f877d9dbdc4243e1d80d9',3,1,'Silvia','oiasda@iaon.com');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-11-20 23:06:37

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
  `codProjeto` int(11) NOT NULL,
  PRIMARY KEY (`codAutor`),
  UNIQUE KEY `raAutor_UNIQUE` (`raAutor`),
  UNIQUE KEY `codAutor_UNIQUE` (`codAutor`),
  KEY `FK_PROJETO_idx` (`codProjeto`),
  CONSTRAINT `FK_AUTOR_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codprojeto`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autores`
--

LOCK TABLES `autores` WRITE;
/*!40000 ALTER TABLE `autores` DISABLE KEYS */;
INSERT INTO `autores` VALUES (21,'1111111111111','Autor1',42),(22,'2222222222222','Autor2',42),(23,'123123','qwe',43),(24,'0128301283','autor teste',44),(25,'7319273212','autor teste 2',45);
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
  `abreviacao` varchar(10) NOT NULL,
  PRIMARY KEY (`codCurso`),
  UNIQUE KEY `abreviacao_UNIQUE` (`abreviacao`),
  UNIQUE KEY `descricaoCurso_UNIQUE` (`descricaoCurso`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
-- Table structure for table `gerenciadores`
--

DROP TABLE IF EXISTS `gerenciadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `gerenciadores` (
  `codGerenciador` int(11) NOT NULL AUTO_INCREMENT,
  `cpfGerenciador` varchar(11) NOT NULL,
  `instituicao` varchar(100) NOT NULL,
  `nomeGerenciador` varchar(100) NOT NULL,
  `emailGerenciador` varchar(100) NOT NULL,
  PRIMARY KEY (`codGerenciador`),
  UNIQUE KEY `cpfGerenciador_UNIQUE` (`cpfGerenciador`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gerenciadores`
--

LOCK TABLES `gerenciadores` WRITE;
/*!40000 ALTER TABLE `gerenciadores` DISABLE KEYS */;
INSERT INTO `gerenciadores` VALUES (1,'12312312312','Fatec','Pedro','Pedro@mail.com'),(2,'12332112312','Fatec','Teste','teste@mail.com');
/*!40000 ALTER TABLE `gerenciadores` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orientadores`
--

LOCK TABLES `orientadores` WRITE;
/*!40000 ALTER TABLE `orientadores` DISABLE KEYS */;
INSERT INTO `orientadores` VALUES (1,'nome ori','1237816283'),(2,'nome ori 2','0000000122');
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
  CONSTRAINT `FK_PALAVRA_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codprojeto`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `palavras_chave`
--

LOCK TABLES `palavras_chave` WRITE;
/*!40000 ALTER TABLE `palavras_chave` DISABLE KEYS */;
INSERT INTO `palavras_chave` VALUES (5,'Palavra1',42),(6,'Palavra2',42),(7,'qweqwe',43),(8,'pal k',44),(9,'pal k 2',45);
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
  CONSTRAINT `FK_AUTOR` FOREIGN KEY (`codAutor`) REFERENCES `autores` (`codautor`),
  CONSTRAINT `FK_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codprojeto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projeto_autor`
--

LOCK TABLES `projeto_autor` WRITE;
/*!40000 ALTER TABLE `projeto_autor` DISABLE KEYS */;
INSERT INTO `projeto_autor` VALUES (42,21),(42,22),(43,23),(44,24),(45,25);
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
  CONSTRAINT `FK_ORIENTADOR` FOREIGN KEY (`codOrientador`) REFERENCES `orientadores` (`codorientador`),
  CONSTRAINT `FK_PROJETO_ORI` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codprojeto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projeto_orientador`
--

LOCK TABLES `projeto_orientador` WRITE;
/*!40000 ALTER TABLE `projeto_orientador` DISABLE KEYS */;
INSERT INTO `projeto_orientador` VALUES (1,44),(2,45);
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
  `notaProjeto` decimal(5,2) NOT NULL,
  `dataAvaliacao` date NOT NULL,
  `dataEnvio` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codGerenciador` int(11) NOT NULL,
  `codCurso` int(11) NOT NULL,
  `ativo` int(11) NOT NULL,
  `subTitulo` longtext NOT NULL,
  PRIMARY KEY (`codProjeto`),
  UNIQUE KEY `nomeArquivo_UNIQUE` (`nomeArquivo`),
  UNIQUE KEY `codProjeto_UNIQUE` (`codProjeto`),
  KEY `FK_GERENCIAOR_idx` (`codGerenciador`),
  KEY `FK_CURSO_idx` (`codCurso`),
  CONSTRAINT `FK_CURSO` FOREIGN KEY (`codCurso`) REFERENCES `cursos` (`codcurso`),
  CONSTRAINT `FK_GERENCIAOR` FOREIGN KEY (`codGerenciador`) REFERENCES `gerenciadores` (`codgerenciador`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projetos`
--

LOCK TABLES `projetos` WRITE;
/*!40000 ALTER TABLE `projetos` DISABLE KEYS */;
INSERT INTO `projetos` VALUES (42,'Projeto','descricao','ADS-PROJETO-2019-10-30-0XA63950.pdf',0,0,0,0,0.00,'2019-10-30','2019-10-30 18:08:54',2,2,1,''),(43,'tit','des','ADS-TIT-2019-11-01-0X710B8F.pdf',0,0,0,0,0.00,'1232-09-17','2019-11-01 16:42:11',2,2,1,''),(44,'teste ori','qoejhoqdqiow fdde desc','JD-TESTE-ORI-2019-11-04-0X4A63A5.pdf',0,0,0,0,0.00,'2019-10-14','2019-11-04 17:52:08',2,1,1,''),(45,'teste ori 2','qoejhoqdqiow fdde desc 2','JD-TESTE-ORI-2-2019-11-04-0XA15714.pdf',0,0,0,0,0.00,'2019-07-19','2019-11-04 17:59:18',2,1,1,'');
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
  `ativo` int(11) NOT NULL,
  `codGerenciador` int(11) NOT NULL,
  PRIMARY KEY (`codUsuario`),
  UNIQUE KEY `nomeUsuario_UNIQUE` (`nomeUsuario`),
  KEY `FK_GERENCIADOR_idx` (`codGerenciador`),
  CONSTRAINT `FK_GERENCIADOR` FOREIGN KEY (`codGerenciador`) REFERENCES `gerenciadores` (`codgerenciador`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','pbkdf2:sha256:50000$ugKk3qk8$a68e58926f85dff54dd23416597dff7465f9855ff94f877d9dbdc4243e1d80d9',3,1,2),(9,'pedro','pbkdf2:sha256:150000$11LdKkAa$35848c4199690f50c414c1b7498d542cc29cea3e8d3168a9d94fcc574cdcfc71',3,1,1);
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

-- Dump completed on 2019-11-12 21:44:34

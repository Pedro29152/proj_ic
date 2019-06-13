-- MySQL dump 10.13  Distrib 8.0.16, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: proj_ic
-- ------------------------------------------------------
-- Server version	8.0.16

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
  `raAutor` varchar(12) NOT NULL,
  `nomeAutor` varchar(200) NOT NULL,
  PRIMARY KEY (`codAutor`),
  UNIQUE KEY `raAutor_UNIQUE` (`raAutor`),
  UNIQUE KEY `codAutor_UNIQUE` (`codAutor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autores`
--

LOCK TABLES `autores` WRITE;
/*!40000 ALTER TABLE `autores` DISABLE KEYS */;
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
  `abreviacao` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`codCurso`),
  UNIQUE KEY `abreviacao_UNIQUE` (`abreviacao`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  PRIMARY KEY (`codGerenciador`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gerenciadores`
--

LOCK TABLES `gerenciadores` WRITE;
/*!40000 ALTER TABLE `gerenciadores` DISABLE KEYS */;
INSERT INTO `gerenciadores` VALUES (1,'12312312312','fatec','gay'),(2,'12332112312','FateB','Une Persona');
/*!40000 ALTER TABLE `gerenciadores` ENABLE KEYS */;
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
  CONSTRAINT `FK_PALAVRA_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codProjeto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `palavras_chave`
--

LOCK TABLES `palavras_chave` WRITE;
/*!40000 ALTER TABLE `palavras_chave` DISABLE KEYS */;
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
  CONSTRAINT `FK_AUTOR` FOREIGN KEY (`codAutor`) REFERENCES `autores` (`codAutor`),
  CONSTRAINT `FK_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codProjeto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projeto_autor`
--

LOCK TABLES `projeto_autor` WRITE;
/*!40000 ALTER TABLE `projeto_autor` DISABLE KEYS */;
/*!40000 ALTER TABLE `projeto_autor` ENABLE KEYS */;
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
  `nomeOrientador` varchar(100) NOT NULL,
  `descricao` longtext NOT NULL,
  `nomeArquivo` varchar(80) NOT NULL,
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
  PRIMARY KEY (`codProjeto`),
  KEY `FK_GERENCIAOR_idx` (`codGerenciador`),
  KEY `FK_CURSO_idx` (`codCurso`),
  CONSTRAINT `FK_CURSO` FOREIGN KEY (`codCurso`) REFERENCES `cursos` (`codCurso`),
  CONSTRAINT `FK_GERENCIAOR` FOREIGN KEY (`codGerenciador`) REFERENCES `gerenciadores` (`codGerenciador`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projetos`
--

LOCK TABLES `projetos` WRITE;
/*!40000 ALTER TABLE `projetos` DISABLE KEYS */;
INSERT INTO `projetos` VALUES (9,'nome lorem lorem nome lorem lorem nome lorem lorem nome lorem lorem nome lorem lorem nome lorem lore','asdas','wqeaeee','ADS-NLLNLLNLLNLLNLLNLL-2019-05-22-0X993AB3.jpeg',0,0,0,0,7.00,'2019-05-08','2019-05-22 23:25:13',2,2,1),(10,'bom dia man','ooosmkd','asmdoamsodmaoskdmasokdm','ADS-BOM-DIA-MAN-2019-05-23-0X78A11A.pdf',0,0,0,0,4.50,'2000-03-01','2019-05-23 18:43:34',2,2,1),(11,'toptop','2','qs','JD-TOPTOP-2019-06-10-0X56141C.pdf',0,0,0,0,3.00,'2019-06-20','2019-06-10 21:06:25',2,1,1),(12,'sla man kkkkkkkkkkkkkkk','asdas','ssasdasd','JD-SLA-MAN-KKKKKKKKKKKKKKK-2019-06-10-0XA95CEF.pdf',0,0,0,0,3.00,'2019-06-28','2019-06-10 21:07:22',2,1,1),(13,'titullo','salve','asoiajsoaknsd','JD-TITULLO-2019-06-10-0X3DDE70.pdf',0,0,0,0,9.90,'2019-06-07','2019-06-10 21:54:14',2,1,1);
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
  KEY `FK_GERENCIADOR_idx` (`codGerenciador`),
  CONSTRAINT `FK_GERENCIADOR` FOREIGN KEY (`codGerenciador`) REFERENCES `gerenciadores` (`codGerenciador`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','pbkdf2:sha256:50000$ugKk3qk8$a68e58926f85dff54dd23416597dff7465f9855ff94f877d9dbdc4243e1d80d9',3,1,2),(4,'disney','pbkdf2:sha256:50000$zUdr3r5C$7f2bed966da6205d972f22d79c06be28f21e9b1e004992513f966f6c06c260a3',1,1,1),(5,'pedro-vitorio@hotmail.com','pbkdf2:sha256:50000$VKwcWIhd$62c3d81302c5f29b092c89865022cbd1c1e35e704a505ddba17a497f1cf9d74e',1,1,2);
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

-- Dump completed on 2019-06-10 21:59:26

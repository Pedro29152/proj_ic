-- MySQL dump 10.13  Distrib 8.0.16, for Win64 (x86_64)
--
-- Host: localhost    Database: proj_ic
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
  `raAutor` varchar(13) NOT NULL,
  `nomeAutor` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`codAutor`),
  UNIQUE KEY `codAutor_UNIQUE` (`codAutor`),
  UNIQUE KEY `email_ra_UNIQUE` (`email`,`raAutor`) /*!80000 INVISIBLE */,
  UNIQUE KEY `raAutor_UNIQUE` (`raAutor`)
) ENGINE=InnoDB AUTO_INCREMENT=146 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autores`
--

LOCK TABLES `autores` WRITE;
/*!40000 ALTER TABLE `autores` DISABLE KEYS */;
/*!40000 ALTER TABLE `autores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coordenadores`
--

DROP TABLE IF EXISTS `coordenadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `coordenadores` (
  `codCoordenador` int(11) NOT NULL AUTO_INCREMENT,
  `nomeCoordenador` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `ativo` int(11) NOT NULL DEFAULT '1',
  `codCurso` int(11) NOT NULL,
  `codUsuario` int(11) DEFAULT NULL,
  PRIMARY KEY (`codCoordenador`),
  UNIQUE KEY `codCurso_UNIQUE` (`codCurso`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `codUsuario_UNIQUE` (`codUsuario`),
  KEY `FK_COORDENADOR_USUARIO_idx` (`codUsuario`) /*!80000 INVISIBLE */,
  KEY `FK_COORDENADOR_CURSO_idx` (`codCurso`,`ativo`),
  CONSTRAINT `FK_COORDENADOR_CURSO` FOREIGN KEY (`codCurso`) REFERENCES `cursos` (`codCurso`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_COORDENADOR_USUARIO` FOREIGN KEY (`codUsuario`) REFERENCES `usuarios` (`codUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coordenadores`
--

LOCK TABLES `coordenadores` WRITE;
/*!40000 ALTER TABLE `coordenadores` DISABLE KEYS */;
/*!40000 ALTER TABLE `coordenadores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cursos`
--

DROP TABLE IF EXISTS `cursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `cursos` (
  `codCurso` int(11) NOT NULL AUTO_INCREMENT,
  `descricaoCurso` varchar(255) NOT NULL,
  `ativo` int(11) NOT NULL,
  `abreviacao` varchar(5) NOT NULL,
  PRIMARY KEY (`codCurso`),
  UNIQUE KEY `abreviacao_UNIQUE` (`abreviacao`),
  UNIQUE KEY `descricaoCurso_UNIQUE` (`descricaoCurso`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `nomeOrientador` varchar(255) NOT NULL,
  `raOrientador` varchar(14) NOT NULL,
  `currLattes` varchar(256) NOT NULL,
  `email` varchar(256) NOT NULL,
  `ativo` int(11) NOT NULL DEFAULT '1',
  `codUsuario` int(11) DEFAULT NULL,
  PRIMARY KEY (`codOrientador`),
  UNIQUE KEY `raOrientador_UNIQUE` (`raOrientador`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `codUsuario_UNIQUE` (`codUsuario`),
  CONSTRAINT `FK_ORIENTADOR_USUARIO` FOREIGN KEY (`codUsuario`) REFERENCES `usuarios` (`codUsuario`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orientadores`
--

LOCK TABLES `orientadores` WRITE;
/*!40000 ALTER TABLE `orientadores` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  CONSTRAINT `FK_AUTOR` FOREIGN KEY (`codAutor`) REFERENCES `autores` (`codAutor`) ON DELETE CASCADE,
  CONSTRAINT `FK_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codprojeto`) ON DELETE CASCADE
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
  CONSTRAINT `FK_ORIENTADOR` FOREIGN KEY (`codOrientador`) REFERENCES `orientadores` (`codOrientador`) ON DELETE CASCADE,
  CONSTRAINT `FK_PROJETO_ORI` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codprojeto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projeto_orientador`
--

LOCK TABLES `projeto_orientador` WRITE;
/*!40000 ALTER TABLE `projeto_orientador` DISABLE KEYS */;
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
  `tituloProjeto` longtext NOT NULL,
  `descricao` longtext NOT NULL,
  `nomeArquivo` varchar(120) NOT NULL,
  `numVisitas` int(11) NOT NULL DEFAULT '0',
  `numDownloads` int(11) NOT NULL DEFAULT '0',
  `dataAvaliacao` date NOT NULL,
  `dataEnvio` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codCurso` int(11) NOT NULL,
  `ativo` int(11) NOT NULL DEFAULT '1',
  `subTitulo` longtext NOT NULL,
  `status` int(11) NOT NULL DEFAULT '0',
  `linguagem` int(11) NOT NULL,
  PRIMARY KEY (`codProjeto`),
  UNIQUE KEY `nomeArquivo_UNIQUE` (`nomeArquivo`),
  UNIQUE KEY `codProjeto_UNIQUE` (`codProjeto`),
  KEY `FK_CURSO_idx` (`codCurso`),
  CONSTRAINT `FK_CURSO` FOREIGN KEY (`codCurso`) REFERENCES `cursos` (`codCurso`)
) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projetos`
--

LOCK TABLES `projetos` WRITE;
/*!40000 ALTER TABLE `projetos` DISABLE KEYS */;
/*!40000 ALTER TABLE `projetos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solicitacoes_revisao`
--

DROP TABLE IF EXISTS `solicitacoes_revisao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `solicitacoes_revisao` (
  `codSolicitacao` int(11) NOT NULL AUTO_INCREMENT,
  `mensagem` longtext,
  `dataSolicitacao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codUsuarioOrientado` int(11) NOT NULL,
  PRIMARY KEY (`codSolicitacao`),
  KEY `FK_SOLICITACAO_USUARIO_ORIENTADO` (`codUsuarioOrientado`),
  CONSTRAINT `FK_SOLICITACAO_USUARIO_ORIENTADO` FOREIGN KEY (`codUsuarioOrientado`) REFERENCES `usuario_orientado` (`codUsuarioOrientado`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitacoes_revisao`
--

LOCK TABLES `solicitacoes_revisao` WRITE;
/*!40000 ALTER TABLE `solicitacoes_revisao` DISABLE KEYS */;
/*!40000 ALTER TABLE `solicitacoes_revisao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario_orientado`
--

DROP TABLE IF EXISTS `usuario_orientado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `usuario_orientado` (
  `codUsuarioOrientado` int(11) NOT NULL AUTO_INCREMENT,
  `codOrientador` int(11) DEFAULT NULL,
  `codCoordenador` int(11) DEFAULT NULL,
  `codAutor` int(11) NOT NULL,
  `codUsuario` int(11) NOT NULL,
  `dataCriacao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dataValidade` datetime NOT NULL,
  `codCurso` int(11) NOT NULL,
  `codProjeto` int(11) DEFAULT NULL,
  PRIMARY KEY (`codUsuarioOrientado`),
  UNIQUE KEY `codAutor_UNIQUE` (`codAutor`,`codUsuario`) /*!80000 INVISIBLE */,
  UNIQUE KEY `codProjeto_UNIQUE` (`codProjeto`),
  KEY `FK_AUTOR_USUARIO_ORIENTADO_idx` (`codAutor`),
  KEY `FK_USUARIO_USUARIO_ORIENTADO_idx` (`codUsuario`),
  KEY `FK_CURSO_USUARIO_ORIENTADO_idx` (`codCurso`),
  KEY `FK_COORDENADOR_USUARIO_ORIENTADO` (`codCoordenador`),
  KEY `FK_ORIENTADOR_USUARIO_ORIENTADO` (`codOrientador`),
  KEY `FK_USUARIO_ORIENTADO_PROJETO_idx` (`codProjeto`),
  CONSTRAINT `FK_AUTOR_USUARIO_ORIENTADO` FOREIGN KEY (`codAutor`) REFERENCES `autores` (`codAutor`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_COORDENADOR_USUARIO_ORIENTADO` FOREIGN KEY (`codCoordenador`) REFERENCES `coordenadores` (`codCoordenador`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_CURSO_USUARIO_ORIENTADO` FOREIGN KEY (`codCurso`) REFERENCES `cursos` (`codCurso`),
  CONSTRAINT `FK_ORIENTADOR_USUARIO_ORIENTADO` FOREIGN KEY (`codOrientador`) REFERENCES `orientadores` (`codOrientador`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `FK_USUARIO_ORIENTADO_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codProjeto`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_USUARIO_USUARIO_ORIENTADO` FOREIGN KEY (`codUsuario`) REFERENCES `usuarios` (`codUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_orientado`
--

LOCK TABLES `usuario_orientado` WRITE;
/*!40000 ALTER TABLE `usuario_orientado` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuario_orientado` ENABLE KEYS */;
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
  `nome` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`codUsuario`),
  UNIQUE KEY `nomeUsuario_UNIQUE` (`nomeUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','pbkdf2:sha256:150000$7rHphFnD$397c0a570ba3810f5d5f2fbaea54139512a6309e3757fa1ef730d5ca2d73c5b9',4,1,'admin','admin@admin.com');
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

-- Dump completed on 2020-07-12 19:32:30

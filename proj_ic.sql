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
-- Table structure for table `proj_ic`.`autores`
--

DROP TABLE IF EXISTS `proj_ic`.`autores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`autores` (
  `codAutor` int(11) NOT NULL AUTO_INCREMENT,
  `raAutor` varchar(13) NOT NULL,
  `nomeAutor` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`codAutor`),
  UNIQUE KEY `codAutor_UNIQUE` (`codAutor`),
  UNIQUE KEY `email_ra_UNIQUE` (`email`,`raAutor`) /*!80000 INVISIBLE */,
  UNIQUE KEY `raAutor_UNIQUE` (`raAutor`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proj_ic`.`cursos`
--

DROP TABLE IF EXISTS `proj_ic`.`cursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`cursos` (
  `codCurso` int(11) NOT NULL AUTO_INCREMENT,
  `descricaoCurso` varchar(255) NOT NULL,
  `ativo` int(11) NOT NULL,
  `abreviacao` varchar(5) NOT NULL,
  `codUsuario` int(11) NOT NULL,
  PRIMARY KEY (`codCurso`),
  UNIQUE KEY `abreviacao_UNIQUE` (`abreviacao`),
  UNIQUE KEY `descricaoCurso_UNIQUE` (`descricaoCurso`),
  UNIQUE KEY `codUsuario_UNIQUE` (`codUsuario`),
  CONSTRAINT `FK_USUARIO_CURSO` FOREIGN KEY (`codUsuario`) REFERENCES `proj_ic`.`usuarios` (`codUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `proj_ic`.`logger`
--

DROP TABLE IF EXISTS `proj_ic`.`logger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`logger` (
  `codLog` int(11) NOT NULL AUTO_INCREMENT,
  `rotaCompleta` longtext NOT NULL,
  `requestDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `method` varchar(50) NOT NULL,
  `statusCode` int(11) NOT NULL,
  `ipAddress` varchar(20) DEFAULT NULL,
  `info` longtext,
  `requestData` longtext,
  `responseData` longtext,
  `codUsuario` int(11) DEFAULT NULL,
  PRIMARY KEY (`codLog`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

-- Table structure for table `proj_ic`.`orientadores`
--

DROP TABLE IF EXISTS `proj_ic`.`orientadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`orientadores` (
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
  CONSTRAINT `FK_ORIENTADOR_USUARIO` FOREIGN KEY (`codUsuario`) REFERENCES `proj_ic`.`usuarios` (`codUsuario`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proj_ic`.`palavras_chave`
--

DROP TABLE IF EXISTS `proj_ic`.`palavras_chave`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`palavras_chave` (
  `codPalavra` int(11) NOT NULL AUTO_INCREMENT,
  `palavraChave` varchar(50) NOT NULL,
  `codProjeto` int(11) NOT NULL,
  PRIMARY KEY (`codPalavra`),
  KEY `FK_PROJETO_idx` (`codProjeto`),
  CONSTRAINT `FK_PALAVRA_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `proj_ic`.`projetos` (`codprojeto`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proj_ic`.`projeto_autor`
--

DROP TABLE IF EXISTS `proj_ic`.`projeto_autor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`projeto_autor` (
  `codProjeto` int(11) NOT NULL,
  `codAutor` int(11) NOT NULL,
  PRIMARY KEY (`codProjeto`,`codAutor`),
  KEY `FK_AUTOR_idx` (`codAutor`),
  CONSTRAINT `FK_AUTOR` FOREIGN KEY (`codAutor`) REFERENCES `proj_ic`.`autores` (`codAutor`) ON DELETE CASCADE,
  CONSTRAINT `FK_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `proj_ic`.`projetos` (`codprojeto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proj_ic`.`projeto_orientador`
--

DROP TABLE IF EXISTS `proj_ic`.`projeto_orientador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`projeto_orientador` (
  `codOrientador` int(11) NOT NULL,
  `codProjeto` int(11) NOT NULL,
  `tipoOrientador` int(11) DEFAULT NULL,
  PRIMARY KEY (`codOrientador`,`codProjeto`),
  KEY `FK_PROJETO_ORI_idx` (`codProjeto`),
  CONSTRAINT `FK_ORIENTADOR` FOREIGN KEY (`codOrientador`) REFERENCES `proj_ic`.`orientadores` (`codOrientador`) ON DELETE CASCADE,
  CONSTRAINT `FK_PROJETO_ORI` FOREIGN KEY (`codProjeto`) REFERENCES `proj_ic`.`projetos` (`codprojeto`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proj_ic`.`projetos`
--

DROP TABLE IF EXISTS `proj_ic`.`projetos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`projetos` (
  `codProjeto` int(11) NOT NULL AUTO_INCREMENT,
  `tituloProjeto` longtext NOT NULL,
  `subtitulo` longtext,
  `descricao` longtext,
  `nomeArquivo` varchar(120) NOT NULL,
  `numVisitas` int(11) NOT NULL DEFAULT '0',
  `numDownloads` int(11) NOT NULL DEFAULT '0',
  `dataAvaliacao` date NOT NULL,
  `dataEnvio` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codCurso` int(11) NOT NULL,
  `ativo` int(11) NOT NULL DEFAULT '1',
  `status` int(11) NOT NULL DEFAULT '0',
  `linguagem` int(11) NOT NULL,
  `modalidade` int(11) NOT NULL,
  `localPublicacao` longtext,
  PRIMARY KEY (`codProjeto`),
  UNIQUE KEY `nomeArquivo_UNIQUE` (`nomeArquivo`),
  UNIQUE KEY `codProjeto_UNIQUE` (`codProjeto`),
  KEY `FK_CURSO_idx` (`codCurso`),
  CONSTRAINT `FK_CURSO` FOREIGN KEY (`codCurso`) REFERENCES `proj_ic`.`cursos` (`codCurso`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proj_ic`.`slides`
--

DROP TABLE IF EXISTS `proj_ic`.`slides`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`slides` (
  `codSlide` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` longtext,
  `subtitulo` longtext,
  `title` longtext,
  `subtitle` longtext,
  `imagem` varchar(255) NOT NULL,
  PRIMARY KEY (`codSlide`),
  UNIQUE KEY `imagem_UNIQUE` (`imagem`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Table structure for table `proj_ic`.`solicitacoes_revisao`
--

DROP TABLE IF EXISTS `proj_ic`.`solicitacoes_revisao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`solicitacoes_revisao` (
  `codSolicitacao` int(11) NOT NULL AUTO_INCREMENT,
  `mensagem` longtext,
  `dataSolicitacao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codUsuarioOrientado` int(11) NOT NULL,
  PRIMARY KEY (`codSolicitacao`),
  KEY `FK_SOLICITACAO_USUARIO_ORIENTADO` (`codUsuarioOrientado`),
  CONSTRAINT `FK_SOLICITACAO_USUARIO_ORIENTADO` FOREIGN KEY (`codUsuarioOrientado`) REFERENCES `proj_ic`.`usuario_orientado` (`codUsuarioOrientado`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proj_ic`.`usuario_orientado`
--

DROP TABLE IF EXISTS `proj_ic`.`usuario_orientado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`usuario_orientado` (
  `codUsuarioOrientado` int(11) NOT NULL AUTO_INCREMENT,
  `codOrientador` int(11) DEFAULT NULL,
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
  KEY `FK_ORIENTADOR_USUARIO_ORIENTADO` (`codOrientador`),
  KEY `FK_USUARIO_ORIENTADO_PROJETO_idx` (`codProjeto`),
  CONSTRAINT `FK_AUTOR_USUARIO_ORIENTADO` FOREIGN KEY (`codAutor`) REFERENCES `proj_ic`.`autores` (`codAutor`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_CURSO_USUARIO_ORIENTADO` FOREIGN KEY (`codCurso`) REFERENCES `proj_ic`.`cursos` (`codCurso`),
  CONSTRAINT `FK_ORIENTADOR_USUARIO_ORIENTADO` FOREIGN KEY (`codOrientador`) REFERENCES `proj_ic`.`orientadores` (`codOrientador`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `FK_USUARIO_ORIENTADO_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `proj_ic`.`projetos` (`codProjeto`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_USUARIO_USUARIO_ORIENTADO` FOREIGN KEY (`codUsuario`) REFERENCES `proj_ic`.`usuarios` (`codUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `proj_ic`.`usuarios`
--

DROP TABLE IF EXISTS `proj_ic`.`usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `proj_ic`.`usuarios` (
  `codUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `nomeUsuario` varchar(50) NOT NULL,
  `senha` varchar(100) NOT NULL,
  `tipoUsuario` int(11) NOT NULL,
  `ativo` int(11) NOT NULL DEFAULT '1',
  `nome` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`codUsuario`),
  UNIQUE KEY `nomeUsuario_UNIQUE` (`nomeUsuario`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proj_ic`.`usuarios`
--

LOCK TABLES `proj_ic`.`usuarios` WRITE;
/*!40000 ALTER TABLE `proj_ic`.`usuarios` DISABLE KEYS */;
INSERT INTO `proj_ic`.`usuarios` VALUES (1,'admin','pbkdf2:sha256:150000$C4IIWvwb$de5c8d5282ed9666d92b13df6fe15688b31c5eeebc2360afa726f08ff265d42c',4,1,'admin','admin@admin.com');
/*!40000 ALTER TABLE `proj_ic`.`usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-09 19:36:39

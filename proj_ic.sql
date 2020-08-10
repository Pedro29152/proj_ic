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
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autores`
--

LOCK TABLES `autores` WRITE;
/*!40000 ALTER TABLE `autores` DISABLE KEYS */;
INSERT INTO `autores` VALUES (139,'1234567890123','aluno','pedro.joao.pl@gmail.com'),(140,'1231231212312','autor aa','teste@teste.com'),(141,'123123122223','jojofeg','teste@teste.com'),(143,'1239011232231','autor-2-aluno','email2@mail2.com'),(146,'1234567890121','aluno 2','pedro.joao.pl@gmail.com'),(149,'1234567890120','aluno 3','pedro.joao.pl@gmail.com'),(152,'1234567890111','aluno 4','pedro.joao.pl@gmail.com'),(155,'1234567890112','aluno 5','pedro.joao.pl@gmail.com'),(158,'1234567890113','aluno 6','pedro.joao.pl@gmail.com');
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
  `descricaoCurso` varchar(255) NOT NULL,
  `ativo` int(11) NOT NULL,
  `abreviacao` varchar(5) NOT NULL,
  `codUsuario` int(11) NOT NULL,
  PRIMARY KEY (`codCurso`),
  UNIQUE KEY `abreviacao_UNIQUE` (`abreviacao`),
  UNIQUE KEY `descricaoCurso_UNIQUE` (`descricaoCurso`),
  UNIQUE KEY `codUsuario_UNIQUE` (`codUsuario`),
  CONSTRAINT `FK_USUARIO_CURSO` FOREIGN KEY (`codUsuario`) REFERENCES `usuarios` (`codUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cursos`
--

LOCK TABLES `cursos` WRITE;
/*!40000 ALTER TABLE `cursos` DISABLE KEYS */;
INSERT INTO `cursos` VALUES (1,'Jogos Digitais',1,'JD',95),(2,'Analise e Desenvolvimento de Sistemas',1,'ADS',106);
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
INSERT INTO `orientadores` VALUES (20,'orientador','1234567890123','http://lattes.teste.edu/','orientador@teste.com',1,97);
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
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `palavras_chave`
--

LOCK TABLES `palavras_chave` WRITE;
/*!40000 ALTER TABLE `palavras_chave` DISABLE KEYS */;
INSERT INTO `palavras_chave` VALUES (61,'palalalalaala',120),(63,'palavra pal',122),(64,'palavra p2l',123),(65,'palavra p2l',124),(67,'palavra p2l',126),(68,'palavra p2l',127);
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
INSERT INTO `projeto_autor` VALUES (122,139),(120,140),(120,141),(122,143),(123,143),(124,143),(126,143),(127,143),(123,146),(124,149),(126,155),(127,158);
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
  `tipoOrientador` int(11) DEFAULT NULL,
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
INSERT INTO `projeto_orientador` VALUES (20,120,0),(20,122,0),(20,123,0),(20,124,0),(20,126,0),(20,127,0),(20,132,0),(23,131,0),(23,133,0),(23,136,1),(26,134,0),(26,135,0),(26,136,0);
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
  `subTitulo` longtext,
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
  PRIMARY KEY (`codProjeto`),
  UNIQUE KEY `nomeArquivo_UNIQUE` (`nomeArquivo`),
  UNIQUE KEY `codProjeto_UNIQUE` (`codProjeto`),
  KEY `FK_CURSO_idx` (`codCurso`),
  CONSTRAINT `FK_CURSO` FOREIGN KEY (`codCurso`) REFERENCES `cursos` (`codCurso`)
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projetos`
--

LOCK TABLES `projetos` WRITE;
/*!40000 ALTER TABLE `projetos` DISABLE KEYS */;
INSERT INTO `projetos` VALUES (120,'projeto 1','projojojotjoejotjo 1','este teste esta aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','SIST-PROJETO-1-2020-07-12-262D81.PDF',0,0,'2020-07-12','2020-07-12 18:17:48',2,0,1,0,0),(122,'proj aluno 1','sub titulo 1 aluno','descricao/resumo 1 aluno','SIST-PROJ-ALUNO-1-2020-07-12-A37913.PDF',0,0,'2020-07-12','2020-07-12 19:29:08',2,1,1,0,0),(123,'proj aluno 2','sub titulo 2 aluno','descricao/resumo 2 aluno','SIST-PROJ-ALUNO-2-2020-07-12-929FC7.PDF',0,0,'2020-07-12','2020-07-12 20:10:15',2,1,2,0,0),(124,'proj aluno 3','sub titulo 3 aluno','descricao/resumo 3 aluno','SIST-PROJ-ALUNO-3-2020-07-12-267FE2.PDF',0,0,'2020-07-12','2020-07-12 20:14:36',2,1,2,0,0),(126,'proj aluno 4','sub titulo 4 aluno','descricao/resumo 4 aluno','SIST-PROJ-ALUNO-4-2020-07-12-B4E5E4.PDF',0,0,'2020-07-12','2020-07-12 20:38:15',2,1,2,0,0),(127,'proj aluno 6','sub titulo 6 aluno','descricao/resumo 6 aluno','SIST-PROJ-ALUNO-6-2020-07-12-240DB5.PDF',0,0,'2020-07-12','2020-07-12 22:39:31',2,1,1,0,0),(131,'proj aluno ori2','sub titulo ori2 aluno','descricao/resumo ori2 aluno','LOG-PROJ-ALUNO-ORI2-2020-07-13-2F1D65.PDF',0,0,'2020-07-13','2020-07-13 19:00:55',24,1,1,0,0),(132,'proj aluno ori2 2','sub titulo ori2 2 aluno','descricao/resumo ori2 2 aluno','LOG-PROJ-ALUNO-ORI2-2-2020-07-13-38CAD7.PDF',0,5,'2020-07-13','2020-07-13 20:30:16',24,1,0,0,0),(133,'proj aluno ori2 2','sub titulo ori2 2 aluno','descricao/resumo ori2 2 aluno','LOG-PROJ-ALUNO-ORI2-2-2020-07-13-4F3DF7.PDF',0,0,'2020-07-13','2020-07-13 20:34:18',24,1,1,0,0),(134,'projeto 2','projoj tjo 2','teste jojo','SIST-PROJETO-2-2020-07-23-D4B18F.PDF',0,3,'2020-07-12','2020-07-23 15:35:18',2,1,1,0,0),(135,'projeto 2','','','SIST-PROJETO-2-2020-08-10-B8455F.PDF',0,0,'2020-07-12','2020-08-10 17:14:17',2,1,1,0,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitacoes_revisao`
--

LOCK TABLES `solicitacoes_revisao` WRITE;
/*!40000 ALTER TABLE `solicitacoes_revisao` DISABLE KEYS */;
INSERT INTO `solicitacoes_revisao` VALUES (6,'Corrigir erro blablabal','2020-07-12 22:43:44',13);
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
  CONSTRAINT `FK_AUTOR_USUARIO_ORIENTADO` FOREIGN KEY (`codAutor`) REFERENCES `autores` (`codAutor`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_CURSO_USUARIO_ORIENTADO` FOREIGN KEY (`codCurso`) REFERENCES `cursos` (`codCurso`),
  CONSTRAINT `FK_ORIENTADOR_USUARIO_ORIENTADO` FOREIGN KEY (`codOrientador`) REFERENCES `orientadores` (`codOrientador`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `FK_USUARIO_ORIENTADO_PROJETO` FOREIGN KEY (`codProjeto`) REFERENCES `projetos` (`codProjeto`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_USUARIO_USUARIO_ORIENTADO` FOREIGN KEY (`codUsuario`) REFERENCES `usuarios` (`codUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_orientado`
--

LOCK TABLES `usuario_orientado` WRITE;
/*!40000 ALTER TABLE `usuario_orientado` DISABLE KEYS */;
INSERT INTO `usuario_orientado` VALUES (8,20,139,99,'2020-07-12 19:28:53','2020-08-11 19:28:53',2,122),(9,20,146,101,'2020-07-12 20:09:45','2020-08-11 20:09:45',2,123),(10,20,149,102,'2020-07-12 20:14:02','2020-08-11 20:14:02',2,124),(12,20,155,104,'2020-07-12 20:37:44','2020-08-11 20:37:44',2,126),(13,20,158,105,'2020-07-12 22:31:36','2020-08-11 22:31:36',2,127);
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
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`codUsuario`),
  UNIQUE KEY `nomeUsuario_UNIQUE` (`nomeUsuario`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','pbkdf2:sha256:150000$C4IIWvwb$de5c8d5282ed9666d92b13df6fe15688b31c5eeebc2360afa726f08ff265d42c',4,1,'admin','admin@admin.com'),(95,'coordenador1','pbkdf2:sha256:150000$nIkQgwVz$843d49106e605b9bec095ac122d7b88745a7972988811b67baa3ee12977ba50e',5,1,'coordenador','coordenador@coordenador.com'),(96,'secretaria','pbkdf2:sha256:150000$dUOaNcMT$09ddd8017fdf403242ddd958cc14e884d563f44b658815218201739908d009b7',3,1,'secretaria','secretaria@secretaria.com'),(97,'orientador','pbkdf2:sha256:150000$i2vsfiCz$00c92c56436405d8f96ba191c4e76f32c6afe899f67bc6bfcafd80363b27bd3a',2,1,'orientador','orientador@orientador.com'),(99,'1234567890123','pbkdf2:sha256:150000$rWKWq8zr$85d7fa5010801dfbb9bda6e204ab23d5d92d2549a9d65ef134cedd35383079d8',1,0,'aluno',NULL),(101,'1234567890121','pbkdf2:sha256:150000$nd8f89Zx$a3c4fa1e989a9b297e14641da4612dd7bcfbab3fb0da7392ada902c5e4a1d1c9',1,0,'aluno 2',NULL),(102,'1234567890120','pbkdf2:sha256:150000$Smv5oRl5$3678a1ba218d9b3e6c78fe2d050c0ad1d581e551ce5779bd0c5f0784c02a7987',1,0,'aluno 3',NULL),(103,'1234567890111','pbkdf2:sha256:150000$hg21AJwB$5ab5371f2064204417bb960e37a8db1ad599017357e685fa15b5f3e6d0e1b8e9',1,0,'aluno 4',NULL),(104,'1234567890112','pbkdf2:sha256:150000$6GBfb5FF$0f3b58b63895db6f59bddece48fa30926a393eded7583850bc4dfa46af75babf',1,0,'aluno 5',NULL),(105,'1234567890113','pbkdf2:sha256:150000$XImhg2yR$5c9c074878b3b1bca424c865c1a456a2d577b33ae1448f0fa63db77bc9e0941c',1,1,'aluno 6','pedro.joao.pl@gmail.com'),(106,'coordenador 2','pbkdf2:sha256:150000$nIkQgwVz$843d49106e605b9bec095ac122d7b88745a7972988811b67baa3ee12977ba50e',5,1,'coordenador 2','coordenador2@coordenador.com');
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

-- Dump completed on 2020-08-10 18:28:11

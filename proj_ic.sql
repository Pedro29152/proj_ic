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
) ENGINE=InnoDB AUTO_INCREMENT=139 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autores`
--

LOCK TABLES `autores` WRITE;
/*!40000 ALTER TABLE `autores` DISABLE KEYS */;
INSERT INTO `autores` VALUES (112,'1234567890132','aluno2','aluno2@aluno.com'),(114,'1239011231231','autor-2','email@mail.com'),(119,'1234567890123','aluno','aluno@aluno.com'),(122,'1231231212312','jojofeg','teste@teste.com'),(127,'123123122223','jojofeg','teste@teste.com'),(135,'1239011232231','autor-2-aluno','email2@mail2.com'),(136,'1234567890124','aluuuuuuu','aluno@teste.com');
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
  `nomeCoordenador` varchar(200) NOT NULL,
  `email` varchar(100) NOT NULL,
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coordenadores`
--

LOCK TABLES `coordenadores` WRITE;
/*!40000 ALTER TABLE `coordenadores` DISABLE KEYS */;
INSERT INTO `coordenadores` VALUES (1,'cordena ads','ads@teste.com',1,2,87),(3,'cordena jd','jd@teste.com',1,1,86);
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
  `descricaoCurso` varchar(50) NOT NULL,
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
  `nomeOrientador` varchar(200) NOT NULL,
  `raOrientador` varchar(20) NOT NULL,
  `currLattes` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `ativo` int(11) NOT NULL DEFAULT '1',
  `codUsuario` int(11) DEFAULT NULL,
  PRIMARY KEY (`codOrientador`),
  UNIQUE KEY `raOrientador_UNIQUE` (`raOrientador`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  UNIQUE KEY `codUsuario_UNIQUE` (`codUsuario`),
  CONSTRAINT `FK_ORIENTADOR_USUARIO` FOREIGN KEY (`codUsuario`) REFERENCES `usuarios` (`codUsuario`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orientadores`
--

LOCK TABLES `orientadores` WRITE;
/*!40000 ALTER TABLE `orientadores` DISABLE KEYS */;
INSERT INTO `orientadores` VALUES (16,'orientador','1234567890','http://lattes.cnpq.br/corucilo','orientador@orientador.com',1,69),(17,'orientador 2','12345678902','http://lattes.cnpq.br/corucilo2','orientador2@orientador.com',1,73),(18,'Oirentador JOJOFEG','12345678901234567890','http://lattes.aojo.edu/','ojoaoksj@teste.ca',0,NULL),(19,'oriTesteJojo','12345678901234567891','http://www.lattes.edu.br/','oriiteste@teste.com',0,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `palavras_chave`
--

LOCK TABLES `palavras_chave` WRITE;
/*!40000 ALTER TABLE `palavras_chave` DISABLE KEYS */;
INSERT INTO `palavras_chave` VALUES (51,'palavra 1',109),(52,'palavra 1',110),(53,'ojasdojasdsad',111),(54,'ojasdojasdsad',112),(55,'ojasdojasdsad',114),(56,'ojasdojasdsad',115),(57,'ojasdojasdsad',116),(58,'ojasdojasdsad',117),(59,'palavra pal',118),(60,'palavra pal',119);
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
INSERT INTO `projeto_autor` VALUES (109,112),(109,114),(110,114),(110,119),(118,119),(111,122),(112,122),(114,122),(115,122),(116,122),(117,122),(114,127),(115,127),(116,127),(117,127),(118,135),(119,135),(119,136);
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
INSERT INTO `projeto_orientador` VALUES (16,109),(16,110),(16,111),(16,112),(16,114),(16,115),(16,116),(16,117),(18,118),(17,119);
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
) ENGINE=InnoDB AUTO_INCREMENT=120 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projetos`
--

LOCK TABLES `projetos` WRITE;
/*!40000 ALTER TABLE `projetos` DISABLE KEYS */;
INSERT INTO `projetos` VALUES (109,'projeto aluno1','descricao\\resumo 1','JD-PROJETO-ALUNO1-2020-06-04-0X20C81A.PDF',0,0,'2020-06-02','2020-06-04 16:41:02',1,1,'sub titulo 1',1,0),(110,'projeto 1','descricao/resumo 1','JD-PROJETO-1-2020-06-19-935502.PDF',0,0,'2020-06-02','2020-06-19 17:01:33',1,1,'sub titulo 1',1,0),(111,'jojofeg','as','JD-JOJOFEG-2020-06-23-B853EE.PDF',0,0,'2020-05-26','2020-06-23 14:22:41',1,1,'jojofeg lixo kkvkkk',1,0),(112,'jojofeg','as','JD-JOJOFEG-2020-06-23-9E710E.PDF',0,0,'2020-05-26','2020-06-23 14:23:37',2,1,'jojofeg lixo kkvkkk',1,0),(114,'jojofeg','as','JD-JOJOFEG-2020-06-23-628CA1.PDF',0,0,'2020-05-26','2020-06-23 14:24:07',2,1,'jojofeg lixo kkvkkk',1,0),(115,'jojofeg','as','JD-JOJOFEG-2020-06-23-3D4817.PDF',0,0,'2020-05-26','2020-06-23 14:33:36',2,1,'jojofeg lixo kkvkkk',1,0),(116,'jojofeg','a teste aaaa','JD-JOJOFEG-2020-06-23-929E62.PDF',0,1,'2020-05-26','2020-06-23 14:41:15',1,1,'jojofeg lixo kkvkkk',1,0),(117,'jojofeg','a teste aaaa','JD-JOJOFEG-2020-06-25-731C36.PDF',0,0,'2020-05-26','2020-06-25 16:07:06',1,1,'jojofeg lixo kkvkkk',1,1),(118,'proj aluno 2','descricao/resumo 2 aluno','JD-PROJ-ALUNO-2-2020-07-03-20DE44.PDF',0,0,'2020-07-01','2020-07-03 15:27:59',1,1,'sub titulo 2 aluno',0,0),(119,'teste 1','descricao/resumo 2 aluno','SIST-PROJ-ALUNO-2-2020-07-07-97D128.PDF',0,1,'2020-07-01','2020-07-07 16:30:42',2,1,'sub titulo 2 aluno',0,0);
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
  `mensagem` varchar(200) DEFAULT NULL,
  `dataSolicitacao` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `codUsuarioOrientado` int(11) NOT NULL,
  PRIMARY KEY (`codSolicitacao`),
  KEY `FK_SOLICITACAO_USUARIO_ORIENTADO` (`codUsuarioOrientado`),
  CONSTRAINT `FK_SOLICITACAO_USUARIO_ORIENTADO` FOREIGN KEY (`codUsuarioOrientado`) REFERENCES `usuario_orientado` (`codUsuarioOrientado`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solicitacoes_revisao`
--

LOCK TABLES `solicitacoes_revisao` WRITE;
/*!40000 ALTER TABLE `solicitacoes_revisao` DISABLE KEYS */;
INSERT INTO `solicitacoes_revisao` VALUES (1,'','2020-07-09 03:52:22',3),(2,'','2020-07-09 19:22:51',6),(3,'Corrigir erro blablabal','2020-07-09 19:23:52',6);
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
  PRIMARY KEY (`codUsuarioOrientado`),
  UNIQUE KEY `codAutor_UNIQUE` (`codAutor`,`codUsuario`) /*!80000 INVISIBLE */,
  KEY `FK_AUTOR_USUARIO_ORIENTADO_idx` (`codAutor`),
  KEY `FK_USUARIO_USUARIO_ORIENTADO_idx` (`codUsuario`),
  KEY `FK_CURSO_USUARIO_ORIENTADO_idx` (`codCurso`),
  KEY `FK_COORDENADOR_USUARIO_ORIENTADO` (`codCoordenador`),
  KEY `FK_ORIENTADOR_USUARIO_ORIENTADO` (`codOrientador`),
  CONSTRAINT `FK_AUTOR_USUARIO_ORIENTADO` FOREIGN KEY (`codAutor`) REFERENCES `autores` (`codAutor`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_COORDENADOR_USUARIO_ORIENTADO` FOREIGN KEY (`codCoordenador`) REFERENCES `coordenadores` (`codCoordenador`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_CURSO_USUARIO_ORIENTADO` FOREIGN KEY (`codCurso`) REFERENCES `cursos` (`codCurso`),
  CONSTRAINT `FK_ORIENTADOR_USUARIO_ORIENTADO` FOREIGN KEY (`codOrientador`) REFERENCES `orientadores` (`codOrientador`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `FK_USUARIO_USUARIO_ORIENTADO` FOREIGN KEY (`codUsuario`) REFERENCES `usuarios` (`codUsuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_orientado`
--

LOCK TABLES `usuario_orientado` WRITE;
/*!40000 ALTER TABLE `usuario_orientado` DISABLE KEYS */;
INSERT INTO `usuario_orientado` VALUES (1,16,NULL,112,70,'2020-06-04 14:52:53','2020-07-04 14:52:53',1),(2,16,NULL,119,72,'2020-06-19 17:00:34','2020-07-19 17:00:34',1),(3,17,NULL,119,79,'2020-06-26 15:52:36','2020-07-26 15:52:36',1),(4,NULL,3,119,80,'2020-07-01 21:48:22','2020-07-31 21:48:22',1),(5,NULL,3,119,82,'2020-07-01 21:49:47','2020-07-31 21:49:47',1),(6,17,NULL,136,84,'2020-07-07 16:29:56','2020-08-06 16:29:56',2);
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
  `nome` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  PRIMARY KEY (`codUsuario`),
  UNIQUE KEY `nomeUsuario_UNIQUE` (`nomeUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','pbkdf2:sha256:150000$7rHphFnD$397c0a570ba3810f5d5f2fbaea54139512a6309e3757fa1ef730d5ca2d73c5b9',4,1,'admin','admin@admin.com'),(69,'professor','pbkdf2:sha256:150000$OVCxAVvj$8201f99b0f6e3999ded3dfbaa802b35f81ebd18e3e16e4c4f91b0903882327ea',2,1,'professor','professor@professor.com'),(70,'aluno2','pbkdf2:sha256:150000$twwOG5FU$41f8acdbf92eb1cd65539866cafbb2515984d2a0186bedc0b7d7983805fd9bd9',1,0,'aluno2','aluno2@aluno.com'),(71,'secretaria','pbkdf2:sha256:150000$bZ1vLB3W$b574ea1aba7b87c722087e2d0a363883a939adbb947367238eb8a8f8cdc22292',3,1,'secretaria','secreataria@secreataria.com'),(72,'aluno','pbkdf2:sha256:150000$xWk5qTpT$9218f17dbcec9b77b5ef5e9086fe1ac8a04176a33f7c79d37e9feb57cef874ea',1,0,'aluno','aluno@aluno.com'),(73,'professor2','pbkdf2:sha256:150000$Qgnz6KCU$53aa6239150f4a11da759507f1f7f9a007b2b9ee10501194d2e5e4bdcf45e16f',2,1,'professor dois','professor2@professor2.com'),(75,'oriteste','pbkdf2:sha256:150000$LXLhOqiB$0a1324bf8add3978af777d181d83fdad6d52a9800ce08e6e507af425600b0b0e',2,0,'Oirentador JOJOFEG','pedro.joao.pl@gmail.com'),(79,'alunoteste','pbkdf2:sha256:150000$1ifioFwq$10960f10bd4e5ec2a86245894cef5a3fd1c890ad131e37643b902fb31d3f6ce4',1,0,'aluno','aluno2joj@aluno2.com'),(80,'22222222','pbkdf2:sha256:150000$if6wsAEX$84fb67bfe001ca1712d0ccb3351431dcfc01dd8a0668983ed64f2a631c41828f',1,0,'alune','alune@lll.com.br'),(82,'1234567890123','pbkdf2:sha256:150000$692p6DOi$90be0728146fcab8d8dc639ec90de61aa9c6659a3c82fb46492a55c7ef31c591',1,1,'alunaae','pedro-vitorio@hotmail.com'),(84,'1234567890124','pbkdf2:sha256:150000$ReWHEIcq$8db2653de9ac6f5ef0e493b544561900507ba8d494e3d62293966fdab32cd7b3',1,1,'aluuuuuuu','aluno@teste.com'),(85,'oritesteJOJO','pbkdf2:sha256:150000$5YA3Kbw2$08669015163055a4381e0d33c57fb8962e301d4872fa401a3abc3d2263b34f47',2,0,'oritesteJOJO','oritestejojo@professor2.com'),(86,'coordenadorjd','pbkdf2:sha256:150000$5YA3Kbw2$08669015163055a4381e0d33c57fb8962e301d4872fa401a3abc3d2263b34f47',5,1,'coordteste','coorde@teste.com'),(87,'coordenadorads','pbkdf2:sha256:150000$5YA3Kbw2$08669015163055a4381e0d33c57fb8962e301d4872fa401a3abc3d2263b34f47',5,1,'coorde','coordeteste@teste.com'),(88,'coordteste','pbkdf2:sha256:150000$fgaufQie$93ae638c9966548cb20d59a6954cdb6ce6c99b1ca53d2bf2f92828682bdda1c9',5,1,'JOsefa','teste@teste.com');
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

-- Dump completed on 2020-07-09 19:27:31

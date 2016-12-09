-- MySQL dump 10.13  Distrib 5.7.16, for Linux (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	5.7.16-0ubuntu0.16.04.1

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
-- Table structure for table `live_taobao_webstar_crawl_goods_info`
--

DROP TABLE IF EXISTS `live_taobao_webstar_crawl_goods_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_taobao_webstar_crawl_goods_info` (
  `goods_id` varchar(45) NOT NULL,
  `crawl_time` varchar(45) NOT NULL,
  `goods_price` varchar(45) DEFAULT NULL,
  `comment_count` varchar(45) DEFAULT NULL,
  `comment_summary` longtext,
  `service` varchar(45) DEFAULT NULL,
  `service_rate` varchar(45) DEFAULT NULL,
  `description` varchar(45) DEFAULT NULL,
  `description_rate` varchar(45) DEFAULT NULL,
  `logistics` varchar(45) DEFAULT NULL,
  `logistics_rate` varchar(45) DEFAULT NULL,
  `confirm_goods_count` varchar(45) DEFAULT NULL,
  `different_price` longtext,
  `sold_total_count` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`goods_id`,`crawl_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `live_taobao_webstar_crawl_live_basic`
--

DROP TABLE IF EXISTS `live_taobao_webstar_crawl_live_basic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_taobao_webstar_crawl_live_basic` (
  `zhubo_id` varchar(45) NOT NULL,
  `crawl_time` varchar(45) NOT NULL,
  `live_id` varchar(45) NOT NULL,
  `user_info_json` longtext,
  `goods_json` longtext,
  `live_url` varchar(100) DEFAULT NULL,
  `is_live` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`zhubo_id`,`crawl_time`,`live_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `live_taobao_webstar_crawl_live_danmu`
--

DROP TABLE IF EXISTS `live_taobao_webstar_crawl_live_danmu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_taobao_webstar_crawl_live_danmu` (
  `live_id` varchar(45) NOT NULL,
  `crawl_time` varchar(45) NOT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  `action` varchar(45) DEFAULT NULL,
  `comment` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`live_id`,`crawl_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `live_taobao_webstar_crawl_live_dynamic`
--

DROP TABLE IF EXISTS `live_taobao_webstar_crawl_live_dynamic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_taobao_webstar_crawl_live_dynamic` (
  `live_id` varchar(45) NOT NULL,
  `crawl_time` varchar(45) NOT NULL,
  `attention` varchar(45) DEFAULT NULL,
  `watching` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`live_id`,`crawl_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `live_taobao_webstar_crawl_live_goods`
--

DROP TABLE IF EXISTS `live_taobao_webstar_crawl_live_goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_taobao_webstar_crawl_live_goods` (
  `live_id` varchar(45) NOT NULL,
  `goods_id` varchar(45) NOT NULL,
  `goods_title` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`live_id`,`goods_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `live_taobao_webstar_crawl_zhubo_info`
--

DROP TABLE IF EXISTS `live_taobao_webstar_crawl_zhubo_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `live_taobao_webstar_crawl_zhubo_info` (
  `zhubo_id` varchar(45) NOT NULL,
  `zhubo_name` varchar(45) NOT NULL,
  `zhubo_url` varchar(100) NOT NULL,
  `zhubo_fans` varchar(45) NOT NULL,
  `zhubo_profile` varchar(100) NOT NULL DEFAULT '达人',
  `zhubo_identity` varchar(100) NOT NULL DEFAULT '达人',
  `zhubo_authen_infor` varchar(45) NOT NULL DEFAULT '无',
  PRIMARY KEY (`zhubo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-12-06 14:23:03

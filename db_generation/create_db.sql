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

CREATE DATABASE `telegram_bot_data`;
USE `telegram_bot_data`;


select 'Create users table' AS '';

DROP TABLE IF EXISTS `telegram_users`;
CREATE TABLE `telegram_users` (
  `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  `e_mail` VARCHAR(100) NOT NULL,
  `personal_account` VARCHAR(100) NOT NULL,
  `telegram_token` VARCHAR(100),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `telegram_token_index`(`telegram_token`),
  UNIQUE INDEX `personal_account_index`(`personal_account`)
)
ENGINE = MyISAM;

select 'Insert data into users table' AS '';

LOAD DATA LOCAL INFILE '/data/users_data.csv' INTO TABLE `telegram_users` FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
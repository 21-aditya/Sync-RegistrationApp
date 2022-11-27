CREATE DATABASE IF NOT EXISTS `sync` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `sync`;

CREATE TABLE IF NOT EXISTS `accounts` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(50) NOT NULL,
        `roll` varchar(12) NOT NULL,
        `contact` varchar(12) NOT NULL,
        `email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
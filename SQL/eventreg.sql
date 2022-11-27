USE `sync`;
CREATE TABLE IF NOT EXISTS `eventreg` (
        `id` int(11) NOT NULL AUTO_INCREMENT,
        `name` varchar(50) NOT NULL,
        `roll` varchar(12) NOT NULL,
        `event` varchar(100) NOT NULL,
        PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
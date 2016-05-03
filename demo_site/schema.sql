CREATE TABLE `t_cor_correction` (
  `cor_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `cor_pre_id` bigint(20) NOT NULL,
  `cor_correction` enum('male','female','correct','other') DEFAULT NULL,
  `cor_ts` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`cor_id`),
  KEY `prediction_id` (`cor_pre_id`),
  KEY `correction` (`cor_correction`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;


CREATE TABLE `t_pre_prediction` (
  `pre_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `pre_term` varchar(500) NOT NULL,
  `pre_type` enum('url','twitter_username','first_name') DEFAULT NULL,
  `pre_prediction` varchar(45) DEFAULT NULL,
  `pre_count` int(11) DEFAULT '1',
  `pre_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `pre_last_accessed` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`pre_id`),
  KEY `term` (`pre_term`(191)),
  KEY `type` (`pre_type`),
  KEY `prediction` (`pre_prediction`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

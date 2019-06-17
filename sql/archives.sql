CREATE TABLE IF NOT EXISTS `images`.`archives` (
  `archive_id` INT(11) NOT NULL,
  `archive` VARCHAR(200) NOT NULL,
  `former_name` VARCHAR(100) NULL,
  `hosting_organization` VARCHAR(200) NULL,
  `country` VARCHAR(45) NULL,
  `url` VARCHAR(100) NULL,
  `api_url` VARCHAR(200) NULL,
  `api_docs` VARCHAR(2000) NULL,
  `notes` VARCHAR(45) NULL,
  PRIMARY KEY (`archive_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

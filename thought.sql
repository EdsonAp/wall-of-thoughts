-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema thoughtsdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema thoughtsdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `thoughtsdb` ;
USE `thoughtsdb` ;

-- -----------------------------------------------------
-- Table `thoughtsdb`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thoughtsdb`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `thoughtsdb`.`followers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thoughtsdb`.`followers` (
  `follower` INT(11) NOT NULL,
  `following` INT(11) NOT NULL,
  PRIMARY KEY (`follower`, `following`),
  INDEX `fk_users_has_users_users2_idx` (`following` ASC),
  INDEX `fk_users_has_users_users1_idx` (`follower` ASC),
  CONSTRAINT `fk_users_has_users_users1`
    FOREIGN KEY (`follower`)
    REFERENCES `thoughtsdb`.`users` (`id`),
  CONSTRAINT `fk_users_has_users_users2`
    FOREIGN KEY (`following`)
    REFERENCES `thoughtsdb`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `thoughtsdb`.`thoughts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thoughtsdb`.`thoughts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `message` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  `user_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_thoughts_users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_thoughts_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `thoughtsdb`.`users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 20
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `thoughtsdb`.`like_thoughts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `thoughtsdb`.`like_thoughts` (
  `thoughts_id` INT(11) NOT NULL,
  `users_id` INT(11) NOT NULL,
  PRIMARY KEY (`thoughts_id`, `users_id`),
  INDEX `fk_users_has_thoughts_thoughts1_idx` (`thoughts_id` ASC),
  INDEX `fk_users_has_thoughts_users_idx` (`users_id` ASC),
  CONSTRAINT `fk_users_has_thoughts_thoughts1`
    FOREIGN KEY (`thoughts_id`)
    REFERENCES `thoughtsdb`.`thoughts` (`id`),
  CONSTRAINT `fk_users_has_thoughts_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `thoughtsdb`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

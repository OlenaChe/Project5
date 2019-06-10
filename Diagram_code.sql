-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Projet5
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Projet5
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Projet5` DEFAULT CHARACTER SET utf8 ;
USE `Projet5` ;

-- -----------------------------------------------------
-- Table `Projet5`.`product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Projet5`.`product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nom` VARCHAR(100) NOT NULL,
  `description` VARCHAR(150) NULL,
  `url` VARCHAR(45) NOT NULL,
  `score` CHAR(1) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Projet5`.`store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Projet5`.`store` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Projet5`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Projet5`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Projet5`.`product_has_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Projet5`.`product_has_category` (
  `product_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  PRIMARY KEY (`product_id`, `category_id`),
  INDEX `fk_product_has_category_category1_idx` (`category_id` ASC) VISIBLE,
  INDEX `fk_product_has_category_product1_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `fk_product_has_category_product1`
    FOREIGN KEY (`product_id`)
    REFERENCES `Projet5`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_has_category_category1`
    FOREIGN KEY (`category_id`)
    REFERENCES `Projet5`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Projet5`.`substitute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Projet5`.`substitute` (
  `usual_product_id` INT NULL,
  `healthy_product_id1` INT NULL,
  INDEX `fk_substitute_product1_idx` (`usual_product_id` ASC) VISIBLE,
  INDEX `fk_substitute_product2_idx` (`healthy_product_id1` ASC) VISIBLE,
  CONSTRAINT `fk_substitute_product1`
    FOREIGN KEY (`usual_product_id`)
    REFERENCES `Projet5`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_substitute_product2`
    FOREIGN KEY (`healthy_product_id1`)
    REFERENCES `Projet5`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Projet5`.`product_has_store`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Projet5`.`product_has_store` (
  `product_id` INT NOT NULL,
  `store_id` INT NOT NULL,
  PRIMARY KEY (`product_id`, `store_id`),
  INDEX `fk_product_has_store1_store1_idx` (`store_id` ASC) VISIBLE,
  INDEX `fk_product_has_store1_product1_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `fk_product_has_store1_product1`
    FOREIGN KEY (`product_id`)
    REFERENCES `Projet5`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_has_store1_store1`
    FOREIGN KEY (`store_id`)
    REFERENCES `Projet5`.`store` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

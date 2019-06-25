
CREATE DATABASE Project5;
USE Project5;

CREATE TABLE category (
  id SMALLINT NOT NULL AUTO_INCREMENT = 1,
  name VARCHAR(45) NOT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB;


CREATE TABLE product (
  id INT(11) NOT NULL AUTO_INCREMENT = 1,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(150) NOT NULL,
  url VARCHAR(200) NOT NULL,
  score CHAR(1) NOT NULL,
  category_id SMALLINT NOT NULL,
  store VARCHAR(200) NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_product_category_idx (category_id ASC) VISIBLE,
  CONSTRAINT fk_product_category
    FOREIGN KEY (category_id)
    REFERENCES category (id))
ENGINE = InnoDB;


CREATE TABLE substitute (
  usual_product_id INT(11) NULL DEFAULT NULL,
  healthy_product_id INT(11) NULL DEFAULT NULL,
  INDEX fk_substitute_product1_idx (usual_product_id ASC) VISIBLE,
  INDEX fk_substitute_product2_idx (healthy_product_id ASC) VISIBLE,
  CONSTRAINT fk_substitute_product1
    FOREIGN KEY (usual_product_id)
    REFERENCES product.id,
  CONSTRAINT fk_substitute_product2
    FOREIGN KEY (healthy_product_id)
    REFERENCES product (id))
ENGINE = InnoDB;
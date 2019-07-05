import requests
import pymysql

from constants import *
from private import *


class Data_OFF():
    """Class defines the data which we want to get from Open Food Facts
    using the library request"""
    def __init__(self):
        self.categories = LIST_CATEGORIES

    def get_data(self):
        """Method which get the necessary information in certain categories"""
        all_products = []
        self.cat_number = 1
        for category in self.categories:
            p = {"search_terms": category, "json": 1, "page_size": 100}
            r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl",
                             params=p)
            i = 0
            for i in range(100):
                if i < NUM_PRODUCTS:
                    product = {"name": "", "description": "", "url": "",
                               "score": "", "category": "", "store": ""}
                    try:
                        if (len(r.json()["products"][i]["product_name_fr"]) >
                            2 and
                            len(r.json()["products"][i]["generic_name_fr"]) >
                            2 and
                            len(r.json()["products"][i]["url"]) >
                                2 and
                            (len(r.json()["products"][i]
                             ["nutrition_grade_fr"]) >= 1) and
                            len(r.json()["products"][i]["stores"]) > 2):
                                product["name"] = (r.json()["products"][i]
                                                   ["product_name_fr"])
                                product["description"] = \
                                    r.json()["products"][i]["generic_name_fr"]
                                product["url"] = \
                                    r.json()["products"][i]["url"]
                                product["store"] = \
                                    r.json()['products'][i]['stores']
                                product["category"] = self.cat_number
                                product["score"] = (r.json()["products"][i]
                                                    ["nutrition_grade_fr"])
                                product["store"] = \
                                    r.json()["products"][i]["stores"]
                                all_products.append(product)
                    except (TypeError):
                        pass
                    except (KeyError):
                        pass
                    i += 1
            self.cat_number += 1
        self.products = all_products
        return(self.products)


class Data_PB():
    """Claass defines the data which fills the database Pur Beurre"""
    def __init__(self):
        self.data_off = Data_OFF()

    def connect(self):
        """Method which creates la connection with PyMySQL"""
        self.connection = pymysql.connect(host=HOST,
                                          user=USER,
                                          password=PASSWORD,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def commit_connection(self):
        """Method which commit the changes with the database Pur Beurre"""
        self.connection.commit()

    def close_connection(self):
        """Method which closes the connection with the database Pur Beurre"""
        self.connection.close()

    def create_db(self):
        """Method which creates the database"""
        with self.connection.cursor() as cursor:
            sql_data = "CREATE DATABASE IF NOT EXISTS Project5;"
            cursor.execute(sql_data)
            self.commit_connection()

    def drop_db(self):
        """Method which deletes the database"""
        with self.connection.cursor() as cursor:
            sql_data = "DROP DATABASE IF EXISTS Project5;"
            cursor.execute(sql_data)
            self.commit_connection()

    def create_category(self):
        """Method which creates the table category"""
        with self.connection.cursor() as cursor:
            sql_data = "USE Project5;"
            cursor.execute(sql_data)
            sql_data = "CREATE TABLE category (\
                        id SMALLINT NOT NULL AUTO_INCREMENT,\
                        name VARCHAR(45) NOT NULL,\
                        PRIMARY KEY (id))\
                        ENGINE=InnoDB;"
            cursor.execute(sql_data)
            self.commit_connection()

    def create_product(self):
        """Method which creates the table product"""
        with self.connection.cursor() as cursor:
            sql_data = "USE Project5;"
            cursor.execute(sql_data)
            sql_data = "CREATE TABLE product (\
                        id INT(11) NOT NULL AUTO_INCREMENT, \
                        name VARCHAR(100) NOT NULL,\
                        description VARCHAR(150) NOT NULL,\
                        url VARCHAR(200) NOT NULL,\
                        score CHAR(1) NOT NULL,\
                        category_id SMALLINT NOT NULL,\
                        store VARCHAR(200) NOT NULL,\
                        PRIMARY KEY (id), INDEX fk_product_category_idx \
                            (category_id ASC) VISIBLE,\
                        CONSTRAINT fk_product_category\
                            FOREIGN KEY (category_id)\
                            REFERENCES category (id))\
                        ENGINE = InnoDB;"
            cursor.execute(sql_data)
            self.commit_connection()

    def create_substitute(self):
        """Method which creates the table substitute"""
        with self.connection.cursor() as cursor:
            sql_data = "USE Project5;"
            cursor.execute(sql_data)
            sql_data = "CREATE TABLE substitute (\
                        usual_product_id INT(11) NULL DEFAULT NULL,\
                        healthy_product_id INT(11) NULL DEFAULT NULL,\
                        INDEX fk_substitute_product1_idx \
                            (usual_product_id ASC) VISIBLE,\
                        INDEX fk_substitute_product2_idx \
                            (healthy_product_id ASC) VISIBLE,\
                        CONSTRAINT fk_substitute_product1\
                            FOREIGN KEY (usual_product_id)\
                            REFERENCES product(id),\
                        CONSTRAINT fk_substitute_product2\
                            FOREIGN KEY (healthy_product_id)\
                            REFERENCES product(id))\
                        ENGINE = InnoDB;"
            cursor.execute(sql_data)
            self.commit_connection()

    def insert_category(self):
        """Method which creates new records and commits the changes
in the table 'category'"""
        for category in LIST_CATEGORIES:
            with self.connection.cursor() as cursor:
                sql_data = "USE Project5;"
                cursor.execute(sql_data)
                sql_data = "INSERT INTO `category` (`name`) VALUES (%s)"
                cursor.execute(sql_data, category)
        self.commit_connection()

    def insert_product(self):
        """Method which creates new records and commits the changes
in the table 'product'"""
        for prod in self.data_off.get_data():
            with self.connection.cursor() as cursor:
                sql_data = "USE Project5;"
                cursor.execute(sql_data)
            with self.connection.cursor() as cursor:
                sql_data = "INSERT INTO `product` (`name`, `description`, \
                    `url`, `score`, `category_id`, `store`) \
                        VALUES (%s, %s, %s, %s, %s, %s)"
                try:
                    cursor.execute(sql_data, (prod['name'],
                                   prod['description'], prod['url'],
                                   prod['score'], prod['category'],
                                   prod['store']))
                except:
                    pass
        self.commit_connection()

    def find_from_table(self, search, column, table, how_many):
        """Method which gets the specific data from the table"""
        self.connect()
        with self.connection.cursor() as cursor:
            sql_data = "USE Project5;"
            cursor.execute(sql_data)
        with self.connection.cursor() as cursor:
            sql_data =\
                "SELECT DISTINCT * \
                    FROM `" + table + "` WHERE `" + column + "`=%s"
            cursor.execute(sql_data, (search))
            if how_many == 1:
                r = cursor.fetchone()
            else:
                r = cursor.fetchall()
        # self.close_connection()
        return r

    def insert_substitute(self, id1=None, id2=None):
        """Method which fils the table 'substitute'"""
        # self.connect()
        with self.connection.cursor() as cursor:
            sql_data = "USE Project5;"
            cursor.execute(sql_data)
        with self.connection.cursor() as cursor:
            sql_data = "INSERT INTO `substitute` \
                (`usual_product_id`, `healthy_product_id`) VALUES (%s, %s)"
            cursor.execute(sql_data, (id1, id2))
        self.commit_connection()
        # self.close_connection()

    def sql(self, sql, optional):
        """Method which executes mysql code"""
        self.connect()
        with self.connection.cursor() as cursor:
            sql_data = "USE Project5;"
            cursor.execute(sql_data)
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            if optional == "one":
                r = cursor.fetchone()
            elif optional == "all":
                r = cursor.fetchall()
        self.close_connection()
        return r


class Display_data():
    """Claass defines the data which enables the user to interact with DB"""
    def __init__(self):
        self.nutridict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
        self.substitute_list = []
        self.result = None
        self.data_pb = Data_PB()
        self.saved_data = Saved_data()

    def nutricompare(self, score1, score2):
        """Method which compares the nutriscores of two products"""
        return self.nutridict[score1] < self.nutridict[score2]

    def super_input(self, accepted_inputs):
        """Method which checks input for mistakes"""
        while True:
            the_input = input()
            for input1 in accepted_inputs:
                if str(input1) == the_input:
                    return the_input
            print("")
            print("Erreur. Vous avez entré un mauvais caractère'")
            print("Retapez, s'il vous plaît")
            print("")

    def choose_option(self):
        """Method which asks the user to choose the product to replace"""
        b = 1
        print("Choisissez une catégorie et entrez son numéro :")
        for category in LIST_CATEGORIES:
            print(str(b) + " : " + category)
            b += 1
        print("")
        self.choicecat = \
            int(self.super_input(range(1, len(LIST_CATEGORIES)+1)))
        self.result = self.data_pb.find_from_table(self.choicecat,
                                                   "category_id", "product",
                                                   NUM_PRODUCTS)
        print("")
        print("Sélectionnez le numéro du produit que vous voulez remplacer :")
        b = 1
        self.choices = {}
        for product in self.result:
            self.choices[b] = product
            print(str(b) + " : " + product['name'] + ", " + product['score'])
            b += 1
        print("")
        self.chosenproduct = \
            self.choices[int(self.super_input(range(1, len(self.choices)+1)))]

    def find_substutute(self):
        """Method which finds the substitute and displays its description"""
        self.substitute_list = []
        for product in self.result:
            if self.nutricompare(product['score'],
                                 self.chosenproduct['score']):
                self.substitute_list.append(product)
        print("")
        print("Choisissez un substitut et entrez son numéro:")
        b = 1
        self.choices = {}
        for product in self.substitute_list:
            self.choices[b] = product
            print(str(b) + " : " + product['name'] + ", " + product['score'])
            b += 1
        print("")
        if len(self.choices) == 0:
            print("Il n'y a pas de produit plus sain dans cette catégorie ")
            self.substitute = self.chosenproduct
        else:
            self.substitute = self.choices[int(self.super_input(range(1,
                                           len(self.substitute_list)+1)))]
        print("")
        print("Vous avez choisi : " + self.substitute['name'])
        print("Description : " + self.substitute['description'])
        print("URL : " + self.substitute['url'])
        print("NutriScore : " + self.substitute['score'])
        print("Catégorie : " + self.data_pb.find_from_table
              (self.substitute['category_id'], "id", "category", 1)['name'])
        print("Où acheter : " + self.substitute['store'])

    def add_data_choice(self):
        """Method which asks the user to save a substitute product
        into the list of healthy products"""
        print("")
        print("Enregistrer le résultat dans votre liste des produits sains ?")
        print("Si oui, tapez 'Y'. Si non, tapez 'N'.")
        print("")
        if self.super_input(["Y", "N"]) == "Y":
            id1 = str(self.data_pb.find_from_table
                      (self.chosenproduct['id'], "id", "product", 1)['id'])
            id2 = (str(self.data_pb.find_from_table(self.substitute['id'],
                   "id", "product", 1)['id']))
            self.data_pb.insert_substitute(id1, id2)
            print("")
            print("Le produit est ajouté dans la liste")


class Saved_data():
    """Claass defines the data which the user saves"""

    def display_result(self, result):
        """Method which displays the saved list of healthy products"""
        n = 1
        for dic in result:
            print("")
            print(n)
            print("")
            print("NOM DU PRODUIT SÉLECTIONNÉ : "+dic['produit'])
            print("DESCRIPTION : "+dic['description'])
            print("NUTRISCORE : "+dic['n_s'])
            print("URL : "+dic['url'])
            print("OÙ ACHETER : "+dic['magasins'])
            print("")
            n += 1
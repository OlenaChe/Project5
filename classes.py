import requests
import mysql
import pymysql
import pymysql.cursors

from constants import *
from private import *

class DataOFF():
    """Class defines the data which we want to get from Open Food Facts using the library request"""
    def __init__(self):
        self.categories = LIST_CATEGORIES      
        
    def get_data(self):
        """Method which get the necessary information in certain categories"""
        all_products = []
        self.cat_number = 1
        for category in self.categories:
            p = {"search_terms":category,"json":1, "page_size":100}
            r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl", params = p)
            i = 0
            for i in range(100):
                if i < NUM_PRODUCTS:
                    product = {"name": "", "description": "", "url": "", "score": "", "category": "", 
                                "store": ""}
                    try:
                        if (len(r.json()["products"][i]["product_name_fr"]) > 2 and
                            len(r.json()["products"][i]["generic_name_fr"]) > 2 and
                            len(r.json()["products"][i]["url"]) > 2 and 
                            len(r.json()["products"][i]["nutrition_grade_fr"]) >= 1 and 
                            len(r.json()["products"][i]["stores"]) > 2):
                            product["name"] = r.json()["products"][i]["product_name_fr"]
                            product["description"] = r.json()["products"][i]["generic_name_fr"]
                            product["url"] = r.json()["products"][i]["url"]
                            product["store"] = r.json()['products'][i]['stores']
                            product["category"] = self.cat_number
                            product["score"] = r.json()["products"][i]["nutrition_grade_fr"] 
                            product["store"] = r.json()["products"][i]["stores"] 
                            all_products.append(product)
                    except (TypeError):
                        print ("TypeError!")
                    except (KeyError):
                        print ("That key does not exist!")
                    i += 1
            self.cat_number += 1
        self.products = all_products  
        return(self.products)
      

class DataPB():
    """Claass defines the data which fills the database Pur Beurre """
    def __init__(self):
        self.data_off = DataOFF()

    def connect_db(self): 
        """Method which creates la connection with the database Pur Beurre"""       
        self.connection = pymysql.connect(host=HOST,
                                user=USER,
                                password=PASSWORD,
                                db=DB,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    def commit_connection(self):
        """Method which commit the changes"""
        self.connection.commit()
            
    def close_connection(self):
        """Method which closes the connection"""
        self.connection.close()

    def insert_category(self):
        """Method which creates new records and commits the changes in the table category"""
        self.connect_db()
        for category in LIST_CATEGORIES:
            with self.connection.cursor() as cursor:
                sql_data = "INSERT INTO `category` (`name`) VALUES (%s)"
                cursor.execute(sql_data, category)
        self.commit_connection()
        self.close_connection()

    def insert_product(self):
        """Method which creates new records and commits the changes in the table Product"""
        self.connect_db()
        for prod in self.data_off.get_data():
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `product` (`name`, `description`, `url`, `score`, `category_id`, `store`) VALUES (%s, %s, %s, %s, %s, %s)"
                try:
                    cursor.execute(sql, (prod['name'], prod['description'], prod['url'], prod['score'], prod['category'], prod['store'])) 
                except:
                    print("error")    
        self.commit_connection()
        self.close_connection()

    def clean(self, whattable):
        self.connect_db()
        with self.connection.cursor() as cursor:
            sqlclean = "DELETE FROM " + whattable
            cursor.execute(sqlclean)
            sqlreset = "ALTER TABLE " + whattable + " AUTO_INCREMENT = 1"
            cursor.execute(sqlreset)
        self.commit_connection()
        self.close_connection()

    def find_from_table(self, search, column, table, how_many):
        self.connect_db()
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `" + table + "` WHERE `" + column + "`=%s"
            cursor.execute(sql, (search))
            if how_many == 1: 
                r = cursor.fetchone()
            else:
                r = cursor.fetchall()
        self.close_connection()
        return r  
    
    def insert_substitute(self, id1 = None, id2 = None):
        self.connect_db()
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `substitute` (`usual_product_id`, `healthy_product_id`) VALUES (%s, %s)"
            cursor.execute(sql, (id1, id2))    
        self.commit_connection()
        self.close_connection()


class Display_data():
    """Claass defines the data """
    def __init__(self):
        self.nutridict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
        self.substitute_list = []
        self.result = None
        self.dataPB = DataPB()

    def nutricompare(self, score1, score2):
        return self.nutridict[score1] < self.nutridict[score2]

    def super_input(self, acsepted_inputs):
        while True:
            theinput = input()
            for input1 in acsepted_inputs:
                if str(input1) == theinput:
                    return theinput
            print("Mauvais numéro. Retapez s'il vous plaît") 

    def choose_option(self):
        print("Choisissez l'option et entrez le chiffre correspondant: 1 - Quel aliment souhaitez-vous remplacer ? 2 - Retrouver mes aliments substitués.")
        self.choice = self.super_input(['1','2'])
        if self.choice == "1":
            print("Choisissez la catégorie et entrez son numéro:")
            b = 1
            for category in LIST_CATEGORIES:
                print(str(b) + " : " + category)
                b += 1
            self.choicecat = int(self.super_input(range(1, len(LIST_CATEGORIES)+1)))
            self.result = self.dataPB.find_from_table(self.choicecat, "category_id", "product", NUM_PRODUCTS)
            print("")
            print("Sélectionnez le produit que vous voulez remplacer et entrez son numéro:")
            b = 1
            self.choices = {}
            for product in self.result:
                self.choices[b] = product
                print(str(b) + " : " + product['name'])
                b += 1
            self.chosenproduct = self.choices[int(self.super_input(range(1, len(self.choices)+1)))]

    def findsubstutute(self):
        for product in self.result:
            if self.nutricompare(product['score'], self.chosenproduct['score']):
                self.substitute_list.append(product)
        print('')
        print("Choisissez votre substitué et entrez son numéro:")
        b = 1
        self.choices = {}
        for product in self.substitute_list:
            self.choices[b] = product
            print(str(b) + " : " + product['name'] + ", " + product['score'])
            b +=1
        if len(self.choices) == 0:
            print("Désolé, il n'y a pas de produit plus sain que le vôtre dans cette catégorie ")
            self.substitute_product = self.chosenproduct
        else:
            self.substitute_product = self.choices[int(self.super_input(range(1, len(self.substitute_list)+1)))]
        print("Vous avez choisi " + self.substitute_product['name'])
        print("Description : " + self.substitute_product['description'])
        print("URL : " + self.substitute_product['url'])
        print("NutriScore : " + self.substitute_product['score'])
        print("Catégorie : " +  self.dataPB.find_from_table(self.substitute_product['category_id'], "id", "category", 1)['name'])
        print("Où acheter : " + self.substitute_product['store'])

    def add_data_choice(self):
        id1 = str(self.dataPB.find_from_table(self.chosenproduct['id'], "id", "product", 1)['id'])
        id2 = str(self.dataPB.find_from_table(self.substitute_product['id'], "id", "product", 1)['id'])
        self.dataPB.insert_substitute(id1, id2)
        

class Saved_Data():
    """ """
    def __init__(self):
     pass






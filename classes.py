import requests
import mysql
import pymysql
import pymysql.cursors

from constants import *
from privite import *

connection = pymysql.connect(host=HOST,
                                user=USER,
                                password=PASSWORD,
                                db=DB,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

class DataOFF():
    """Class defines the data which we want to get from Open Food Facts using the library request"""
    def __init__(self):
        self.categories = LIST_CATEGORIES      
        
    def get_data(self):
        """Method which get the necessary information in certain categories"""
        all_products = []
        self.catnumber = 1
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
                            product["category"] = self.catnumber
                            product["score"] = r.json()["products"][i]["nutrition_grade_fr"]   
                            all_products.append(product)
                    except (TypeError):
                        print ("TypeError!")
                    except (KeyError):
                        print ("That key does not exist!")
                    i += 1
            self.catnumber += 1
        self.products = all_products  
        #print(self.products)
        return(self.products)
            

#data_off = DataOFF()
#data_off.get_data()


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

    def insert_category(self):
        """Method which creates new records and commits the changes in the table category"""
        for category in LIST_CATEGORIES:
            with self.connection.cursor() as cursor:
                sql_data = "INSERT INTO `category` (`name`) VALUES (%s)"
                cursor.execute(sql_data, category)

    def insert_product(self):
        """Method which creates new records and commits the changes in the table Product"""
        for prod in self.data_off.get_data():
            #self.catid = int()
            with self.connection.cursor() as cursor:
                #insert into `product`
                sql = "INSERT INTO `product` (`name`, `description`, `url`, `score`, `category_id`) VALUES (%s, %s, %s, %s, %s)"
                try:
                    cursor.execute(sql, (prod['name'], prod['description'], prod['url'], prod['score'], prod['category'])) 
                except:
                    print("error")
            #print(prod)
    
    def insert_substitute(self):
        """Method which creates new records and commits the changes in the table Substitute"""
        pass

    def commit_connection(self):
        """Method which commit the changes"""
        self.connection.commit()
            
    def close_connection(self):
        """Method which closes the connection"""
        self.connection.close()

    def clean(self, whattable):
        with self.connection.cursor() as cursor:
            sqlclean = "DELETE FROM " + whattable
            cursor.execute(sqlclean)
            sqlreset = "ALTER TABLE " + whattable + " AUTO_INCREMENT = 1"
            cursor.execute(sqlreset)

    def find_from_table(self, search, colum, table):
        self.connect_db()
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM `" + table + "` WHERE `" + colum + "`=%s"
            cursor.execute(sql, (search))
            return cursor.fetchone()
        self.close_connection()
    
"""
data_pb = DataPB()
data_pb.connect_db()
data_pb.clean("product")
data_pb.clean("category")
data_pb.insert_category()
data_pb.commit_connection()
data_pb.insert_product()
data_pb.commit_connection()
data_pb.close_connection()
"""

class Display_data():
    """Claass defines the data """
    def __init__(self):
        self.nutridict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}
        self.substitute_list = []
        self.result = None
        self.dataPB = DataPB()

    def nutricompare(self, score1, score2):
        if self.nutridict[score1] < self.nutridict[score2]:
            return True
        else: 
            return False

    def super_input(self, acsepted_inputs):
        while True:
            theinput = input()
            for input1 in acsepted_inputs:
                if str(input1) == theinput:
                    return theinput
            print("Maovais, Retapez s'il vous plait") 

    def choose_option(self):
        print("Choisissez l'option and entrez le chiffre correspondant: 1 - Quel aliment souhaitez-vous remplacer ? 2 - Retrouver mes aliments substitués.")
        self.choice = self.super_input(['1','2'])
        if self.choice == "1":
            print("Sélectionnez la catégorie:")
            b = 1
            for category in LIST_CATEGORIES:
                print(str(b) + " : " + category)
                b += 1
            self.choicecat = int(self.super_input(range(1, len(LIST_CATEGORIES)+1)))
            with connection.cursor() as cursor:
                sql = "SELECT `name`, `description`, `url`, `score`, `category_id` FROM `product` WHERE `category_id`=%s"
                cursor.execute(sql, (self.choicecat))
                self.result = cursor.fetchall()
                #print(self.result)
            print("")
            print("Sélectionnez le produit que vous voulez remplacer.")
            b = 1
            self.choices = {}
            for product in self.result:
                self.choices[b] = product
                print(str(b) + " : " + product['name'])
                b += 1
            self.chosenproduct = self.choices[int(self.super_input(range(1, len(self.choices)+1)))]

    
    def findsubstutute(self):

        #print(self.chosenproduct['score'])

        for product in self.result:
            #print(product['score'])
            if self.nutricompare(product['score'], self.chosenproduct['score']):
                self.substitute_list.append(product)
        print('')
        print("Choisissez votre substitué:")
        b = 1
        self.choices = {}
        for product in self.substitute_list:
            self.choices[b] = product
            print(str(b) + " : " + product['name'] + ", " + product['score'])
            b +=1
        self.substitute_product = self.choices[int(self.super_input(range(1, len(self.substitute_list)+1)))]
        print("Your final substitute is: " + self.substitute_product['name'])
        print("Description: " + self.substitute_product['description'])
        print("URL: " + self.substitute_product['url'])
        print("NutriScore: " + self.substitute_product['score'])
        print("Category: " +  self.dataPB.find_from_table(self.substitute_product['category_id'], "id", "category")['name'])

        """with connection.cursor() as cursor:
            sql = "SELECT `name` FROM `category` WHERE `id`=%s"
            cursor.execute(sql, (self.substitute_product['category_id']))
            print("Category: " + cursor.fetchone()['name'])"""




displaydata = Display_data()
displaydata.choose_option()
displaydata.findsubstutute()
        

connection.commit()
connection.close()
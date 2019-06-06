import requests
import mysql
import pymysql
import pymysql.cursors

from constants import *

class DataOFF():
    """Class defines the data which we want to get from Open Food Facts using the library request"""
    def __init__(self):
        self.categories = LIST_CATEGORIES      
        
    def get_data(self):
        """Method which get the necessary information in certain categories"""
        cat_products = []
        all_products = []
        for category in self.categories:
            p = {"search_terms":category,"json":1, "page_size":100}
            r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl", params = p)
            i = 0
            for i in range(100):
                if i < NUM_PRODUCTS:
                    product = {"name": "", "description": "", "url": "", "score": "", "category": "", 
                                "store": ""}
                    if (len(r.json()["products"][i]["product_name_fr"]) > 2 and
                        len(r.json()["products"][i]["generic_name_fr"]) > 2 and
                        len(r.json()["products"][i]["url"]) > 2 and 
                        len(r.json()["products"][i]["nutrition_grade_fr"]) >= 1 and 
                        len(r.json()["products"][i]["stores"]) > 2):
                        product["name"] = r.json()["products"][i]["product_name_fr"]
                        product["description"] = r.json()["products"][i]["generic_name_fr"]
                        product["url"] = r.json()["products"][i]["url"]
                        product["store"] = r.json()['products'][i]['stores']
                        product["category"] = category
                        product["score"] = r.json()["products"][i]["nutrition_grade_fr"]   
                        cat_products.append(product)
                    i += 1
        all_products.append(cat_products)
        self.products = all_products  
        #print(self.products)
        return(self.products)
            

data_off = DataOFF()
data_off.get_data()


class DataPB():
    """Claass defines the data which fills the database Pur Beurre """
    def __init__(self):
        self.data_off = DataOFF()

    def connect_db(self): 
        """Method which creates la connection with the database Pur Beurre"""       
        self.connection = pymysql.connect(host='localhost',
                                user='olena',
                                password='Nazarchik1',
                                db='projet5',
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
        for lst in self.data_off.get_data():
            for prod in lst:
                number = 1
                while number < len(LIST_CATEGORIES):
                    with self.connection.cursor() as cursor:
                        # Read a single record
                        sqlsearch = "SELECT `name` FROM `category` WHERE `id`=%s"
                        cursor.execute(sqlsearch, (number))
                        if cursor.fetchone() == prod['category']:
                            self.result = number
                        #print(self.result)
                    number = number + 1
                with self.connection.cursor() as cursor:
                    sql = "INSERT INTO `product` (`name`, `description`, `url`, `score`, `category_id`) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (prod['name'], prod['description'], prod['url'], prod['score'], 1)) #"""self.result['id']"""
                #print(prod)

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
    

data_pb = DataPB()
data_pb.connect_db()
data_pb.clean("product")
data_pb.clean("category")
data_pb.insert_category()
data_pb.insert_product()
data_pb.commit_connection()
data_pb.close_connection()
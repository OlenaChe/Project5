#!/usr/bin/python3
# -*- coding: Utf-8 -*

from classes import DataOFF, DataPB, Display_data, Saved_data

data_off = DataOFF()
data_pb = DataPB()
displaydata = Display_data()
saved_data = Saved_data()

data_off.get_data()

data_pb.clean("substitute")
data_pb.clean("product")
data_pb.clean("category")
data_pb.insert_category()
data_pb.insert_product()

displaydata.session = True
while displaydata.session:
    print("")
    print("Choisissez l'option et entrez le chiffre correspondant: 1 - Quel aliment souhaitez-vous remplacer ? 2 - Retrouver mes aliments substitués. Q - Quitter")
    print("")
    choice = displaydata.super_input(['1', '2', 'Q'])
    print("")
    if choice == "1":
        print("")
        displaydata.choose_option()
        displaydata.findsubstutute()
        displaydata.add_data_choice()
    elif choice == "2":
        print("")
        print("VOILÀ VOTRE LISTE DES PRODUITS SAINS :")
        displaydata.saved_data.display_result(displaydata.dataPB.sql("SELECT DISTINCT product.name as produit, product.description, product.score as n_s, product.url, product.store as magasins FROM product INNER JOIN substitute ON product.id = substitute.healthy_product_id", "all"))
    elif choice == "Q":
        displaydata.session = False
    
    



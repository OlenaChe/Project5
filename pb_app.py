#!/usr/bin/python3
# -*- coding: Utf-8 -*

from classes import Data_OFF, Data_PB, Display_data, Saved_data

data_off = Data_OFF()
data_pb = Data_PB()
display_data = Display_data()
saved_data = Saved_data()

print("")
print("Bonjour!")
print("Si vous utilisez l'application 'Pur Beurre' pour la première fois, \
tapez '0' ")
print("Sinon, tapez '1'")
print("")

if display_data.super_input(['0', '1']) == '0':
    print("Attendez quelques instants, s'il vous plaît ")
    data_off.get_data()
    # print("Get data over")
    data_pb.connect()
    data_pb.drop_db()
    data_pb.create_db()
    data_pb.create_category()
    data_pb.create_product()
    data_pb.create_substitute()
    # data_pb.clean("substitute")
    # print("clean substitute over")
    # data_pb.clean("product")
    # print("clean product over")
    # data_pb.clean("category")
    # print("clean category over")
    data_pb.insert_category()
    # print("insert category over")
    data_pb.insert_product()
    # print("insert product over")

display_data.session = True
while display_data.session:
    print("")
    print("Choisissez l'option et entrez le chiffre correspondant :")
    print("1 - Quel aliment souhaitez-vous remplacer ?")
    print("2 - Retrouver mes aliments substitués")
    print("Q - Quitter")
    print("")
    choice = display_data.super_input(['1', '2', 'Q'])
    print("")
    if choice == "1":
        print("")
        display_data.choose_option()
        display_data.find_substutute()
        display_data.add_data_choice()
    elif choice == "2":
        print("")
        print("VOILÀ VOTRE LISTE DES PRODUITS SAINS :")
        display_data.saved_data.display_result(display_data.data_pb.sql(
         "SELECT DISTINCT\
          product.name as produit,\
          product.description,\
          product.score as n_s,\
          product.url,\
          product.store as magasins\
          FROM product INNER JOIN substitute\
          ON product.id=substitute.healthy_product_id", "all"))
    elif choice == "Q":
        display_data.session = False
            
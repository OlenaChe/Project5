#!/usr/bin/python3
# -*- coding: Utf-8 -*

from classes import DataOFF, DataPB, Display_data

data_off = DataOFF()
data_off.get_data()

data_pb = DataPB()
data_pb.clean("substitute")
data_pb.clean("product")
data_pb.clean("category")
data_pb.insert_category()
data_pb.insert_product()

displaydata = Display_data()
displaydata.choose_option()
displaydata.findsubstutute()
displaydata.add_data_choice()


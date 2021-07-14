#
# solution_DAO.py
# src
#
# Created by Javier Contreras el 13/03/2021
# Escuela Técnica Superior de Ingenieros de Telecomunicación
# Universidad Politécnica de Madrid
# 

from pymongo import MongoClient
import pymongo
import numpy as np
import pickle
from src.VRP.dao.db_connection import get_all_locations_dst
from datetime import date

today = date.today()

current_date = today.strftime("%d/%m/%y")


def get_data(name):
    global current_date
    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    shipping_collection = VRP_db[current_date+'-Shipping']

    shipment = shipping_collection.find(
        {
            'data.name': name
        }
    )

    client.close()
    return shipment[0]['data']

def get_solution(name):
    global current_date

    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    shipping_collection = VRP_db[current_date+'-Shipping']

    try:
        shipment = shipping_collection.find(
            {
                'data.name': name
            }
        )

        client.close()
        return shipment[0]['solution']
    except Exception as e:
        print(str(e))

def set_result_table_content(result_table_content, name):
    global current_date

    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    shipping_collection = VRP_db[current_date+'-Shipping']

    try:
        shipping_collection.update_one(
            {
                'data.name': name
            },
            {
                '$set': {
                    'solution.result_table_content': result_table_content,

                }
            }
        )

        client.close()
    except Exception as e:
        print("Error al guardar tabla de resultados en la base de datos")
        print(str(e))

def set_solution(routes_array, name):
    global current_date

    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    shipping_collection = VRP_db[current_date+'-Shipping']

    try:
        shipping_collection.update_one(
            {
                'data.name': name
            },
            {
                '$set': {
                    'solution.routes': routes_array,

                }
            }
        )

        client.close()
    except Exception as e:
        print("Error al guardar rutas en la base de datos")
        print(str(e))


def set_parameters(shipment, name):
    global current_date

    print("""Imprimiendo datos que se enviarán al solver:
        Locations_DST: """ + str(shipment['data']['locations_dst_address'])+"""
        Locations_DEPOT: """ + str(shipment['data']['locations_depot_address'])+ """
        Demands: """ + str(shipment['data']['demands']) + """
        Vehicles_capacities: """ + str(shipment['data']['vehicle_capacities']) + """
        Distance_Matrix: """ + str(shipment['data']['distance_matrix']) + """
        Duration_Matrix: """ + str(shipment['data']['duration_matrix']) + """
        Num_Vehicles: """ + str(shipment['data']['num_vehicles']) + """
        Vehicles: """ + str(shipment['data']['vehicles']) + """
        Deliver_To: """ + str(shipment['data']['deliver_to']) + """
        Time_Window: """ + str(shipment['data']['time_window']) + """
        Name: """ + name)

    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    shipping_collection = VRP_db[current_date+'-Shipping']
    with open('pickle/distance_matrix_for_shipping.pickle', 'wb') as file:
        pickle.dump(shipment['data']['distance_matrix'], file)
    with open('pickle/duration_matrix_for_shipping.pickle', 'wb') as file:
        pickle.dump(shipment['data']['duration_matrix'], file)
    save_parameters(shipping_collection, shipment, name)

def save_parameters(shipping_collection, shipment, name):
    shipping_collection.update_one(
        {
            'data.name': name
        },
        {
            '$set':{
                'data.locations_depot_address': shipment['data']['locations_depot_address'],
                'data.locations_dst_address': shipment['data']['locations_dst_address'],
                'data.demands': shipment['data']['demands'],
                'data.vehicle_capacities': shipment['data']['vehicle_capacities'],
                'data.coordinates_dst': shipment['data']['coordinates_dst'],

                'data.num_vehicles': shipment['data']['num_vehicles'],
                'data.vehicles': shipment['data']['vehicles'],
                'data.deliver_to': shipment['data']['deliver_to'],
                'data.time_window': shipment['data']['time_window'],
                }
        })  

def format_solution(name):
    global current_date

    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    shipping_collection = VRP_db[current_date+'-Shipping']

    try:
        shipment = shipping_collection.find(
            {
                'data.name': name
            }
        )

        client.close()
    except Exception as e:
        print(str(e))
        return

    locations = [ location for location in shipment[0]['data']['locations_dst_address']]

    coordinates = [ location for location in shipment[0]['data']['locations_dst_address']]


    vehicles = shipment[0]['data']['vehicles']
    table = []
    for i in range(0, len(vehicles)):
        locations_for_each_vehicle = []

        for location_id in shipment[0]['solution']['routes'][i]:
            if location_id != 0:
                locations_for_each_vehicle.append(locations[location_id-1])
                #location_id = location_id -1
            else:
                continue
            #locations_for_each_vehicle.append(locations[location_id])
        table.append(locations_for_each_vehicle)
    return table

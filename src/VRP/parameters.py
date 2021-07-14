#
# parameters.py
# src
#
# Created by Javier Contreras el 13/03/2021
# Escuela Técnica Superior de Ingenieros de Telecomunicación
# Universidad Politécnica de Madrid
# 

import pymongo
import pandas as pd
import datetime
import time
import numpy as np
import json
import urllib
import requests
from pymongo import MongoClient
from src.VRP.dao.db_connection import get_all_locations_dst
from src.VRP.dao.db_connection import get_all_locations_depot



current_date = datetime.datetime.now().date().strftime("%d/%m/%Y")  # Formato: 01/12/2020


def local_duration_matrix(places_found_depot, places_found_dst):
    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    matrix_collection = VRP_db['Distance_Duration_Matrix']
    try:

        matrix_dst = matrix_collection.find(
            {
                'matrix_dst.name': "distance-duration-matrix"
            }
        )
    except Exception as e:
        print(str(e))
        return
    try:

        matrix_depot = matrix_collection.find(
            {
                'matrix_depot.name': "distance-duration-matrix-depot"
            }
        )
    except Exception as e:
        print(str(e))
        return
    df_dst = np.array(matrix_dst[0]['matrix_dst']['duration'])
    indexes_for_cost_matrix_to_remove_dst,indexes_for_cost_matrix_dst = get_locations_indexes_dst(places_found_dst)
    duration_matrix = np.delete(df_dst , indexes_for_cost_matrix_to_remove_dst, axis=1)
    duration_matrix = np.delete(duration_matrix, indexes_for_cost_matrix_to_remove_dst, axis=0)

    df_depot = np.array(matrix_depot[0]['matrix_depot']['duration'])
    duration_matrix = merge_dst_depot_matrix(indexes_for_cost_matrix_dst,duration_matrix,df_depot)
    return duration_matrix





def local_distance_matrix(places_found_depot, places_found_dst):
    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    matrix_collection = VRP_db['Distance_Duration_Matrix']
    try:

        matrix_dst = matrix_collection.find(
            {
                'matrix_dst.name': "distance-duration-matrix"
            }
        )
    except Exception as e:
        print(str(e))
        return
    try:

        matrix_depot = matrix_collection.find(
            {
                'matrix_depot.name': "distance-duration-matrix-depot"
            }
        )
    except Exception as e:
        print(str(e))
        return
    df_dst = np.array(matrix_dst[0]['matrix_dst']['distance'])
    indexes_for_cost_matrix_to_remove_dst,indexes_for_cost_matrix_dst = get_locations_indexes_dst(places_found_dst)
    distance_matrix = np.delete(df_dst , indexes_for_cost_matrix_to_remove_dst, axis=1)
    distance_matrix = np.delete(distance_matrix, indexes_for_cost_matrix_to_remove_dst, axis=0)

    df_depot = np.array(matrix_depot[0]['matrix_depot']['distance'])
    distance_matrix = merge_dst_depot_matrix(indexes_for_cost_matrix_dst,distance_matrix,df_depot)
    return distance_matrix


def merge_dst_depot_matrix(indexes_for_cost_matrix_dst,distance_matrix, df_depot):
    #for i_depot in indexes_for_cost_matrix_depot:
    row = [0]
    col = []
    for i_dst in indexes_for_cost_matrix_dst:
        row.append(df_depot[0][i_dst])
        col.append(df_depot[1][i_dst])
    distance_matrix = np.c_[col,distance_matrix]
    distance_matrix = np.append([row], distance_matrix, axis=0)
    return distance_matrix


def get_locations_indexes_depot(locations_depot):
    all_locations_depot = get_all_locations_dst()
    index = 0
    index_depot = []
    indexes_for_cost_matrix = []
    for location in locations_depot:
        index = 0
        for location_found in all_locations_depot:
            if location_found['address'] == location:
                indexes_for_cost_matrix.append(index)
                break
            index += 1
    return indexes_for_cost_matrix
    

def get_locations_indexes_dst(locations_dst):
    all_locations_dst = get_all_locations_dst()
    index = 0
    index_depot = []
    indexes_for_cost_matrix_to_remove = [i for i in range(0,len(all_locations_dst))]
    indexes_for_cost_matrix = []
    for location in locations_dst:
        index = 0
        for location_found in all_locations_dst:
            if location_found['address'] == location:
                indexes_for_cost_matrix_to_remove.remove(index)
                indexes_for_cost_matrix.append(index)

                break
            index += 1

    return indexes_for_cost_matrix_to_remove, indexes_for_cost_matrix

def update_duration_matrix(shipment, index):
    duration_matrix = shipment['data']['duration_matrix']
    column = duration_matrix[:,index]
    row = duration_matrix[index]
    row = np.append(row, 0)
    duration_matrix = np.c_[duration_matrix,column]
    duration_matrix = np.append(duration_matrix, [row], axis=0)

    shipment['data']['duration_matrix'] = duration_matrix

    return shipment

def update_distance_matrix(shipment, index):

    distance_matrix = shipment['data']['distance_matrix']
    column = distance_matrix[:,index]
    row = distance_matrix[index]
    row = np.append(row, 0)
    distance_matrix = np.c_[distance_matrix,column]
    distance_matrix = np.append(distance_matrix, [row], axis=0)

   
    shipment['data']['distance_matrix'] = distance_matrix

    return shipment

def append_location(shipment, index, new_demand):
    while(shipment['data']['demands'][index] > 5):
        shipment['data']['locations_dst_address'].append(shipment['data']['locations_dst_address'][index-1])
        shipment['data']['locations_dst_names'].append(shipment['data']['locations_dst_names'][index-1])
        shipment['data']['time_window'].append(shipment['data']['time_window'][index])
        shipment['data']['coordinates_dst'].append(shipment['data']['coordinates_dst'][index-1])
        shipment['data']['demands'][index] = shipment['data']['demands'][index] - new_demand
        shipment['data']['demands'].append(new_demand)
        shipment = update_duration_matrix(shipment, index)
        shipment = update_distance_matrix(shipment, index)
    return shipment


def check_split_delivery(shipment):
    vehicle_capacities = [vehicle['capacity'] for vehicle in shipment['data']['vehicles']]
    sum_vehicle_capacities = sum(vehicle_capacities)
    
    index_of_demand = 0
    for demand in shipment['data']['demands']:
        if demand < sum_vehicle_capacities and demand > max(vehicle_capacities):
            shipment = append_location(shipment, index_of_demand, 5)
        index_of_demand += 1 
    
    index_of_demand = 0
    count_demand = 0
    for demand in shipment['data']['demands']:
        if demand > 5 and demand < 8:
            count_demand += 1
        if count_demand > 5:
               append_location(shipment, index_of_demand, 4) 
               count_demand -= 1
        index_of_demand += 1

    return shipment


def format_time(time_in_seconds):
    return time.strftime("%H:%M",time.gmtime(time_in_seconds))


def check_parameters(data):
    vehicle_capacities = [vehicle['capacity'] for vehicle in data['data']['vehicles']]
    sum_vehicle_capacities = sum(vehicle_capacities)
    sum_demands = sum(data['data']['demands'])
    number_of_demands = len(data['data']['demands'])
    number_of_locations_dst = len(data['data']['locations_dst_address'])
    number_of_locations_depot = len(data['data']['locations_depot_address'])
    number_of_vehicle_capacities = len(data['data']['vehicles'])
    number_of_vehicles = data['data']['num_vehicles']
    start_time = 8*3600  
    truck_end_time = 22*3600-start_time 
    index_of_dst = 0
    depot = 0

    if number_of_vehicles <= 0:
        return False, "No vehicles selected"

    if number_of_locations_depot <= 0:
        return False, "No depot selected"

    if number_of_locations_dst <= 0:
        return False, "No destinations selected"

    for time_window in data['data']['time_window']:
        if time_window[1] > truck_end_time:
            time = format_time(time_window[1] + start_time)
            return False, "Max time window: " + time + ". Wrong for: " + str(data['data']['locations_dst_address'][index_of_dst-1])
        trip_time = data['data']['duration_matrix'][depot][index_of_dst]
        max_time_window = time_window[1]

        if (trip_time > max_time_window):
            return False, "Wrong time window for: " + str(data['data']['locations_dst_address'][index_of_dst-1])
        index_of_dst += 1
   

    if sum_vehicle_capacities < sum_demands:
        return False, "Impossible solution, too much demand requested."
     
    return True, "No error"


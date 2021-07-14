#
# db_connection.py
# src
#
# Created by Javier Contreras el 13/03/2021
# Escuela Técnica Superior de Ingenieros de Telecomunicación
# Universidad Politécnica de Madrid
# 

from pymongo import MongoClient
import pymongo
import json
import pickle
from datetime import date

today = date.today()

current_date = today.strftime("%d/%m/%y")



def reset_db():
    data = json.load(open('src/json/destinations.json', 'r'))

    client = MongoClient('localhost', 27017)
    client.drop_database('VRP_db')

    VRP_db = client['VRP_db']
    VRP_db.drop_collection('Locations_Depot')
    VRP_db.drop_collection('Distance_Duration_Matrix')

    VRP_db.drop_collection('Locations_Dst')

    locations_collection = VRP_db['Locations_Dst']
    
    for location in data:
        try:
            locations_collection.insert_one({
                'location_dst': {
                    "id": location["id"],
                    "name": location['name'],
                    "province": location['province'],
                    "address": location['address'],
                    "coordinates": location['coordinates'],
                    "capacity": location['capacity'],
                    "deliver_to": location['deliver_to'], 
                    "from_time": location['from_time'],        
                    "to_time": location['to_time'],
                    "use": 'false',
                    "type": "dst"
                } 
            })
        except Exeption as e:
            print(str(e))
 
    location_dst = locations_collection.find(
        { 
            'location_dst.address': "CARRERA, S/N 18330 CHAUCHINA"
        }  
    )
    with open('pickle/distance_matrix.pickle', 'rb') as file:
        distance_matrix = pickle.load(file)
    with open('pickle/durations_matrix.pickle', 'rb') as file:
        durations_matrix = pickle.load(file)
    matrix_collection = VRP_db['Distance_Duration_Matrix']

    matrix_collection.insert_one({
        'matrix_dst': {
            "name": "distance-duration-matrix",
            "distance": distance_matrix,
            "duration": durations_matrix
            } 
    })
    with open('pickle/distance_matrix_depot.pickle', 'rb') as file:
        distance_matrix = pickle.load(file)
    with open('pickle/durations_matrix_depot.pickle', 'rb') as file:
        durations_matrix = pickle.load(file)
    matrix_collection = VRP_db['Distance_Duration_Matrix']
    matrix_collection.insert_one({
        'matrix_depot': {
            "name": "distance-duration-matrix-depot",
            "distance": distance_matrix,
            "duration": durations_matrix
            } 
    })
    data = json.load(open('src/json/depot.json', 'r'))

    VRP_db = client['VRP_db']
    locations_collection = VRP_db['Locations_Depot']

    for location in data:
        locations_collection.insert_one({
        'location_depot': {
            "name": location['name'],
            "province": location['province'],
            "address": location['address'],
            "coordinates": location['coordinates'],
            "use": location['use'],
            "type": "depot"

            } 
    })


    location_depot = locations_collection.find(
        { 
            'location_depot.address': "CINCA 44, BARCELONA 08223 TERRASSA"
        }  
    )
    data = json.load(open('src/json/vehicles.json', 'r'))

    VRP_db = client['VRP_db']
    vehicles_collection = VRP_db['Vehicles']

    for vehicle in data['vehicles']:
        vehicles_collection.insert_one({
        'vehicle': {
            "registration": vehicle['registration'],
            "capacity": vehicle['capacity'],
            "use": vehicle['use'],

            } 
    })


    vehicle = vehicles_collection.find(
        { 
            'vehicle.registration': "2425 AHJ"
        }  
    )
    
def get_location_by_name(name):
    global current_date
    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    shipping_collection = VRP_db[current_date+'-Shipping']
    locations = shipping_collection.find({ 'data.name': name})
    locations_dst = []
    try:
        for location in locations:
            locations_dst.append({         
                        "address": location['data']['locations_dst'],
                        "capacity": location['data']['demands'],
                        "coordinates": location['data']['coordinates'],
                        "deliver_to": location['data']['deliver_to'],
                        "time_window": location['data']['time_window'],
                        

                        })
    
    except Exception as e:
        print(str(e))
    
    return locations_dst

def get_location_by_province(province):
    global current_date
    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    shipping_collection = VRP_db["Locations_Dst"]
    locations = shipping_collection.find({ 'location_dst.province': province})
    locations_dst = []
    try:
        for location in locations:
            #if location['data']['province']
            print(location)
            locations_dst.append({  
                        "name": location['location_dst']['name'],
                        "id": location['location_dst']["id"],
                        "address": location['location_dst']['address'],
                        "province": location['location_dst']['province'],
                        "capacity": location['location_dst']['capacity'],
                        "coordinates": location['location_dst']['coordinates'],
                        "deliver_to": location['location_dst']['deliver_to'],
                        "from_time": location['location_dst']['from_time'],
                        "to_time": location['location_dst']['to_time']

                        

                        })
    
    except Exception as e:
        print("dkfjg")
        print(str(e))
    
    return locations_dst

def get_location_depot_by_name(name):
    global current_date
    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    shipping_collection = VRP_db[current_date+'-Shipping']
    locations = shipping_collection.find({ 'data.name': name})
    locations_depot = []
    try:
        for location in locations:
            locations_dst.append({         
                        "address": location[0]['data']['locations_depot'],
                        })
    
    except Exception as e:
        print(str(e))
    return locations_depot

def update_location_by_name(name):
    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    locations_collection = VRP_db['Locations']
    locations = locations_collection.find({ 'location_dst.type': "dst", 'location_dst.name': name})

    locations_dst = []
    for location in locations:
        try:
            locations_dst.append({          
                "address": location['location_dst']['address'],
                "capacity": location['location_dst']['capacity'],
                "deliver_to": location['location_dst']['deliver_to'],
                "from_time": location['location_dst']['from_time'],
                "to_time": location['location_dst']['to_time'],
                "use": location['location_dst']['use']

                })
        except:
            return    

    return locations_dst

def get_all_locations_dst():
    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    locations_collection = VRP_db['Locations_Dst']
    locations = locations_collection.find({ 'location_dst.type': "dst"})

    locations_dst = []
    for location in locations:
        try:
            locations_dst.append({
                "id": location['location_dst']["id"],
                "name": location['location_dst']['name'],
                "province": location['location_dst']['province'],        
                "address": location['location_dst']['address'],
                "coordinates": location['location_dst']['coordinates'],
                "capacity": location['location_dst']['capacity'],
                "deliver_to": location['location_dst']['deliver_to'],
                "from_time": location['location_dst']['from_time'],
                "to_time": location['location_dst']['to_time'],
                "use": location['location_dst']['use']

                })
        except:
            print("ERROR")
            continue
    

    return locations_dst

def get_all_locations_depot():
    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    locations_collection = VRP_db['Locations_Depot']
    locations = locations_collection.find({'location_depot.type': "depot"})
    locations_depot = []
    for location in locations:
        locations_depot.append({          
            "name": location['location_depot']['name'],
            "province": location['location_depot']['province'],        
            "address": location['location_depot']['address'],
            "coordinates": location['location_depot']['coordinates'],
            "use": location['location_depot']['use']

            })

    return locations_depot

def get_all_vehicles():
    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    vehicle_collection = VRP_db['Vehicles']
    vehicles = vehicle_collection.find({})
    all_vehicles = []
    for vehicle in vehicles:
        all_vehicles.append({          
            "registration": vehicle['vehicle']['registration'],
            "capacity": vehicle['vehicle']['capacity'],
            "use": vehicle['vehicle']['use']

            })

    return all_vehicles



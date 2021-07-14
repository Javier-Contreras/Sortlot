#
# shipment_DAO.py
# src
#
# Created by Javier Contreras el 13/03/2021
# Escuela Técnica Superior de Ingenieros de Telecomunicación
# Universidad Politécnica de Madrid
# 

from pymongo import MongoClient
import pymongo

from src.VRP.dao.db_connection import get_location_by_name
from datetime import date

today = date.today()

current_date = today.strftime("%d/%m/%y")

client = MongoClient('localhost', 27017)
VRP_db = client['VRP_db']
shipping_collection = VRP_db[current_date+'-Shipping']

locations_dst_address = []
locations_dst_names = []
locations_dst_provinces = []
demands = [0]
deliver_to = []
coordinates = []
start_time = 8*3600  
end_time = 22*3600-start_time # Horario de 08:00 a 18:00  
time_window = [[0,end_time]] 

locations_depot_names = []
locations_depot_address = []
locations_depot_provinces = []

vehicles = []



def add_dst_to_shipping(location):
    global locations_dst_address, locations_dst_names, locations_dst_provinces, coordinates
    
    locations_dst_names.append(location['name'])
    locations_dst_address.append(location['address'])
    locations_dst_provinces.append(location['province'])
    coordinates.append(location['coordinates'])


def add_demand_to_shipping(location):
    global demands
    
    demands.append(int(location['capacity']))


def add_tw_to_shipping(location, index):
    global time_window, start_time, end_time
    
    total_seconds_from_time = sum(x * int(t) for x, t in zip([3600, 60], location['from_time'].split(":")))-start_time
    total_seconds_to_time = sum(x * int(t) for x, t in zip([3600, 60], location['to_time'].split(":")))-start_time
    time_window[index] = [total_seconds_from_time, total_seconds_to_time]


def add_pickup_delivery_to_shipping(location, data, index):
    global deliver_to
    
    deliver_to.append([index, data[int(location['deliver_to'])]['address']])


def format_pickup_deliveries():
    global deliver_to, locations_dst_address
    
    for deliver in deliver_to:
        deliver[1] = locations_dst_address.index(deliver[1])+1


def set_locations_dst_shipping(data, name):
    global locations_dst_address, locations_dst_names,locations_dst_provinces,demands, coordinates, deliver_to, time_window, start_time, end_time
    reset_variables()
    index = 1
    for location in data:
        if (location['use'] and not isinstance(location['use'], str)):
            time_window.append([0,end_time])
            add_dst_to_shipping(location)
            add_demand_to_shipping(location)
            try:
                add_pickup_delivery_to_shipping(location, data, index)
            except :
                pass
            try:    
                add_tw_to_shipping(location, index)
            except Exception as e:
                index +=1
                continue
            index +=1

    format_pickup_deliveries()
    save_data(name)
    

def save_data(name):
    if get_shipping_data(name) is None:
        insert_one_shipping(name)
    else:
        update_dst_one_shipping(name)


def update_dst_one_shipping(name):
    global shipping_collection, locations_dst_address, locations_dst_names,locations_dst_provinces,demands, coordinates, deliver_to, time_window
    
    shipping_collection.update_one(
        {
            'data.name': name
        },
        {
            '$set':{
                "data.locations_dst_address": locations_dst_address,
                "data.locations_dst_names": locations_dst_names,
                "data.locations_dst_provinces": locations_dst_provinces,
                "data.demands": demands,
                "data.coordinates_dst": coordinates,
                "data.deliver_to": deliver_to, 
                "data.time_window": time_window,
            }
        })    

def insert_one_shipping(name):
    global shipping_collection, locations_dst_address, locations_dst_names,locations_dst_provinces,demands, coordinates, deliver_to, time_window

    shipping_collection.insert_one({
            'data': {
                "name": name,
                "locations_dst_address": locations_dst_address,
                "locations_dst_names": locations_dst_names,
                "locations_dst_provinces": locations_dst_provinces,
                "demands": demands,
                "coordinates_dst": coordinates,
                "deliver_to": deliver_to, 
                "time_window": time_window
            } 
        })


def add_depot_to_shipping(location):
    global locations_depot_address, locations_depot_names, locations_depot_provinces, coordinates
    
    locations_depot_names.append(location['name'])
    locations_depot_provinces.append(location['province'])
    locations_depot_address.append(location['address'])
    coordinates.append(location['coordinates'])


def update_depot_one_shipping( name):
    global shipping_collection, locations_depot_address, locations_depot_names, locations_depot_provinces, coordinates
    
    shipping_collection.update_one(
        {
            'data.name': name
        },
        {
            '$set':{
                'data.locations_depot_address': locations_depot_address,
                "data.locations_depot_provinces": locations_depot_provinces,
                'data.locations_depot_names': locations_depot_names,
                'data.coordinates_depot': coordinates

            }
        })


def set_locations_depot_shipping(data, name):
    global coordinates
    coordinates = []

    for location in data:
        if (location['use']):
            add_depot_to_shipping(location)
            
    update_depot_one_shipping(name)
    

def update_vehicles_one_shipping(data, name):
    global vehicles, shipping_collection
    
    vehicle_capacities = [int(v['capacity']) for v in data if (v['use'])]
    shipping_collection.update_one(
        {
            'data.name': name
        },
        {
            '$set':{
                'data.vehicles': vehicles,
                'data.vehicle_capacities': vehicle_capacities,
                'data.num_vehicles': len(vehicles)
            }
        })


def add_vehicle_to_shipping(vehicle):
    global vehicles
    
    vehicles.append({
        "registration": vehicle['registration'], 
        "capacity": int(vehicle['capacity'])
    })


def set_vehicles_shipping(data, name):
    for vehicle in data:
        if (vehicle['use']):
            add_vehicle_to_shipping(vehicle)

    update_vehicles_one_shipping(data, name)


def get_shipping_data(name):
    global shipping_collection
       
    data = shipping_collection.find(
        { 
            'data.name': name
        }  
    )
    try: 
        return data[0]
    except Exception as e:
        print("Error al coger los datos")
        print(str(e))
        return None

def reset_variables():
    global locations_dst_address, locations_dst_names,locations_dst_provinces,demands, coordinates, deliver_to, time_window, start_time, end_time, locations_depot_address, locations_depot_names, locations_depot_provinces, vehicles
    locations_dst_address = []
    locations_dst_names = []
    locations_dst_provinces = []
    demands = [0]
    deliver_to = []
    coordinates = []
    start_time = 8*3600  
    end_time = 22*3600-start_time # Horario de 08:00 a 18:00  
    time_window = [[0,end_time]] 

    locations_depot_names = []
    locations_depot_address = []
    locations_depot_provinces = []

    vehicles = []

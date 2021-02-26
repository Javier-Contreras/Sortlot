import gmaps
import googlemaps
import pymongo
import pandas as pd
import datetime
import time
import numpy as np
import json
import urllib
import requests
from ..constants import API_KEY
from pymongo import MongoClient


current_date = datetime.datetime.now().date().strftime("%d/%m/%Y")  # Formato: 01/12/2020


gmaps.configure(api_key=API_KEY)
gmaps_services = googlemaps.Client(key=API_KEY)


def format_parameters(data):
    data['num_vehicles'] = int(data['num_vehicles'])
    str1 = data['demands'].replace(']', '').replace('[', '')
    demands_formatted = str1.replace('"', '').split(",")
    for i in range(0, len(demands_formatted)):
        demands_formatted[i] = int(demands_formatted[i])
    data['demands'] = demands_formatted

    str1 = data['vehicle_capacities'].replace(']', '').replace('[', '')
    vehicle_capacities_formatted = str1.replace('"', '').split(",")
    for i in range(0, len(vehicle_capacities_formatted)):
        vehicle_capacities_formatted[i] = int(vehicle_capacities_formatted[i])
    data['vehicle_capacities'] = vehicle_capacities_formatted

    aux = []
    locations = data['locations_dst'].split("\n")
    if not len(locations) == 1:
        for location in locations:
            aux.append(location[:-1])
    else:
        aux = locations
    data['locations_dst'] = aux

    aux = []
    locations = data['locations_depot'].split("\n")

    if not len(locations) == 1:
        for location in locations:
            aux.append(location[:-1])
    else:
        aux = locations
    data['locations_depot'] = aux
    return data


# Obtener localizaciones
def get_locations(places):
    locations_found = []
    for i in places:
        result = gmaps_services.geocode(i)
        if len(result) > 0:
            result = result[0]
            place = {"label": i,
                     "location": (result["geometry"]["location"]["lat"], result["geometry"]["location"]["lng"])}
            locations_found.append(place)

    locations_found_array = []
    for location_found in locations_found:
        locations_found_array.append(
            {
                'label': location_found['label'],
                'location': (float(location_found['location'][0]),
                             float(location_found['location'][1])),
            })
    return locations_found_array


def get_distance_matrix(places_found_depot, places_found, current_date):
    client = MongoClient('localhost', 27017)
    VRP_db = client['VRP_db']
    CVRP_collection = VRP_db['CVRP']
    try:

        vrp = CVRP_collection.find(
            {
                'data.date': current_date
            }
        )
        distance_matrix = vrp[0]['data']['distance_matrix']
        print("Dentro del Try")
        print(distance_matrix)
        return distance_matrix
    except:
        print("Using Distance Matrix API")

        depot = places_found_depot[0]
        locations = [p["location"] for p in [depot] + places_found]

        max_elements = 100
        num_addresses = len(locations)

        def build_distance_matrix(response):
            distance_matrix_aux = []
            for row in response['rows']:
                try:
                    row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
                    distance_matrix_aux.append(row_list)
                except Exception as e:
                    print(str(e))
                    continue
            return distance_matrix_aux

        max_rows = max_elements // num_addresses
        # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
        q, r = divmod(num_addresses, max_rows)
        dest_addresses = locations
        distance_matrix = []
        # Send q requests, returning max_rows rows per request.
        for i in range(q):
            origin_addresses = locations[i * max_rows: (i + 1) * max_rows]
            response = gmaps_services.distance_matrix(origins=origin_addresses,
                                                      destinations=dest_addresses)  # , mode="transit", transit_mode="train")
            time.sleep(1)
            distance_matrix += build_distance_matrix(response)

        # Get the remaining remaining r rows, if necessary.
        if r > 0:
            origin_addresses = locations[q * max_rows: q * max_rows + r]
            response = gmaps_services.distance_matrix(origins=origin_addresses,
                                                      destinations=dest_addresses)  # , mode="transit", transit_mode="train")
            distance_matrix += build_distance_matrix(response)

        return distance_matrix

        df = pd.DataFrame(distance_matrix)
        df_norm = (df - df.min()) * 10000 / (df.max() - df.min())
        distance_matrix = df_norm.values
        # dataset = np.array(new_distance_matrix)
        return distance_matrix

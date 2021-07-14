#
# main.py
# src
#
# Created by Javier Contreras el 13/03/2021
# Escuela Técnica Superior de Ingenieros de Telecomunicación
# Universidad Politécnica de Madrid
# 

from src.VRP.dao.solution_DAO import set_parameters
from src.VRP.dao.solution_DAO import set_solution
from src.VRP.dao.solution_DAO import set_result_table_content
from src.VRP.dao.solution_DAO import get_data
from src.VRP.dao.solution_DAO import get_solution
from src.VRP.dao.solution_DAO import format_solution
from src.VRP.dao.shipment_DAO import get_shipping_data
from src.VRP.parameters import local_distance_matrix
from src.VRP.parameters import local_duration_matrix
from src.VRP.parameters import check_split_delivery



from src.VRP.parameters import check_parameters
from src.VRP.solver import solver_VRP


def main(name,json_locations_dst):

    shipment = get_shipping_data(name)
    
    shipment['data']['distance_matrix'] = local_distance_matrix(shipment['data']['locations_depot_address'], shipment['data']['locations_dst_address'])
    shipment['data']['duration_matrix'] = local_duration_matrix(shipment['data']['locations_depot_address'], shipment['data']['locations_dst_address'])
    
    possible_solution, error = check_parameters(shipment)
    if not possible_solution:
        print("Not possible solution")
        return error, json_locations_dst

    shipment = check_split_delivery(shipment)
    set_parameters(shipment, name)

    
    vehicle_capacities = shipment['data']['vehicle_capacities'] 
    shipment['data']['vehicle_capacities'] = []
    num_vehicles = shipment['data']['num_vehicles']
    routes_array = None
    result_table_content = None
    for vehicles in range(1, num_vehicles+1):
        shipment['data']['num_vehicles'] = vehicles
        print("Number of Vehicles: " + str(vehicles))
        shipment['data']['vehicle_capacities'].append(max(vehicle_capacities))
        vehicle_capacities.remove(max(vehicle_capacities))
        print("Vehicle Capacities:" + str(shipment['data']['vehicle_capacities']))
        
        if(sum(shipment['data']['vehicle_capacities'])) < sum(shipment['data']['demands']):
            continue

        try:
            routes_array, result_table_content = solver_VRP(shipment)
            print(routes_array)
            break
        except Exception as e:
            print(str(e))
            continue

    set_solution(routes_array, name)
    set_result_table_content(result_table_content,name)

    data = get_data(name)
    solution = get_solution(name)
    return solution, data

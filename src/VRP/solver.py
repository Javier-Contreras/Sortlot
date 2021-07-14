#
# solver.py
# src
#
# Created by Javier Contreras el 13/03/2021
# Escuela Técnica Superior de Ingenieros de Telecomunicación
# Universidad Politécnica de Madrid
# 

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pickle
import time


def print_solution(data, manager, routing, solution,shipment):
   
    table_content = []
    time_dimension = routing.GetDimensionOrDie('Time')
    for vehicle_id in range(shipment['data']['num_vehicles']):
        index = routing.Start(vehicle_id)
        start_location = shipment['data']['locations_depot_names'][manager.IndexToNode(index)]
        table_content.append({
                "vehicle": shipment['data']['vehicles'][vehicle_id]['registration'],
                "start": start_location,
                "route": "",
                "route_time": "",
                "route_distance": "",
                "route_load": ""
            })
        plan_output = ""
        route_distance = 0
        route_load = 0
        route_time = 0
        start_node = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            if node_index == start_node:
                location = shipment['data']['locations_depot_names'][manager.IndexToNode(index)-1]
            else:
                location = shipment['data']['locations_dst_names'][manager.IndexToNode(index)-1]
            dst_load = shipment['data']['demands'][node_index]
            route_load += shipment['data']['demands'][node_index]
            time_var = time_dimension.CumulVar(index)
            plan_output += ' {0} Load({1})'.format(location, dst_load) 

            if solution.Min(time_var) == solution.Max(time_var):                              #to_time)
                plan_output += ' Time({1}) -> '.format(manager.IndexToNode(index),
                    format_time(solution.Min(time_var),False))
            else:
                plan_output += ' Time({1},{2}) -> '.format(manager.IndexToNode(index), 
                    format_time(solution.Min(time_var),False),
                    format_time(solution.Max(time_var),False))

            previous_index = index

            index = solution.Value(routing.NextVar(index))
            route_distance += data['distance_matrix'][manager.IndexToNode(previous_index)][manager.IndexToNode(index)]#routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        route_distance += data['distance_matrix'][manager.IndexToNode(index)][manager.IndexToNode(start_node)]
        plan_output += ' {0} Load({1})'.format(start_location,
                                                 route_load)
        time_var = time_dimension.CumulVar(index)


        route_time += solution.Min(time_var)
        table_content[vehicle_id]["route_time"] = format_time(route_time,True)
        table_content[vehicle_id]["route_distance"] = int(route_distance/1000)
        table_content[vehicle_id]["route_load"] = route_load
        table_content[vehicle_id]["route"] = plan_output
    return table_content

def format_time(time_in_seconds, accumulative_time):
    if accumulative_time:
            return time.strftime("%H:%M",time.gmtime(time_in_seconds))

    truck_start_time = 8*3600 # Hora de salida de los camiones (offset)
    return time.strftime("%H:%M",time.gmtime(time_in_seconds+truck_start_time))
            
def extract_routes(num_vehicles, manager, routing, solution):
    routes = {}
    for vehicle_id in range(num_vehicles):
        routes[vehicle_id] = []
        index = routing.Start(vehicle_id)
        while not routing.IsEnd(index):
            routes[vehicle_id].append(manager.IndexToNode(index))
            previous_index = index
            index = solution.Value(routing.NextVar(index))
        routes[vehicle_id].append(manager.IndexToNode(index))
    return routes


##################################################

def generate_solution(data, manager, routing):  
    # FUNCION CALLBACK Y DIMENSION PARA DISTANCIAS
    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        # return data['distance_matrix'][from_node][to_node]
        return data['distance_matrix'][from_node][to_node]
        
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index) 
    # Add Distance constraint.
    dimension_name = 'Distance'
    flattened_distance_matrix = [i for j in data['distance_matrix'] for i in j]
    max_travel_distance = 2.5 * max(flattened_distance_matrix)
    #print(max_travel_distance)
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        int(max_travel_distance),  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(0)


    # FUNCION CALLBACK Y DIMENSION PARA CAPACIDADES
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]
    
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # FUNCION CALLBACK Y DIMENSION PARA DURACIONES
    def duration_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['duration_matrix'][from_node][to_node]

    duration_callback_index = routing.RegisterTransitCallback(duration_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(duration_callback_index)

    time = 'Time'
    flattened_duration_matrix = [i for j in data['duration_matrix'] for i in j]
    max_travel_time = 2.5 * max(flattened_duration_matrix)
    #max_travel_time = 36000
    #print(max_travel_time)

    routing.AddDimension(
        duration_callback_index,
        int(max_travel_time),  # allow waiting time
        int(max_travel_time),  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)

    if len(data['pickups_deliveries']) > 0:   
        for request in data['pickups_deliveries']:
            pickup_index = manager.NodeToIndex(request[0])
            delivery_index = manager.NodeToIndex(request[1])
            routing.AddPickupAndDelivery(pickup_index, delivery_index)
            routing.solver().Add(
                routing.VehicleVar(pickup_index) == routing.VehicleVar(
                    delivery_index))
            routing.solver().Add(
                distance_dimension.CumulVar(pickup_index) <=
                distance_dimension.CumulVar(delivery_index))
    # Add time window constraints for each vehicle start node.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == 0:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])

    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(data['time_windows'][0][0],
                                                data['time_windows'][0][1])

    # Instantiate route start and end times to produce feasible times.
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC   )
    search_parameters.time_limit.seconds = 5

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    return solution



def solver_VRP(shipment):
    with open('pickle/distance_matrix_for_shipping.pickle', 'rb') as file:  
        distance_matrix = pickle.load(file)
    with open('pickle/duration_matrix_for_shipping.pickle', 'rb') as file:
        duration_matrix = pickle.load(file)
    data = {
        "distance_matrix": distance_matrix,
        "duration_matrix": duration_matrix, 
        "num_vehicles": shipment['data']['num_vehicles'],
        "depot": 0,
        "demands": shipment['data']['demands'], 
        "vehicle_capacities": shipment['data']['vehicle_capacities'],
        "time_windows": shipment['data']['time_window'],
        "pickups_deliveries": shipment['data']['deliver_to']
    }
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    solution = generate_solution(data, manager, routing)
    print("Solution founded!")
    # print_solution(num_vehicles, manager, routing, solution)
    routes = extract_routes(data['num_vehicles'], manager, routing, solution)
    result_table_content = print_solution(data, manager, routing, solution, shipment)
    routes_array = []
    for vehicle in range(data['num_vehicles']):
        routes_array.append(routes[vehicle])
    print(result_table_content)
    return routes_array,result_table_content

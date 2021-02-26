from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


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
def dynamic_cost(data, from_node, to_node):
    return data['distance_matrix'][from_node][to_node]


def generate_solution(data, manager, routing):
    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        # return data['distance_matrix'][from_node][to_node]
        return dynamic_cost(data, from_node, to_node)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    flattened_distance_matrix = [i for j in data['distance_matrix'] for i in j]
    max_travel_time = int(2 * max(flattened_distance_matrix))

    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        max_travel_time,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

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
    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    return solution




def solver_CVRP(data):
    data = {"distance_matrix": data['distance_matrix'], "num_vehicles": data['num_vehicles'], "depot": 0,
            "demands": data['demands'], "vehicle_capacities": data['vehicle_capacities']}
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    solution = generate_solution(data, manager, routing)
    # print_solution(num_vehicles, manager, routing, solution)
    routes = extract_routes(data['num_vehicles'], manager, routing, solution)

    routes_array = []
    for vehicle in range(data['num_vehicles']):
        routes_array.append(routes[vehicle])
    print(routes_array)
    return routes_array

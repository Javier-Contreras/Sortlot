from scripts.CVRP.db_connection import set_parameters
from scripts.CVRP.db_connection import is_cached
from scripts.CVRP.db_connection import set_solution
from scripts.CVRP.db_connection import get_data
from scripts.CVRP.db_connection import get_solution

from scripts.CVRP.parameters import get_locations
from scripts.CVRP.parameters import get_distance_matrix
from scripts.CVRP.parameters import format_parameters
from scripts.CVRP.solver import solver_CVRP

import datetime


current_date = datetime.datetime.now().date().strftime("%d/%m/%Y")  # Formato: 01/12/2020


# Comprobar si los parámetros son correctos
def check_parameters(data):
    return True


# Elegir versión del problema
def choose_version(data):
    return




# Comprobar el cache

# Guardar todo en la base de datos

# Llamar al solver

# Guardar solucion en base de datos


def main(data):
    data = format_parameters(data)

    #if not is_cached(current_date):
    data['locations_dst'] = get_locations(data['locations_dst'])
    data['locations_depot'] = get_locations(data['locations_depot'])
    data['distance_matrix'] = get_distance_matrix(data['locations_depot'], data['locations_dst'], current_date)
    set_parameters(data, current_date)
    routes_array = solver_CVRP(data)
    set_solution(routes_array, current_date)
    data = get_data(current_date)
    solution = get_solution(current_date)
    return solution
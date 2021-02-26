from pymongo import MongoClient
import pymongo

client = MongoClient('localhost', 27017)
VRP_db = client['VRP_db']
CVRP_collection = VRP_db['CVRP']


def reset_db():
    client = MongoClient('localhost', 27017)

    # Database Reset

    client.drop_database('VRP_db')
    VRP_db = client['VRP_db']
    VRP_db.drop_collection('CVRP')


def is_cached(current_date):

    try:
        data = CVRP_collection.find(
            {
                'data.date': current_date
            }
        )
        print(data[0]['data']['locations_dst'])
        var = data[0]['data']['locations_dst']
        return True

    except:
        return False


def set_parameters(data, current_date):
    CVRP_collection.insert_one(
        {
            'data': {
                'locations_depot': data['locations_depot'],
                'locations_dst': data['locations_dst'],
                'demands': data['demands'],
                'vehicle_capacities': data['vehicle_capacities'],
                'distance_matrix': data['distance_matrix'],
                'num_vehicles': data['num_vehicles'],
                'date': current_date
            }
        }
    )


def get_data(current_date):

    places_found_depot = []
    places_found = []

    data = CVRP_collection.find(
        {
            'data.date': current_date
        }
    )

    client.close()
    print(data[0]['data']['locations_dst'])
    return data[0]['data']


def get_solution(current_date):

    places_found_depot = []
    places_found = []

    data = CVRP_collection.find(
        {
            'data.date': current_date
        }
    )

    client.close()
    print(data[0]['data']['locations_dst'])
    return data[0]['solution']

def set_solution(routes_array, current_date):

    try:
        CVRP_collection.update_one(
            {
                'data.date': current_date
            },
            {
                '$set': {
                    'solution.routes': routes_array,

                }
            }
        )

        client.close()
        print("Guardado correctamente")
    except Exception as e:
        print("Error al guardar en la base de datos")
        print(str(e))

from flask import Flask, render_template, request
from src.VRP.main import main
from src.VRP.dao.db_connection import reset_db
from src.VRP.dao.db_connection import get_all_locations_dst
from src.VRP.dao.db_connection import get_all_vehicles
from src.VRP.dao.db_connection import get_all_locations_depot
from src.VRP.dao.db_connection import get_location_by_province

from src.VRP.dao.shipment_DAO import set_locations_dst_shipping
from src.VRP.dao.shipment_DAO import set_locations_depot_shipping
from src.VRP.dao.shipment_DAO import set_vehicles_shipping
from src.VRP.dao.shipment_DAO import get_shipping_data
from src.VRP.dao.solution_DAO import get_data

import json

app = Flask(__name__)

name = ""
json_locations_dst = None

@app.route('/')
def index():
    global name, json_locations_dst

    name = ""
    json_locations_dst = None

    return render_template('index.html')


@app.route('/locations_dst')
def locations_dst(error_msg="",data=None):
    global name, json_locations_dst
    
    if data!=None :
        locations = data
        print(data)
    else: 
        locations = get_all_locations_dst()

    return render_template('locations_dst.html', locations=locations, name=name, error_msg=error_msg)


@app.route('/locations_depot', methods=['POST'])
def locations_depot():
    global name, json_locations_dst


    name = request.form['name']
    locations_dst = json.loads(request.form['json'])
    set_locations_dst_shipping(locations_dst, name)
    
    locations = get_all_locations_depot()
    

    return render_template('locations_depot.html', locations=locations, name=name)

@app.route('/get_data/<province>', methods=['GET'])
def get_data(province):
    global name, json_locations_dst
    print(province)
    locations_by_province = json.dumps(get_location_by_province(province))

    print(locations_by_province)

    return locations_by_province


@app.route('/vehicles', methods=['POST'])
def vehicles():
    global name
    name = request.form['name']

    locations_depot = json.loads(request.form['json'])

    set_locations_depot_shipping(locations_depot, name)

    vehicles = get_all_vehicles()
    return render_template('vehicles.html', vehicles=vehicles, name=name)


@app.route('/reset', methods=['POST'])
def reset():
    global name, json_locations_dst

    name = ""
    json_locations_dst = None
    reset_db()
    return render_template('index.html')


@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    global name, json_locations_dst

    name = request.form['name']
    print("locations_dst: "+name)

    vehicles = json.loads(request.form['json'])

    set_vehicles_shipping(vehicles, name)
    solution, data = main(name, json_locations_dst)
    if isinstance(solution, str):
        return locations_dst(solution, data)
    #data = get_data(name)
    locations = get_all_locations_depot()
    #return render_template('locations_depot.html', locations = locations, name=name)

    return render_template('solution.html', data = data, solution=solution)


if __name__ == "__main__":
    app.run(debug=True,port=8080)

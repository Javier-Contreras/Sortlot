from flask import Flask, render_template, request
from src.CVRP.main import main
from src.CVRP.db_connection import reset_db
from src.CVRP.db_connection import get_all_locations_dst
from src.CVRP.db_connection import get_all_vehicles
from src.CVRP.db_connection import get_all_locations_depot
from src.CVRP.db_connection import set_locations_dst_shipping
from src.CVRP.db_connection import set_locations_depot_shipping
from src.CVRP.db_connection import set_vehicles_shipping


from src.CVRP.db_connection import get_shipping_data
from datetime import datetime

import json
app = Flask(__name__)
import time
from flask_table import Table, Col

from src.format_json import format_dst
from src.format_json import format_depot
from src.format_json import format_vehicle


name = ""

@app.route('/')
def index():
    locations = get_all_locations_dst()
    # return render_template('index.html')
    return render_template('index.html', locations = locations)



@app.route('/locations_dst')
def locations_dst():
    locations = get_all_locations_dst()

    return render_template('locations_dst.html', locations = locations)

@app.route('/locations_depot', methods=['POST'])
def locations_depot():
    global name
    name = request.form['name']
    
    f = request.form['json']
    
    locations_dst = format_dst(f)

    set_locations_dst_shipping(locations_dst, name)
    
    locations = get_all_locations_depot()
    return render_template('locations_depot.html', locations = locations)


@app.route('/vehicles', methods=['POST'])
def vehicles():
    global name

    f = request.form['json']
    locations_depot = format_depot(f)

    set_locations_depot_shipping(locations_depot, name)

    vehicles = get_all_vehicles()

    return render_template('vehicles.html', vehicles = vehicles)



@app.route('/reset', methods=['POST'])
def reset():
    reset_db()
    return render_template('index.html')



@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    global name
    f = request.form['json']

    vehicles = format_vehicle(f)

    set_vehicles_shipping(vehicles, name)
    solution, data = main(name)
    if not data:
        return solution
    return str(solution['routes'])


@app.route('/confirm_data', methods=['POST'])
def confirm_data():
    # locations_dst_parsed = parse_locations(request.form['locations_dst'].split("\n"))
    # locations_depot_parsed = parse_locations(request.form['locations_depot'].split("\n"))
    print("Datos de la tabla")
    f = request.files['destination_addresses']
    locations_dst = format_dst(f)

    f = request.files['origin_addresses']
    locations_depot = format_depot(f)

    locations = [l.get_address() for l in locations_dst]
    print(locations)
    data = {
        'num_vehicles': request.form['num_vehicles'],
        'locations_dst': [l.get_address() for l in locations_dst],
        'locations_depot': [l.get_address() for l in locations_depot],
        'vehicle_capacities': request.form['vehicle_capacities'],
        'demands': [l.get_capacity() for l in locations_dst]
    }

    locations_found = main(data)
    return render_template('test.html', array=data)


if __name__ == "__main__":
    app.run(debug=True)

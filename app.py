from flask import Flask, render_template, request
from src.VRP.main import main
from src.VRP.dao.db_connection import reset_db
from src.VRP.dao.db_connection import get_all_locations_dst
from src.VRP.dao.db_connection import get_all_vehicles
from src.VRP.dao.db_connection import get_all_locations_depot
from src.VRP.dao.shipment_DAO import set_locations_dst_shipping
from src.VRP.dao.shipment_DAO import set_locations_depot_shipping
from src.VRP.dao.shipment_DAO import set_vehicles_shipping
from src.VRP.dao.shipment_DAO import get_shipping_data

import json

app = Flask(__name__)



@app.route('/')
def index():
    #return render_template('solution.html')
    return render_template('index.html')



@app.route('/locations_dst')
def locations_dst():
    locations = get_all_locations_dst()
    print(locations)
    return render_template('locations_dst.html', locations = locations)

@app.route('/locations_depot', methods=['POST'])
def locations_depot():
    name = request.form['name']

    locations_dst = json.loads(request.form['json'])
    set_locations_dst_shipping(locations_dst, name)
    
    locations = get_all_locations_depot()

    return render_template('locations_depot.html', locations = locations, name=name)


@app.route('/vehicles', methods=['POST'])
def vehicles():
    name = request.form['name']

    locations_depot = json.loads(request.form['json'])

    set_locations_depot_shipping(locations_depot, name)

    vehicles = get_all_vehicles()

    return render_template('vehicles.html', vehicles = vehicles, name = name)



@app.route('/reset', methods=['POST'])
def reset():
    reset_db()
    return render_template('index.html')



@app.route('/run_algorithm', methods=['POST'])
def run_algorithm():
    name = request.form['name']

    vehicles = json.loads(request.form['json'])

    set_vehicles_shipping(vehicles, name)
    solution, data = main(name)
    return str(solution)
    if not data:
        return solution
    return str(solution)




if __name__ == "__main__":
    app.run(port=8080, debug=True)

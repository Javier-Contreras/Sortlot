from flask import Flask, render_template, request
from scripts.CVRP.main import main
from scripts.CVRP.db_connection import reset_db
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reset', methods=['POST'])
def reset():
    reset_db()
    return render_template('index.html')


@app.route('/run_algorithm', methods=['POST'])
def run_algorithm_mock():
    # locations_dst_parsed = parse_locations(request.form['locations_dst'].split("\n"))
    # locations_depot_parsed = parse_locations(request.form['locations_depot'].split("\n"))

    data = {
        'num_vehicles': request.form['num_vehicles'],
        'locations_dst': request.form['locations_dst'] + " ",
        'locations_depot': request.form['locations_depot'] + " ",
        'vehicle_capacities': request.form['vehicle_capacities'],
        'demands': request.form['demands']
    }

    locations_found = main(data)
    return str(locations_found)


if __name__ == "__main__":
    app.run(debug=True)

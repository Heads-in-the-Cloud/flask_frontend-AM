from flask import Blueprint, render_template, request, redirect
import requests
import json

airports_controller = Blueprint('airports_controller', __name__, template_folder='templates')
uri = "http://localhost:8081/"


# List all Airports
@airports_controller.route('/airports', methods=['GET'])
def list_airports():
    if request.method == 'GET':
        airports = json.loads(requests.get(uri + 'api/v1/airports').text)
        return render_template("Airports/airports.html", airports=airports)


# Create Airport
@airports_controller.route('/airports/new', methods=['GET', 'POST'])
def origin():
    if request.method == 'GET':
        return render_template('Airports/airportNew.html')
    if request.method == 'POST':
        # send airport as json
        result_form = json.loads(json.dumps(request.form.to_dict()))
        post_form = requests.post(uri + 'api/v1/airports', json=result_form)
        new_object = json.loads(post_form.text)
        if post_form.status_code == 409:
            return render_template("Airports/airportNewResult.html", text="Error inserting airport into database: "
                                                                          "Airport already exists.")
        elif post_form.status_code >= 400:
            return render_template("Airports/airportNewResult.html", text="Error inserting airport into remote "
                                                                          "database.")
        return redirect('/airports/' + new_object['id'])


# GET Airport by ID
@airports_controller.route('/airports/<iata_id>', methods=['GET'])
def edit(iata_id):
    if request.method == 'GET':
        airport = json.loads(requests.get(uri + 'api/v1/airports/' + iata_id).text)
        return render_template('Airports/airport.html', airport=airport)


# Update Airport
@airports_controller.route('/airports/<iata_id>/edit', methods=['GET', 'POST'])
def update(iata_id):
    if request.method == 'GET':
        airport = json.loads(requests.get(uri + 'api/v1/airports/' + iata_id).text)
        return render_template("Airports/airportUpdate.html", airport=airport)
    if request.method == 'POST':
        result_form = json.loads(json.dumps(request.form.to_dict()))
        result_form['iataId'] = iata_id
        post_form = requests.put(uri + 'api/v1/airports/' + iata_id, json=result_form)
        return redirect("/airports/" + iata_id)


# Delete Airport
@airports_controller.route('/airports/<iata_id>/delete', methods=['POST'])
def delete(iata_id):
    if request.method == 'POST':
        requests.delete(uri + '/api/v1/airports/' + iata_id)
        return redirect("/airports")

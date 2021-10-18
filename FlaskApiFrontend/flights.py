from flask import Blueprint, render_template, request, redirect
import requests
import json

flights_controller = Blueprint('flights_controller', __name__, template_folder='templates')
uri = "http://localhost:8081/"


# List all flights
@flights_controller.route('/flights', methods=['GET'])
def list_flights():
    if request.method == 'GET':
        flights = json.loads(requests.get(uri + 'api/v1/flights').text)
        return render_template("flights/flights.html", flights=flights)


# Create flight
@flights_controller.route('/flights/new', methods=['GET', 'POST'])
def origin():
    if request.method == 'GET':
        airplanes = json.loads(requests.get(uri + 'api/v1/airplanes').text)
        routes = json.loads(requests.get(uri + 'api/v1/routes').text)
        return render_template('flights/flightNew.html', airplanes=airplanes, routes=routes)
    if request.method == 'POST':
        # send flight as json
        result_form = json.loads(json.dumps(request.form.to_dict()))
        post_form = requests.post(uri + 'api/v1/flights', json=result_form)
        new_object = json.loads(post_form.text)
        if post_form.status_code == 409:
            return render_template("flights/flightNewResult.html", text="Error inserting flight into database: "
                                                                            "flight already exists.")
        elif post_form.status_code >= 400:
            return render_template("flights/flightNewResult.html", text="Error inserting flight into remote "
                                                                            "database.")
        return redirect('/flights/' + str(new_object['id']))


# GET flight by ID
@flights_controller.route('/flights/<flight_id>', methods=['GET'])
def edit(flight_id):
    if request.method == 'GET':
        flight = json.loads(requests.get(uri + 'api/v1/flights/' + flight_id).text)
        return render_template('flights/flight.html', flight=flight)


# Update flight
@flights_controller.route('/flights/<flight_id>/edit', methods=['GET', 'POST'])
def update(flight_id):
    if request.method == 'GET':
        flight = json.loads(requests.get(uri + 'api/v1/flights/' + flight_id).text)
        airplanes = json.loads(requests.get(uri + 'api/v1/airplanes').text)
        routes = json.loads(requests.get(uri + 'api/v1/routes').text)
        return render_template("flights/flightUpdate.html", flight=flight, airplanes=airplanes, routes=routes)
    if request.method == 'POST':
        result_form = json.loads(json.dumps(request.form.to_dict()))
        result_form['id'] = flight_id
        post_form = requests.put(uri + 'api/v1/flights/' + flight_id, json=result_form)
        return redirect("/flights/" + flight_id)


# Delete flight
@flights_controller.route('/flights/<flight_id>/delete', methods=['POST'])
def delete(flight_id):
    if request.method == 'POST':
        requests.delete(uri + '/api/v1/flights/' + flight_id)
        return redirect("/flights")

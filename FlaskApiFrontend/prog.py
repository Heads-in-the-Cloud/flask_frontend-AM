from flask import Flask, render_template, request, redirect
import requests
import json

app = Flask(__name__)
uri = "http://localhost:8080/"


# home routing (currently routes to tested module)
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def root():
    return redirect("/airports/new")


@app.route('/airports', methods=['GET', 'POST'])
def list_airports():
    if request.method == 'GET':
        airports = json.loads(requests.get(uri + 'api/v1/airports').text)
        return render_template("airports.html", airports=airports)
    if request.method == 'POST':
        # send airport as json
        result_form = json.loads(json.dumps(request.form.to_dict()))
        post_form = requests.post(uri + 'api/v1/airports', json=result_form)
        if post_form.status_code == 409:
            return render_template("airportNewResult.html", text="Error inserting airport into database: Airport "
                                                                 "already exists.")
        elif post_form.status_code >= 400:
            return render_template("airportNewResult.html", text="Error inserting airport into remote database.")
        return redirect('/airports/' + result_form['iataId'])


# form for creating a new airport
@app.route('/airports/new', methods=['GET'])
def origin():
    if request.method == 'GET':
        return render_template('airportNew.html')


# GET for individual airport
@app.route('/airports/<iata_id>', methods=['GET'])
def edit(iata_id):
    if request.method == 'GET':
        airport = json.loads(requests.get(uri + 'api/v1/airports/' + iata_id).text)
        return render_template('airport.html', airport=airport)


@app.route('/airports/<iata_id>/edit', methods=['GET', 'POST'])
def update(iata_id):
    if request.method == 'GET':
        airport = json.loads(requests.get(uri + 'api/v1/airports/' + iata_id).text)
        return render_template("airportUpdate.html", airport=airport)
    if request.method == 'POST':
        result_form = json.loads(json.dumps(request.form.to_dict()))
        post_form = requests.put(uri + 'api/v1/airports/' + iata_id, json=result_form)
        return redirect("/airports/" + iata_id)


@app.route('/airports/<iata_id>/delete', methods=['POST'])
def delete(iata_id):
    if request.method == 'POST':
        requests.delete(uri + '/api/v1/airports/' + iata_id)
        return redirect("/airports")


# base main run function
if __name__ == '__main__':
    app.run(debug=True)

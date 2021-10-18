from flask import Blueprint, render_template, request, redirect
import requests
import json

airplanes_controller = Blueprint('airplanes_controller', __name__, template_folder='templates')
uri = "http://localhost:8081/"


# List all airplanes
@airplanes_controller.route('/airplanes', methods=['GET'])
def list_airplanes():
    if request.method == 'GET':
        airplanes = json.loads(requests.get(uri + 'api/v1/airplanes').text)
        return render_template("airplanes/airplanes.html", airplanes=airplanes)


# Create airplane
@airplanes_controller.route('/airplanes/new', methods=['GET', 'POST'])
def origin():
    if request.method == 'GET':
        types = json.loads(requests.get(uri + 'api/v1/airplaneTypes').text)
        return render_template('airplanes/airplaneNew.html', types=types)
    if request.method == 'POST':
        # send airplane as json
        result_form = json.loads(json.dumps(request.form.to_dict()))
        post_form = requests.post(uri + 'api/v1/airplanes', json=result_form)
        new_object = json.loads(post_form.text)
        if post_form.status_code == 409:
            return render_template("airplanes/airplaneNewResult.html", text="Error inserting airplane into database: "
                                                                      "airplane already exists.")
        elif post_form.status_code >= 400:
            return render_template("airplanes/airplaneNewResult.html", text="Error inserting airplane into remote "
                                                                      "database.")
        return redirect('/airplanes/' + str(new_object['id']))


# GET airplane by ID
@airplanes_controller.route('/airplanes/<airplane_id>', methods=['GET'])
def edit(airplane_id):
    if request.method == 'GET':
        airplane = json.loads(requests.get(uri + 'api/v1/airplanes/' + airplane_id).text)
        return render_template('airplanes/airplane.html', airplane=airplane)


# Update airplane
@airplanes_controller.route('/airplanes/<airplane_id>/edit', methods=['GET', 'POST'])
def update(airplane_id):
    if request.method == 'GET':
        airplane = json.loads(requests.get(uri + 'api/v1/airplanes/' + airplane_id).text)
        types = json.loads(requests.get(uri + 'api/v1/airplaneTypes').text)
        return render_template("airplanes/airplaneUpdate.html", airplane=airplane, types=types)
    if request.method == 'POST':
        result_form = json.loads(json.dumps(request.form.to_dict()))
        result_form['id'] = airplane_id
        post_form = requests.put(uri + 'api/v1/airplanes/' + airplane_id, json=result_form)
        return redirect("/airplanes/" + airplane_id)


# Delete airplane
@airplanes_controller.route('/airplanes/<airplane_id>/delete', methods=['POST'])
def delete(airplane_id):
    if request.method == 'POST':
        requests.delete(uri + '/api/v1/airplanes/' + airplane_id)
        return redirect("/airplanes")

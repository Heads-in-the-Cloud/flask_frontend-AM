from flask import Blueprint, render_template, request, redirect, session, url_for
import requests
import json

airplane_types_controller = Blueprint('airplane_types_controller', __name__, template_folder='templates')
uri = "http://localhost:8081/"


# List all airplane_types
@airplane_types_controller.route('/airplane_types', methods=['GET'])
def list_airplane_types():
    if request.method == 'GET':
        airplane_types = json.loads(requests.get(uri + 'api/v1/airplaneTypes').text)
        errormsg = ''
        if 'errormsg' in request.args:
            errormsg = request.args['errormsg']
        return render_template("airplaneTypes/airplaneTypes.html", airplane_types=airplane_types, errormsg=errormsg)


# Create airplane_type
@airplane_types_controller.route('/airplane_types/new', methods=['GET', 'POST'])
def airplane():
    if request.method == 'GET':
        return render_template('airplaneTypes/airplaneTypeNew.html')
    if request.method == 'POST':
        # send airplane_type as json
        result_form = json.loads(json.dumps(request.form.to_dict()))
        post_form = requests.post(uri + 'api/v1/airplaneTypes', json=result_form)
        new_object = json.loads(post_form.text)
        if post_form.status_code >= 400:
            return redirect(url_for('.list_airplane_types', errormsg="Unable to insert Airplane Type."))
        return redirect('/airplane_types/' + str(new_object['id']))


# GET airplane_type by ID
@airplane_types_controller.route('/airplane_types/<airplane_type_id>', methods=['GET'])
def edit(airplane_type_id):
    if request.method == 'GET':
        airplane_type = json.loads(requests.get(uri + 'api/v1/airplaneTypes/' + airplane_type_id).text)
        return render_template('airplaneTypes/airplaneType.html', airplane_type=airplane_type)


# Update airplane_type
@airplane_types_controller.route('/airplane_types/<airplane_type_id>/edit', methods=['GET', 'POST'])
def update(airplane_type_id):
    if request.method == 'GET':
        airplane_type = json.loads(requests.get(uri + 'api/v1/airplaneTypes/' + airplane_type_id).text)
        return render_template("airplaneTypes/airplaneTypeUpdate.html", airplane_type=airplane_type)
    if request.method == 'POST':
        result_form = json.loads(json.dumps(request.form.to_dict()))
        result_form['id'] = airplane_type_id
        post_form = requests.put(uri + 'api/v1/airplaneTypes/' + airplane_type_id, json=result_form)
        return redirect("/airplane_types/" + airplane_type_id)


# Delete airplane_type
@airplane_types_controller.route('/airplane_types/<airplane_type_id>/delete', methods=['POST'])
def delete(airplane_type_id):
    if request.method == 'POST':
        requests.delete(uri + '/api/v1/airplaneTypes/' + airplane_type_id)
        return redirect("/airplane_types")

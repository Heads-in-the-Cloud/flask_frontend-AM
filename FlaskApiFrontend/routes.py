from flask import Blueprint, render_template, request, redirect
import requests
import json

routes_controller = Blueprint('routes_controller', __name__, template_folder='templates')
uri = "http://localhost:8081/"


# List all routes
@routes_controller.route('/routes', methods=['GET'])
def list_routes():
    if request.method == 'GET':
        routes = json.loads(requests.get(uri + 'api/v1/routes').text)
        return render_template("routes/routes.html", routes=routes)


# Create route
@routes_controller.route('/routes/new', methods=['GET', 'POST'])
def origin():
    if request.method == 'GET':
        airports = json.loads(requests.get(uri + 'api/v1/airports').text)
        return render_template('routes/routeNew.html', airports=airports)
    if request.method == 'POST':
        # send route as json
        result_form = json.loads(json.dumps(request.form.to_dict()))
        post_form = requests.post(uri + 'api/v1/routes', json=result_form)
        new_object = json.loads(post_form.text)
        if post_form.status_code == 409:
            return render_template("routes/routeNewResult.html", text="Error inserting route into database: "
                                                                      "route already exists.")
        elif post_form.status_code >= 400:
            return render_template("routes/routeNewResult.html", text="Error inserting route into remote "
                                                                      "database.")
        return redirect('/routes/' + str(new_object['id']))


# GET route by ID
@routes_controller.route('/routes/<route_id>', methods=['GET'])
def edit(route_id):
    if request.method == 'GET':
        route = json.loads(requests.get(uri + 'api/v1/routes/' + route_id).text)
        return render_template('routes/route.html', route=route)


# Update route
@routes_controller.route('/routes/<route_id>/edit', methods=['GET', 'POST'])
def update(route_id):
    if request.method == 'GET':
        route = json.loads(requests.get(uri + 'api/v1/routes/' + route_id).text)
        airports = json.loads(requests.get(uri + 'api/v1/airports').text)
        return render_template("routes/routeUpdate.html", route=route, airports=airports)
    if request.method == 'POST':
        result_form = json.loads(json.dumps(request.form.to_dict()))
        result_form['id'] = route_id
        post_form = requests.put(uri + 'api/v1/routes/' + route_id, json=result_form)
        return redirect("/routes/" + route_id)


# Delete route
@routes_controller.route('/routes/<route_id>/delete', methods=['POST'])
def delete(route_id):
    if request.method == 'POST':
        requests.delete(uri + '/api/v1/routes/' + route_id)
        return redirect("/routes")

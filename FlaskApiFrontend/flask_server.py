from flask import Flask, render_template, redirect

from FlaskApiFrontend.airports import airports_controller
from FlaskApiFrontend.routes import routes_controller
from FlaskApiFrontend.airplane_types import airplane_types_controller
from FlaskApiFrontend.airplanes import airplanes_controller
from FlaskApiFrontend.flights import flights_controller

app = Flask(__name__)
app.register_blueprint(airports_controller)
app.register_blueprint(routes_controller)
app.register_blueprint(airplane_types_controller)
app.register_blueprint(airplanes_controller)
app.register_blueprint(flights_controller)


@app.route('/', methods=['GET'])
def root():
    return redirect('/home')


# Home (currently routes to tested module)
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


# About
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


# Flask App
if __name__ == '__main__':
    app.run(debug=True)

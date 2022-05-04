import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *


topbar = Navbar(
    View('Home', 'home'),
    View('About', 'about')
)

nav = Nav()
nav.register_element('top', topbar)


app = Flask(__name__)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/details', methods=['GET', 'POST'])
def details():
    pass


@app.route('/search', methods=['GET', 'POST'])
def search():
    pass


@app.route('/about', methods=['GET', 'POST'])
def about():
    pass


nav.init_app(app)


def get_random_recipe():
    random = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')
    print(random.json())


if __name__ == '__main__':
    get_random_recipe()
    app.run(debug=True)
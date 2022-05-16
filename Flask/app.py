import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_nav.elements import *


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form.get('search'))
        print(request.form.get('Filter'))
        return redirect('/search/{0}/{1}'.format(request.form.get('search'), request.form.get('Filter')), code=301)
    else:
        return render_template('index.html', meal1=get_random_recipe(), meal2=get_random_recipe(),
                               meal3=get_random_recipe())


@app.route('/details/<int:id>', methods=['GET', 'POST'])
def details(id):
    if id == 1:
        return redirect('/', code=301)
    else:
        return render_template('details.html', meal_title=get_meal(id)[0], meal_ingredients=get_meal(id)[1])


@app.route('/search/<item>/<filter>', methods=['GET', 'POST'])
def search(filter, item):
    if request.method == 'POST':
        pass
    else:
        list_meals = get_category(filter, item)
    return render_template('search.html', meals=list_meals)


def get_random_recipe():
    random_meal = requests.get('https://www.themealdb.com/api/json/v1/1/random.php').json()
    id = random_meal['meals'][0]['idMeal']
    title = random_meal['meals'][0]['strMeal']
    image = random_meal['meals'][0]['strMealThumb']
    tags = random_meal['meals'][0]['strTags']
    return id, title, image, tags


def get_meal(id):
    meal = requests.get('https://www.themealdb.com/api/json/v1/1/lookup.php?i={0}'.format(id)).json()
    title = meal['meals'][0]['strMeal']

    ingredients = []

    for i in range(1,20):
        if meal['meals'][0]['strIngredient{0}'.format(i)] != '':
            ingredients.append(meal['meals'][0]['strIngredient{0}'.format(i)])

    return title, ingredients


def get_category(filter, item):
    final_list = []
    if filter == 's':
        list_meals = requests.get('https://www.themealdb.com/api/json/v1/1/search.php?s={0}'.format(item)).json()
    else:
        list_meals = requests.get('https://www.themealdb.com/api/json/v1/1/filter.php?{0}={1}'.format(filter, item)).json()
    print(list_meals['meals'])
    if list_meals['meals'] is None:
        final_list = [['', '/static/images/not_found.png', '1']]
        return final_list
    for i in list_meals['meals']:
        temp_list = [i['strMeal'], i['strMealThumb'], i['idMeal']]
        final_list.append(temp_list)
    return final_list


if __name__ == '__main__':
    get_category('c', 'beef')
    app.run(debug=True)

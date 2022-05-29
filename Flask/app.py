# Imports
import requests
import requests.cookies
from flask import Flask, render_template, redirect, make_response
from flask_nav.elements import *
import json
import re


# Flask App initialization
app = Flask(__name__)


tokens = open('../files/tokens.json', 'r')
tokens_dict = json.load(tokens)
tokens.close()


# Flask App Routes
# Homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect('/search/{0}/{1}'.format(request.form.get('search'), request.form.get('Filter')), code=301) # Redirect to search page with the given search values
    if request.cookies.get('userID'):
        return render_template('index.html', meal1=get_random_recipe(), meal2=get_random_recipe(), meal3=get_random_recipe())   # Render the homepage with 3 random recipes
    else:
        resp = make_response(redirect('/'))
        resp.set_cookie('userID', 'ben')
        return resp


# Details page
@app.route('/details/<int:id>', methods=['GET', 'POST'])
def details(id):
    if request.method == 'GET':
        if id == 1:
            return redirect('/', code=301)  # Redirect to homepage if id is 1 -> id is 1 if the search results are empty
        else:
            return render_template('details.html', meal_title=get_meal(id)[0], meal_ingredients=get_meal(id)[1], meal_image=get_meal(id)[2], meal_id=id, name=request.cookies.get('userID'), reviews=get_reviews(id)[0])
    if request.method == 'POST':
        for i in range(len(tokens_dict['benutzer'])):
            if tokens_dict['benutzer'][i]['name'] == request.cookies.get('userID'):
                token = tokens_dict['benutzer'][i]['token']
                break
        star = request.form.get('rating')
        post_request = {"token": token, "mealId": id, "sterne": star, "kommentar": request.form.get('own-review')}
        json_ = json.dumps(post_request)
        print(json_)
        r = requests.post('https://informatik.mygymer.ch/fts/themealdb/', data=json_)
        print(r.text)
        return render_template('details.html', meal_title=get_meal(id)[0], meal_ingredients=get_meal(id)[1], meal_image=get_meal(id)[2], meal_id=id, name=request.cookies.get('userID'), reviews=get_reviews(id)[0])


# Search page
@app.route('/search/<item>/<filter>', methods=['GET', 'POST'])
def search(filter, item):
    if request.method == 'POST':
        pass
    else:
        list_meals = get_category(filter, item) # Get the list of meals from the API with the given filter and item
    return render_template('search.html', meals=list_meals) # Render the search page with the list of meals


@app.route('/login/<val>', methods=['GET'])
def login(val):
    return render_template('login.html', id=val)


@app.route('/setcookie/<val>', methods=['POST', 'GET'])
def setcookie(val):
    if request.method == 'POST':
        user = request.form['nm']
        resp = make_response(redirect('/details/{0}'.format(val)))
        resp.set_cookie('userID', user)
        return resp


# functions
# function to get a random recipe
def get_random_recipe():
    total_review = 0
    random_meal = requests.get('https://www.themealdb.com/api/json/v1/1/random.php').json() # Get a random recipe from the API
    id = random_meal['meals'][0]['idMeal']  # Get the id of the random recipe
    title = random_meal['meals'][0]['strMeal']  # Get the title of the random recipe
    image = random_meal['meals'][0]['strMealThumb']   # Get the image of the random recipe

    review = requests.get('https://informatik.mygymer.ch/fts/themealdb/?id={0}'.format(id)).json()  # Get the reviews of the random recipe from the API
    for i in range(len(review['bewertungen'])):
        total_review += int(review['bewertungen'][i]['sterne'])
    if total_review == 0:
        stars = 'N/A'
    else:
        stars = round(total_review / len(review['bewertungen']), 1)
    return id, title, image, stars   # Return the id, title, image and the overall review of the random recipe


# function to get a specific recipe
def get_meal(id):
    meal = requests.get('https://www.themealdb.com/api/json/v1/1/lookup.php?i={0}'.format(id)).json()
    title = meal['meals'][0]['strMeal']
    image = meal['meals'][0]['strMealThumb']

    ingredients = {}

    for i in range(1, 20):
        if meal['meals'][0]['strIngredient{0}'.format(i)] != '':  #test if ingredient not empty
            ingredients[meal['meals'][0]['strIngredient{0}'.format(i)]] = meal['meals'][0]['strMeasure{0}'.format(i)]

    return title, ingredients, image


# function to get a list of recipes from the API with the given filter and item
def get_category(filter, item):
    final_list = []
    total_review = 0
    if filter == 's':   # Search by meal name
        list_meals = requests.get('https://www.themealdb.com/api/json/v1/1/search.php?s={0}'.format(item)).json()   # Get the list of meals from the API with the given filter and item
    else:
        list_meals = requests.get('https://www.themealdb.com/api/json/v1/1/filter.php?{0}={1}'.format(filter, item)).json()  # Get the list of meals from the API with the given filter and item
    if list_meals['meals'] is None:  # If the list of meals is empty
        final_list = [['', '/static/images/not_found.png', '1']]    # Return a list with a single element with the title, image and id of the not found recipe
        return final_list   # Return the list of meals
    for i in list_meals['meals']:
        temp_list = [i['strMeal'], i['strMealThumb'], i['idMeal']]  # Create a temporary list with the title, image and id of the recipe
        final_list.append(temp_list)    # Append the temporary list to the final list
        review = requests.get('https://informatik.mygymer.ch/fts/themealdb/?id={0}'.format(i['idMeal'])).json()  # Get the reviews of the random recipe from the API
        for ii in range(len(review['bewertungen'])):
            total_review += int(review['bewertungen'][ii]['sterne'])
        if total_review == 0:
            stars = 'N/A'
        else:
            stars = round(total_review / len(review['bewertungen']), 1)
        temp_list.append(stars)  # Append the overall review to the temporary list

    return final_list   # Return the list of meals


def get_reviews(id):
    reviews = requests.get('https://informatik.mygymer.ch/fts/themealdb/?id={0}'.format(id)).json()
    total_stars = 0
    reviews_processed = []
    for i in range(len(reviews['bewertungen'])):
        reviews_processed.append([reviews['bewertungen'][i]['name'], reviews['bewertungen'][i]['kommentar'], reviews['bewertungen'][i]['sterne']])
        total_stars += reviews['bewertungen'][i]['sterne']
    if len(reviews['bewertungen']) != 0:
        total_stars = total_stars / len(reviews['bewertungen'])
    return reviews_processed, total_stars


# run the app
if __name__ == '__main__':
    app.run()

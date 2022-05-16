# Imports
import requests
from flask import Flask, render_template, redirect
from flask_nav.elements import *


# Flask App initialization
app = Flask(__name__)


# Flask App Routes
# Homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect('/search/{0}/{1}'.format(request.form.get('search'), request.form.get('Filter')), code=301) # Redirect to search page with the given search values
    else:
        return render_template('index.html', meal1=get_random_recipe(), meal2=get_random_recipe(), meal3=get_random_recipe())   # Render the homepage with 3 random recipes


# Details page
@app.route('/details/<int:id>', methods=['GET', 'POST'])
def details(id):
    if id == 1:
        return redirect('/', code=301)  # Redirect to homepage if id is 1 -> id is 1 if the search results are empty
    else:
        return render_template('details.html', meal_title=get_meal(id)[0], meal_ingredients=get_meal(id)[1])


# Search page
@app.route('/search/<item>/<filter>', methods=['GET', 'POST'])
def search(filter, item):
    if request.method == 'POST':
        pass
    else:
        list_meals = get_category(filter, item) # Get the list of meals from the API with the given filter and item
    return render_template('search.html', meals=list_meals) # Render the search page with the list of meals


# functions
# function to get a random recipe
def get_random_recipe():
    random_meal = requests.get('https://www.themealdb.com/api/json/v1/1/random.php').json() # Get a random recipe from the API
    id = random_meal['meals'][0]['idMeal']  # Get the id of the random recipe
    title = random_meal['meals'][0]['strMeal']  # Get the title of the random recipe
    image = random_meal['meals'][0]['strMealThumb']   # Get the image of the random recipe
    tags = random_meal['meals'][0]['strTags']   # Get the tags of the random recipe
    return id, title, image, tags   # Return the id, title, image and tags of the random recipe


# function to get a specific recipe
def get_meal(id):
    meal = requests.get('https://www.themealdb.com/api/json/v1/1/lookup.php?i={0}'.format(id)).json()
    title = meal['meals'][0]['strMeal']

    ingredients = []

    for i in range(1, 20):
        if meal['meals'][0]['strIngredient{0}'.format(i)] != '':
            ingredients.append(meal['meals'][0]['strIngredient{0}'.format(i)])

    return title, ingredients


# function to get a list of recipes from the API with the given filter and item
def get_category(filter, item):
    final_list = []
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
    return final_list   # Return the list of meals


# run the app
if __name__ == '__main__':
    app.run()

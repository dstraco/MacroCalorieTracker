# Author: David Stracola
# Project name: Macro Calorie Tracker Web Application
# File description: Main flask application file
from flask import Flask, request, render_template, redirect, url_for
from meal import *
from flask import request, jsonify
import json

app = Flask(__name__)
api = fatSecret()

meals = []

meals.append(Meal("Breakfast"))
meals.append(Meal("Lunch"))
meals.append(Meal("Dinner"))
meals.append(Meal("Snacks"))

@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')

@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        # Retrieve form data
        meal_name = request.form.get('meal_name')
        food_name_str = request.form.get('food_name')
        serving_size_str = request.form.get('serving_size')
        protein_str = request.form.get('protein')
        carbs_str = request.form.get('carbs')
        fats_str = request.form.get('fats')

        # Find existing meal or create a new one
        meal = next((m for m in meals if m.get_name() == meal_name), None)
        if not meal:
            meal = Meal(meal_name)
            meals.append(meal)

        try:
            # Convert to float and handle missing values
            protein = float(protein_str) if protein_str else 0.0
            carbs = float(carbs_str) if carbs_str else 0.0
            fats = float(fats_str) if fats_str else 0.0
            serving_size = float(serving_size_str) if serving_size_str else 0.0
        except ValueError as e:
            return f"Error: Invalid input data. {str(e)}", 400

        # Create a new food object and add it to the meal 
        new_food = Food(food_name_str, protein, carbs, fats, serving_size)
        
        meal.add_food(new_food)

        # Redirect to index page to display updated data
        return redirect(url_for('index'))
    else:
        # Display the form
        return render_template('add_food.html')

@app.route('/remove_food', methods =['POST'])
def remove_food():

    item_id = request.form.get('item_id')
    for meal in meals:
         for food in meal.show_foods():
             if food.get_id() == item_id:
                 meal.remove_food(food)

    return redirect(url_for('show_meals'))

@app.route('/show_meals', methods=['GET', 'POST'])
def show_meals():
    """
    Shows every meal with the food objects in each
    """
    if request.method == 'GET':
        return render_template('show_meals.html', meals=meals)
    else:
        pass

@app.route('/search_food', methods=['GET', 'POST'])
def search_food():
    if request.method == 'POST':
        meal_name = request.form['meal_name']
        food_query = request.form['food_query']

        found = False
        for meal in meals:
            if meal.get_name() == meal_name:
                found = True
        if found == False:
            meals.append(Meal(meal_name))

        food_results = api.foods_search(food_query)

        food_lst = []
        for food in food_results['foods_search']['results']['food']:
            name = food.get('food_name')
            nutrient_info = food.get('servings')
            brand = food.get('brand_name', "Generic")


            food_item = Food(food_name= name, nutrients=nutrient_info, brand=brand)
            food_item.parse_nutrients()
            print('\n')
            food_lst.append(food_item)

        return render_template('search_results.html', food_data=food_lst, meal=meal_name)
    return render_template('search.html')

@app.route('/select_food', methods=['POST'])
def select_food():
    if request.method == 'POST':

        meal_name = request.form['meal_name']
        raw_data = request.form['food_data']
        food_name = request.form["food_name"]

        # Puts food data into JSON format
        food_data = raw_data.replace("'", "\"")

        new_food = Food(food_name=food_name, nutrients=food_data)
        new_food.process_nutrients()

        for meal in meals:
            if meal.get_name() == meal_name:
                meal.add_food(new_food)
                
        # meals.index(meal_name).add_food(new_food)
        return redirect(url_for('index'))
        
@app.route('/api/meals', methods=['GET'])
def get_meals():
    """
    Returns the meals in JSON format
    """
    
    meal_dict = {}
    for meal in meals:
        foods ={}
        for food in meal.get_foodlst():
            
            food_nutrient_info = food.food_dict()
            meal_name = meal.get_name()
            food_name = food.get_name()
            foods[food_name] = food_nutrient_info

            meal_dict[meal_name] = foods

    return meal_dict

if __name__ == '__main__':
    app.run(debug=True)
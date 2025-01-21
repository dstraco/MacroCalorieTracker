meals = document.getElementById('meals');
daily_calories = document.getElementById('daily-calories');
daily_protein = document.getElementById('daily-protein');
daily_carbs = document.getElementById('daily-carbs');
daily_fat = document.getElementById('daily-fat');
meal_containers = document.getElementsByClassName('container');


// Script for index.html
if (document.querySelector('h1').innerText === 'Big 3 Calorie and Macro tracker') {

    async function getMeals() {
        try {
            const response = await fetch('/api/meals');
            const meals = await response.json();

            updateUI(meals);

        } catch (error) {
            console.log('Error fetching meals', error);
        }
    }
    document.addEventListener('DOMContentLoaded', getMeals);
}

function calculateDailyMacros(meals) {

    console.log('Calculating macros')
    console.log(meals);

    let total_calories = 0;
    let total_protein = 0;
    let total_carbs = 0;
    let total_fat = 0;
    let total_fiber = 0;
    let total_sugar = 0;
    let total_sodium = 0;
    let total_cholesterol = 0;
    let total_saturated_fat = 0;

    for (let meal in meals) {
        for (let food in meals[meal]) {
            total_protein += meals[meal][food].protein;
            total_carbs += meals[meal][food].carbs;
            total_fat += meals[meal][food].fat;
            total_fiber += meals[meal][food].fiber;
            total_sugar += meals[meal][food].sugar;
            total_sodium += meals[meal][food].sodium;
            total_cholesterol += meals[meal][food].cholesterol;
            total_saturated_fat += meals[meal][food].saturated_fat;
            total_calories = Math.round(total_protein * 4 + total_carbs * 4 + total_fat * 9);
        }
    }
    return { "total_calories": total_calories, "total_protein": total_protein, "total_carbs": total_carbs, "total_fat": total_fat, "total_fiber": total_fiber, "total_sugar": total_sugar, "total_sodium": total_sodium, "total_cholesterol": total_cholesterol, "total_saturated_fat": total_saturated_fat };
}
// this fucntion will become update UI
function updateUI(meals) {

    let macros = calculateDailyMacros(meals);
    daily_calories.textContent = `Calories: ${macros.total_calories} kcal`;
    daily_protein.textContent = `Protein: ${macros.total_protein} g`;
    daily_carbs.textContent = `Carbs: ${macros.total_carbs} g`;
    daily_fat.textContent = `Fat: ${macros.total_fat} g`;

    calculateMealMacros('Breakfast', meals);
    calculateMealMacros('Lunch', meals);
    calculateMealMacros('Dinner', meals);
    calculateMealMacros('Snacks', meals);

}

function calculateMealMacros(meal, meals) {
    let meal_protein = 0;
    let meal_carbs = 0;
    let meal_fat = 0;

    for (let food in meals[meal]) {
        meal_protein += meals[meal][food].protein;
        meal_carbs += meals[meal][food].carbs;
        meal_fat += meals[meal][food].fat;
    }

    meal_calories = Math.round(meal_protein * 4 + meal_carbs * 4 + meal_fat * 9);

    const mealElements = {
        'Breakfast': 'breakfast',
        'Lunch': 'lunch',
        'Dinner': 'dinner',
        'Snacks': 'snacks'
    };
    
    document.getElementById(`${mealElements[meal]}-protein`).textContent = `Protein: ${meal_protein} g`;
    document.getElementById(`${mealElements[meal]}-carbs`).textContent = `Carbs: ${meal_carbs} g`;
    document.getElementById(`${mealElements[meal]}-fat`).textContent = `Fat: ${meal_fat} g`;
    document.getElementById(`${mealElements[meal]}-calories`).textContent = `Calories: ${meal_calories} kcal`;
}
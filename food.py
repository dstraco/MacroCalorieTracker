# Author: David Stracola
# Project name: Macro & Calorie Tracker
# File description: Food class for modeling food objects in the program and their associated fields and methods
import uuid
import json

class Food:
    def __init__(self, food_name, protein=None, carbs=None, fats=None, sodium=None, sugar=None, cholesterol=None,
                 fiber=None, serving_description = None, nutrients=None, brand=None):

        self.__name = food_name
        self.__protein = protein
        self.__carbs = carbs
        self.__fats = fats
        self.__sodium = sodium
        self.__sugar = sugar
        self.__cholesterol = cholesterol
        self.__fiber = fiber
        self.__serving_description = serving_description
        self.__id = str(uuid.uuid4())
        self.__nutrients = nutrients # nutrients in JSON format
        self.__brand = brand
        self.__serving_info = {}

    def parse_nutrients(self):
        """
        Function to parse the nutrients from the API response
        """
        data = self.__nutrients
        for item in data['serving']:
            id = item['serving_id']
            serving_description = item['serving_description']

            try:
                self.__serving_info[serving_description] = {
                    'Serving size': item['serving_description'],
                    'Calories': item['calories'],
                    'Carbohydrate': item['carbohydrate'] + 'g',
                    'Protein': item['protein'] + 'g',
                    'Fat': item['fat'] + 'g',
                    'Sodium': item['sodium'] + 'mg',
                    'Cholesterol': item['cholesterol'] + 'mg',
                    'Fiber': item['fiber'] + 'g',
                    'Sugar': item['sugar'] + 'g'
                        }

            except KeyError as e:
                print(e)
                print('Missing Key')

    def get_serving_info(self, description=None):
        if description is None:
            return self.__serving_info
        else:
            return self.__serving_info.get(description)

    def set_brand(self, brand_name):
        self.__brand = brand_name

    def get_brand(self):
        return self.__brand
    
    def set_nutrients(self, nutrient_dict):
        self.__nutrient_dict = nutrient_dict

    def process_nutrients(self):
        """
        Function to process nutrient json into macros
        """
        nutrients = json.loads(self.__nutrients)
        self.__protein = float(nutrients['Protein'].strip('g'))
        self.__carbs = float(nutrients['Carbohydrate'].strip('g'))
        self.__fats = float(nutrients['Fat'].strip('g'))
        self.__sodium = float(nutrients['Sodium'].strip('mg'))
        self.__cholesterol = float(nutrients['Cholesterol'].strip('mg'))
        self.__fiber = float(nutrients['Fiber'].strip('g'))
        self.__sugar = float(nutrients['Sugar'].strip('g'))

    def get_nutrients(self):
        return self.__nutrients
    
    def get_id(self):
        return self.__id
        
    def get_name(self):
        return self.__name

    def __str__(self):
        return str(self.__name)

    def get_protein(self):
        return self.__protein

    def get_carbs(self):
        return self.__carbs

    def get_fats(self):
        return self.__fats

    def set_protein(self, value):
        self.__protein = value

    def set_carbs(self, value):
        self.__carbs = value

    def set_fats(self, value):
        self.__fats = value

    # 4 calories per gram of protein and carbs
    # 9 calories per gram of fats
    def get_calories(self):
        return (4 * self.__protein) + (4 * self.__carbs) + (9 * self.__fats)
     
    def food_dict(self):
        """
        Returns a dictionary of the food object
        Used for serialization
        """
        return {'name': self.__name, 'protein': self.__protein, 'carbs': self.__carbs, 'fat': self.__fats, 'fiber': self.__fiber, 'sugar': self.__sugar, 'sodium': self.__sodium, 'cholesterol': self.__cholesterol}
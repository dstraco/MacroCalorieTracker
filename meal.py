# Author: David Stracola
# Project name: Macro & Calorie Tracker
# File description: Meal class for modeling meal objects in the program and their associated fields and methods
import uuid
from food import Food
import requests
from fat_secret import fatSecret

##########Meal class#############
class Meal:
    '''a class for all things meals'''

    def __init__(self, name):
        self.__protein = 0
        self.__carbs = 0
        self.__fats = 0
        self.__foodlst = []
        self.__calories = (self.__protein * 4) + (self.__carbs * 4) + (self.__fats * 9)
        self.__name = name

    def get_foodlst(self):
        return self.__foodlst

    def get_name(self):
        return self.__name

    def get_calories(self):
        return self.__calories

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

    def show_foods(self):
        '''function to show food items in a meal'''
        return self.__foodlst

    def manual_food_entry(self, food_name, protein, carbs, fats, serving_size):
        '''manual food entry'''

        self.__foodlst.append(Food(food_name, protein, carbs, fats, serving_size))
        self.compile_macros()

    def compile_macros(self):
        """function to compile macro values"""
        self.__protein = 0
        self.__carbs = 0
        self.__fats = 0
        for food in self.__foodlst:
            self.__protein += food.get_protein()
            self.__carbs += food.get_carbs()
            self.__fats += food.get_fats()
        self.__calories = (self.__protein * 4) + (self.__carbs * 4) + (self.__fats * 9)

    def add_food(self, food):
        '''function to add food to a meal'''
        self.__foodlst.append(food)
        self.compile_macros()

    def remove_food(self, food):

        self.__foodlst.remove(food)
        self.compile_macros()





        
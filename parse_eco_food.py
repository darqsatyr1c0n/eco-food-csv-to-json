import csv
import json
import re

# Declaring an empty array for parser
food = {}

def fix_eco_name(name):
    # Regular expression to add spaces to FoodNames while keeping FoodNAMES acronimes
    
    re_outer = re.compile(r'([^A-Z ])([A-Z])')
    re_inner = re.compile(r'(?<!^)([A-Z])([^A-Z])')
    displayName = re_outer.sub(r'\1 \2', re_inner.sub(r' \1\2', name))
    
    return displayName

def parse_ingridients(ingridients):
    # Converting string of ingridients into useful array
    if ingridients == "":
        return []
    else:
        ingridient_list = ingridients.split(";")

        ingridients_parsed = []
        
        for food in ingridient_list:
            food_splited = food.split(",")
            food_name = food_splited[0]
            food_amount = food_splited[1]
            ingridients_parsed.append({food_name: food_amount})
        
        return ingridients_parsed

with open('food.csv', newline='') as csvfile:
    food_csv = csv.reader(csvfile, delimiter=';')
    
    # Counter for food ID
    i = 1
    for row in food_csv:
        name = row[0]
        parentTable = row[2].lower()
        calories = int(row[6])
        carbs = int(row[7])
        protein = int(row[8])
        fat = int(row[9])
        vitamins = int(row[10])
        weight = int(row[12])
        skill = row[13].lower()
        skillLevel = row[14]
        ingridients = parse_ingridients(row[18])
        ingridients_static = parse_ingridients(row[19])
        tag_recipe = parse_ingridients(row[16])
        tag_recipe_static = parse_ingridients(row[17])

        food[name] = {
            "id": i,
            "displayName": fix_eco_name(name),
            "nutrition": {
                "carbs": carbs,
                "protein": protein,
                "fat": fat,
                "vitamins": vitamins,
                "calories": calories,
                "total": carbs + fat + protein + vitamins,
            },
            "profession": skill,
            "professionLevel": skillLevel,
            "ingridients": ingridients,
            "ingridients_static": ingridients_static,
            "tags": tag_recipe,
            "tags_static": tag_recipe_static,
            "tableKey": parentTable,
        }

        # Adding +1 to food ID
        i += 1
        
# Saving result in food.json file in local folder, if present will be overwritted
with open ('food.json', mode='w') as food_json:
    json.dump(food, food_json, indent=4)
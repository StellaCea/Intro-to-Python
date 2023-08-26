import pickle

def calc_difficulty(recipe):
    if recipe["Cooking Time"] < 10 and len(recipe["Ingredients"]) < 4:
        recipe['Difficulty'] = "Easy"
    if recipe["Cooking Time"] < 10 and len(recipe["Ingredients"]) > 4:
        recipe['Difficulty'] = "Medium"
    if recipe["Cooking Time"] >= 10 and len(recipe["Ingredients"]) < 4:
        recipe['Difficulty'] = "Intermediate"
    if recipe["Cooking Time"] >= 10 and len(recipe["Ingredients"]) >= 4:
        recipe['Difficulty'] = "Hard"

def take_recipe():
    name = input("Enter the name of your recipe: ")
    cooking_time = int(input("Enter the cooking time in minutes: "))
    ingredients = input("Enter the ingredients, separated by comma: ").split(", ")
    recipe = {'Name': name, 'Cooking Time': cooking_time, 'Ingredients': ingredients}

    diffuculty = calc_difficulty(recipe)
    return recipe

recipes_list = []
all_ingredients = []

userfile = input("Enter a filename with your recipes: ") + ".bin"

try:
    recipes_file = open(userfile, 'rb')
    data = pickle.load(recipes_file)
except FileNotFoundError:
    print("No file with such name is found. Creating new file")
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
except:
    print("Something went wrong")
    data = {
        'recipes_list': [],
        'all_ingredients': []
    }
else:
    recipes_file.close()
finally:
    #extracts values from data into 2 lists
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

numb_of_recepes = int(input("How many recepes would you like to enter?"))
for i in range(numb_of_recepes):
    recipe = take_recipe()
    print(recipe)

    for ingredient in recipe['Ingredients']:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)
    recipes_list.append(recipe)

data = {'recipes_list': recipes_list, 'all_ingredients': all_ingredients}

recipes_file = open(userfile, 'wb')
pickle.dump(data, recipes_file)
print("File updated")



    




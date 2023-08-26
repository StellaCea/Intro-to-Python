import pickle

def display_recipe(recipe):
    print("Name: ", recipe["Name"])
    print("Cooking Time: ", str(recipe["Cooking Time"]))
    print("Ingredients: ", recipe["Ingredients"])
    print("Difficulty: ", recipe["Difficulty"])

def search_ingredient(data):
    all_ingredients = data['all_ingredients']
    indexed_ingredients = list(enumerate(all_ingredients, 1))

    for ingredient in indexed_ingredients:
        print(ingredient[0], " - ", ingredient[1])

    # user picks a number from the list
    try:
        num = int(input("Enter a number: "))
        index = num - 1
        ingredient_search = all_ingredients[index]

    except IndexError:
        print("Oops, the input is not valid")
    except:
        print("Something went wrong")
    else:
        for recipe in data["recipes_list"]:
            for ingredient in recipe["Ingredients"]:
                if ingredient == ingredient_search:
                    print("You can cook this recipe with this ingredient: ")
                    print(display_recipe(recipe))
                

userfile = input("Enter a recipe file name: ") + ".bin"
try:
    recipe_file = open(userfile, 'rb')
    data = pickle.load(recipe_file)
except FileNotFoundError:
    print("No such file found. Creating new file")
    data = {"recipes_list": [], "all_ingredients": []}
except:
    print("Something went wrong")
else:
    search_ingredient(data)
finally:
    recipe_file.close()

recipes_list = []
ingredients_list = []

def take_recipe(name="", cooking_time="", ingredients="", difficulty="", recipe=""):
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter cooking duration (in min): "))
    ingredients = input("Enter ingredients: ").split(", ")

    recipe = {
        "name": name, 
        "cooking_time": cooking_time,
        "difficulty": difficulty,
        "ingredients":ingredients
    }

    return recipe


n = int(input("Enter a number of recipes: "))
for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    #determine the difficulty by cooking_time
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"]="Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"]="Intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >=4:
        recipe["difficulty"]="Hard"

for recipe in recipes_list:
    print("Recipe: ", recipe["name"])
    print("Cooking Time (min): ", str(recipe["cooking_time"]))
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty level: ", recipe["difficulty"] )

print("----------------------------------------")
print("Ingredients Available Across All Recipes")
print("----------------------------------------")
ingredients_list.sort()
for ingredient in ingredients_list:
    print(ingredient)


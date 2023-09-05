from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://cf-python:password@localhost/task_database")
Base = declarative_base()

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(50))
    ingredients = Column(String(225))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + "- difficulty: " + self.difficulty + ">"

    def __str__(self):
        output =  "\nName: " + self.name + "\nCooking Time: " + str(self.cooking_time) + "\nIngredients: " + str(self.ingredients) + "\nDifficulty: " + str(self.difficulty)
        return output
    
def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        Recipe.difficulty = "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        Recipe.difficulty = "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        Recipe.difficulty = "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        Recipe.difficulty = "Hard"
    else:
        print("Something went wrong")
    print("Difficulty lever: ", Recipe.difficulty)
    return Recipe.difficulty

def return_ingredients_as_list():
    recipes = session.query("Recipe").all()
    if len(recipes) == 0:
        return []
    else:
        return list(Recipe.ingredients.split(" ,"))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Part 3
def create_recipe():
    print("="*30)
    print("Create a recipe!")
    valid_name = False
    while valid_name == False:
        name = input("Enter the name of the recipe: ")
        if len(name) < 50 and name.isalpha() == True:
            valid_name = True
        else:
            print("The name should be less than 50 characters. Try again")
    
    recipe_ingredients = []
    ingredients_valid_number = False

    while ingredients_valid_number == False:
        ingredients_amount = input("How many ingredients does the recipe have? ")

        if ingredients_amount.isnumeric():
            ingredients_valid_number = True
            for i in range(int(ingredients_amount)):
                ingredient = input("Enter an ingredient: ")
                recipe_ingredients.append(ingredient)
        else:
            ingredients_valid_number = False
            print("Please enter a valid number")

    recipe_ingredients_str = ", ".join(recipe_ingredients)
    print(recipe_ingredients_str)

    cooking_time_valid = False
    while cooking_time_valid == False:
        cooking_time = input("Enter cooking duration in minutes: ")
        if cooking_time.isnumeric() == True:
            cooking_time_valid = True
        else:
            print("Please enter valid duration")
    
    difficulty = calculate_difficulty(int(cooking_time), recipe_ingredients)

    recipe_entry = Recipe(
        name = name,
        cooking_time = int(cooking_time),
        ingredients = recipe_ingredients_str,
        difficulty = difficulty
    )

    print(recipe_entry)

    session.add(recipe_entry)
    session.commit()
    print("Recipe is added to the database")

def view_all_recipes():
    print("="*30)
    print("View all recipes!")
    recipes = session.query(Recipe).all()
    if len(recipes) == 0:
        print("There are no recipes added yet")
        return None
    else:
        for recipe in recipes:
            print(recipe)

def search_by_ingredient():
    print("="*30)
    print("Search a recipe by ingredient!")
    recipe_amount = session.query(Recipe).count()
    if recipe_amount == 0:
        print("There are no recipes added yet")
        return None
    
    #Retrieve only the values from the ingredients column and store them into results
    results = session.query(Recipe.ingredients).all()

    all_ingredients = []

    for recipe in results:
        ingredients = recipe[0].split(", ")
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    #Display the ingredients to the user, where each ingredient has an index
    print("These are all ingredients: ")
    display_ingredients = list(enumerate(all_ingredients, 1))
    for ingredient in display_ingredients:
        print(str(ingredient[0]) + ". " + ingredient[1])

    #Ask the user to choose an ingredient by its index
    try:
        ask_ingredient = int(input("Enter the number of the ingredient: "))
        search_ingredient = all_ingredients[ask_ingredient - 1]
        print(search_ingredient.capitalize(), "is used in the following recipe(s): ")
    except:
        print("Invalid number")
    else:
        conditions = []
        for ingredient in search_ingredient:
            like_term = "%" + ingredient + "%"
            conditions.append(Recipe.ingredients.like(like_term))
        searched_recipes = session.query(Recipe).filter(*conditions).all()
        for recipe in searched_recipes:
            print(recipe)

def edit_recipe():
    print("="*30)
    print("Update a recipe!")

    if session.query(Recipe).count() == 0:
        print("There are no recipes added yet")
        return None
    else:
        results = session.query(Recipe.id, Recipe.name).all()
        print("Your recipes:")
        for result in results:
            print("\tRecipe ID:", result[0])
            print("\tRecipe Name:", result[1])

        try:
            selected_id = int(input("Enter the ID of the Recipe you want to edit: "))
            recipe_to_edit = session.query(Recipe).filter(Recipe.id == int(selected_id)).one()
            print("You want to edit the following recipe:")
            print("\tName: " + recipe_to_edit.name)
            print("\tIngredients: " + recipe_to_edit.ingredients)
            print("\tCooking Time: " + str(recipe_to_edit.cooking_time) + " minutes")
        except:
            print("ID not valid")
        else:
            edit_recipe_attr = input("Choose what you want to edit: N for Name, CT for Cooking Time, I for ingredients: ").upper()
            if edit_recipe_attr == "N":
                new_name = input("Enter a new name: ")
                if len(new_name) < 50:
                    recipe_to_edit.name = new_name
                    session.commit()
                    print("Recipe\'s name has been updated: ", recipe_to_edit.name)
                else:
                    print("Recipe Name exceeds 50 characters. Try again")
            elif edit_recipe_attr == "CT":
                new_time = input("Enter new cooking duration (in minutes): ")
                if new_time.isnumeric():
                    recipe_to_edit.cooking_time = new_time
                    new_difficulty = calculate_difficulty(int(new_time), list(recipe_to_edit.ingredients.lower().split(", ")))
                    recipe_to_edit.difficulty = new_difficulty
                    print("Recipe\s cooking duration has been updated: ", recipe_to_edit.cooking_time)
                else:
                    print("Input not valid. Please enter a valid number")
            elif edit_recipe_attr == "I":
                new_ingredients = input("Enter new ingredients, separated by comma: ")
                if len(new_ingredients) < 225:
                    new_ingredients_list = list(new_ingredients.split(", "))
                    new_difficulty = calculate_difficulty(recipe_to_edit.cooking_time, new_ingredients_list)
                    recipe_to_edit.ingredients = new_ingredients
                    recipe_to_edit.difficulty = new_difficulty
                    session.commit()
                    print("Recipe\'s ingredients have been updated: ", recipe_to_edit.ingredients)
                else:
                    print("Invalid input. Try again")
            else:
                print("Invalid input. Please choose among N, CT, I")
def delete_recipe():
    print("="*30)
    print("Delete a recipe!")

    if session.query(Recipe).count() == 0:
        print("There are no recipes added yet")
        return None
    else:
        results = session.query(Recipe.id, Recipe.name).all()
        print("Your recipes:")
        for result in results:
            print("\tRecipe ID:", result[0])
            print("\tRecipe Name:", result[1])
        try:
            selected_id = int(input("Enter the ID of the Recipe you want to delete: "))
            recipe_to_delete = session.query(Recipe).filter(Recipe.id == int(selected_id)).one()
            print("You want to delete the following recipe:")
            print("\tName: " + recipe_to_delete.name)
            print("\tIngredients: " + recipe_to_delete.ingredients)
            print("\tCooking Time: " + str(recipe_to_delete.cooking_time))
        except:
            print("ID not valid")
        else:
            confirmation = input("Are you sure you want to delete this recipe? (Y/N): ").upper()
            if confirmation == "Y":
                session.delete(recipe_to_delete)
                session.commit()
                print("The recipe" + recipe_to_delete.name + "has been deleted" )
            elif confirmation == "N":
                print("Returning to the main menu")
                return None
            else:
                print("Invalid input. Please choose between Y or N")
            

def main_menu():
    choice = ""
    while choice!="quit":
        print("Main Menu")
        print("==============================")
        print("Pick an option:")
        print("     1. View all recipes")
        print("     1. Create a new recipe")
        print("     2. Search for a recipe by ingredient")
        print("     3. Update an existing recipe")
        print("     4. Delete a recipe")
        print("Type \'quit\' to exit options: ")

        choice = input("Your choice: ")
        if choice == "1":
            view_all_recipes()
        elif choice == "2":
            create_recipe()
        elif choice == "3":
            search_by_ingredient()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        else:
            print("Bye")

main_menu()
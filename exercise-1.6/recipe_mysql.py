import mysql.connector

conn = mysql.connector.connect(
    host="localhost", 
    user="cf-python", 
    password="password")
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    ingredients VARCHAR(225),
    cooking_time INT,
    difficulty VARCHAR(20)
)''')

cursor.execute("ALTER TABLE Recipes MODIFY COLUMN id INT AUTO_INCREMENT")

def main_menu(conn, cursor):
    choice = ""
    while choice!="quit":
        print("Main Menu")
        print("==============================")
        print("Pick an option:")
        print("     1. Create a new recipe")
        print("     2. Search for a recipe by ingredient")
        print("     3. Update an existing recipe")
        print("     4. Delete a recipe")
        print("Type \'quit\' to exit options: ")

        choice = input("Your choice: ")
        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        else:
            print("Bye")

def create_recipe(conn, cursor):
    print("----------------------")
    print("Create new recipe")
    print("To create new recipe, please enter the following: ")
    name = input("Name: ")
    cooking_time = int(input("Cooking time in minutes: "))
    ingredients = input("Ingredients separated by comma: ")
    ingredients_list = list(ingredients.lower().split(", "))
    difficulty = calculate_difficulty(cooking_time, ingredients_list)

    sql = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, ingredients, cooking_time, difficulty)
    cursor.execute(sql, val)
    conn.commit()
    print("The recipe is added to the database")
    view_recipes(conn, cursor)

def calculate_difficulty(cooking_time, recipe_ingredients):
    if cooking_time < 10 and len(recipe_ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(recipe_ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(recipe_ingredients) < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and len(recipe_ingredients) >= 4:
        difficulty = "Hard"
    print("Difficulty lever: ", difficulty)
    return difficulty


def search_recipe(conn, cursor):
    print("----------------------")
    print("Search a recipe")
    all_ingredients = []

    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    for recipe in results:
        ingredients = recipe[0].split(", ")
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    print("Take a look at all the ingredients: ")

    display_ingredients = list(enumerate(all_ingredients, 1))
    for ingredient in display_ingredients:
        print(str(ingredient[0]) + ". " + ingredient[1])

    try:
        ask_ingredient = int(input("Select a number of an ingredient: "))
        search_ingredient = all_ingredients[ask_ingredient - 1]
        print(search_ingredient.capitalize(), "is used in this recipe(s): ")
    except:
        print("Invalid number")
    else:
        cursor.execute("SELECT name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE %s", ("%" + search_ingredient + "%", ))
        search_results = cursor.fetchall()
        for row in search_results:
            print("Name: ", row[0])
            print("Ingredients: ", row[1])
            print("Cooking Time: ", row[2], " minutes")
            print("Difficulty: ", row[3])


def update_recipe(conn, cursor):
    print("----------------------")
    print("Update a recipe")
    view_recipes(conn, cursor)
    selected_recipe = input("Select a Recipe\'s ID you want to update: ")
    selected_column = input("Select the column you want to update (type N for Name, CT for Cooking Time, I for ingredients): ").upper()

    if selected_column == "N":
        new_name = input("New name: ")
        cursor.execute("UPDATE Recipes SET name = %s WHERE id=%s", (new_name, selected_recipe))
        print("The name of the recipe has been updated")
    
    elif selected_column == "CT":
        new_time = int(input("Enter new cooking duration (in minutes): "))
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id=%s", (new_time, selected_recipe))
    # updating the difficulty
        cursor.execute("SELECT ingredients FROM Recipes WHERE  id = %s", (selected_recipe, ))
        results = cursor.fetchall()
        ingredients = results[0][0]
        ingredients_list = list(ingredients.split(", "))
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id=%s", (calculate_difficulty(new_time, ingredients_list), selected_recipe))
        print("Your recipe\'s cooking time and difficulty have been updated")
    
    elif selected_column == "I":
        new_ingredients = input("Enter new ingredients: ")
        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (new_ingredients, selected_recipe))
        #updating difficulty
        cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (selected_recipe, ))
        results = cursor.fetchall()
        cooking_time = results[0][0]
        new_ingredients_list = list(new_ingredients.lower().split(", "))
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (calculate_difficulty(cooking_time, new_ingredients_list), selected_recipe))
        print("Your recipe\'s ingredients and difficulty have been updated")

    conn.commit()
    print("Changes are saved")

def delete_recipe(conn, cursor):
    print("----------------------")
    print("Delete a recipe")
    view_recipes(conn, cursor)
    selected_recipe = input("Choose the ID of the recipe you want to delete: ")
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (selected_recipe, ))
    conn.commit()
    print("Recipe deleted")

def view_recipes(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()
    print("Your recipes: ")
    for row in results:
        print("ID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking Time: ", row[3])
        print("Difficulty: ", row[4])


main_menu(conn, cursor)
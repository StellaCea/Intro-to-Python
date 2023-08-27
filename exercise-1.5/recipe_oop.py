class Recipe(object):

    all_ingredients = []

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None
    
    def set_name(self, name):
        self.name = name
    
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    def add_ingredients(self, *args):
        self.ingredients = args
        Recipe.update_all_ingredients(self)
    
    def get_name(self):
        return self.name
    
    def get_ingredients(self):
        return self.ingredients
    
    def calculate_difficulty(self, cooking_time, ingredients):
        if cooking_time < 10 and len(ingredients) < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and len(ingredients) >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and len(ingredients) < 4:
            difficulty = "Intermediate"
        elif cooking_time >= 10 and len(ingredients) >= 4:
            difficulty = "Hard"
        self.difficulty = difficulty
    
    def get_difficulty(self):
        if self.difficulty:
            return self.difficulty
        else:
            self.calculate_difficulty(self.cooking_time, self.ingredients)
    
    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return True
        else: 
            return False
        
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if not ingredient in self.all_ingredients:
                self.all_ingredients.append(ingredient)
    
    def __str__(self):
        output = "Recipe's name: " + str(self.name) + "\nCooking Time: " + str(self.cooking_time) + " minutes" + "\nList of ingredients: " + str(self.ingredients) + "\nDifficulty: " + str(self.difficulty)
        return output
    
def recipe_search(data, search_item):
    print("-----------------------------------------------")
    print("The recipe that includes " + search_item + ": ")
    for recipe in data:
        if recipe.search_ingredient(search_item):
            print(recipe)

tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)
tea.get_difficulty()
print(tea)

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
coffee.get_difficulty()
print(coffee)

cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)
cake.get_difficulty()
print(cake)

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)
banana_smoothie.get_difficulty()
print(banana_smoothie)

recipe_list = [tea, coffee, cake, banana_smoothie]
recipe_search(recipe_list, "Water")
recipe_search(recipe_list, "Sugar")
recipe_search(recipe_list, "Bananas")
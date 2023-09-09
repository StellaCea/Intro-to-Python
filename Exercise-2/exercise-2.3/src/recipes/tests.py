from django.test import TestCase
from .models import Recipes

# Create your tests here.
class RecipeModelTest(TestCase):
    def setUpTestData():
        Recipes.objects.create(name="Tea", cooking_time="5", ingredients=["water", "tea leaves", "sugar"], difficulty="easy")

    def test_recipe_name(self):
        recipe = Recipes.objects.get(id=1)
        field_label = recipe._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")
    
    def test_cooking_time_integer(self):
        recipe = Recipes.objects.get(id=1)
        self.assertIsInstance(recipe.cooking_time, float)


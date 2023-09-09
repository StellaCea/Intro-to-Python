from django.db import models

# Create your models here.
class Recipes(models.Model):
    name = models.CharField(max_length=120)
    cooking_time = models.FloatField()
    ingredients = models.TextField()
    difficulty = models.CharField(max_length=120)

    def __str__(self):
        return str(self.name)
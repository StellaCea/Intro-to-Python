from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=120, unique=True)
    name = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    bio = models.TextField()

    def __str__(self):
        return str(self.username)
    
    
    # Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    #... add more

    def __str__(self):
        return self.username

class Movie (models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    #... add more

    def __str__(self):  
        return self.title
    
# maybe Rating, Watchlist... , Reccomendation 

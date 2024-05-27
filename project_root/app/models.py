from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Restaurant(models.Model):
    name = models.CharField(max_length=100)

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items = models.JSONField()
    menu_date = models.DateField()

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from authentication.models import User


class Product(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()

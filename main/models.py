from django.db import models

# Create your models here.

class Product(models.Model):
    tittle = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.tittle

from django.db import models

# Create your models here.

class Category(models.Model):
   name = models.CharField(max_length=200)
   
   def __str__(self) -> str:
      return self.name


class Product(models.Model):
   
   product_name =  models.CharField(max_length=200)
   category  = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
   price = models.FloatField()
   image = models.ImageField()
   
   def __str__(self) -> str:
      return self.product_name
   

    


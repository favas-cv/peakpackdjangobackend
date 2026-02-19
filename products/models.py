from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20,unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    



class ProductsModel(models.Model):
    
    SEASON_CHOICES = [
        ('WINTER','WINTER'),
        ('SUMMER','SUMMER'),
        ('RAINY','RAINY'),
    ]
    
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    season = models.CharField(max_length=15,choices=SEASON_CHOICES)
    price = models.PositiveIntegerField()
    image_url = models.URLField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

from django.db import models
from products.models import ProductsModel
from accounts.models import User

class BagModel(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='bagitems')
    product = models.ForeignKey(ProductsModel,on_delete=models.CASCADE,related_name='bagproducts')
    quantity = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('user','product')
        ordering = ['id']
    
    
    def __str__(self):
        return self.product.name


class FavoritesModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='favoriteitems')
    product = models.ForeignKey(ProductsModel,on_delete=models.CASCADE,related_name='favoriteproducts')
    #in here related name uses when we wantr to check  how many user favorites this [roducts so for realproject gave user
    # favorites liek that ]
    
    
    class Meta:
        unique_together = ('user','product')
    
    def __str__(self): 
        return self.product.name
 
    
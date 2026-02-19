from django.db import models
from address.models import AddressModel
from products.models import ProductsModel
# Create your models here.
from accounts.models import User


class OrdersModel(models.Model):
    

    
    STATUS_CHOICES = [
        ('PENDING','PENDING'),
        ('DELIVERED','DELIVERED'),
        ('SHIPPED','SHIPPED'),
        ('OUT OF DELIVERY','OUT OF DELIVERY'),
        ('CANCELLED','CANCELLED'),
    ]
    
    user =models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    address = models.ForeignKey(AddressModel,on_delete=models.CASCADE)
    
    subtotal = models.PositiveBigIntegerField()
    delivery = models.PositiveIntegerField()
    total = models.PositiveBigIntegerField()
    paymentmethod = models.CharField(max_length=20)
    status = models.CharField(max_length=25,choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username 
    
    
    
class OrderItemsModel(models.Model):
    
    order = models.ForeignKey(OrdersModel,on_delete=models.CASCADE,related_name='items')
    
    product = models.ForeignKey(ProductsModel,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_time_price = models.PositiveBigIntegerField()
    # price for the price when ordeing , if that change in here not change so , safety 
    
    class Meta:
        unique_together =('order','product')
    
    
    def __str__(self):
        return self.product.name 
    


from django.db import models
from accounts.models import User
# Create your models here.


class AddressModel(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses')
    streetAddress = models.CharField(max_length=50)
    city = models.CharField(max_length=10)
    pincode = models.PositiveBigIntegerField()
    landmark = models.CharField(max_length=50)
    phone = models.PositiveBigIntegerField()
    

    

    
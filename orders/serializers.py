from rest_framework import serializers
from .models import OrderItemsModel,OrdersModel
from accounts.serializers import UserSerializer
from address.serializers import AddressSerializer
from products.serializers import ProductsSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    
    product = ProductsSerializer()
    
    class Meta:
        model = OrderItemsModel
        # fields = ['id','order','product','quantity','order_time_price']
        fields = '__all__'
        

class OrdersSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only = True)
    address = AddressSerializer(read_only =True)
    items = OrderItemSerializer(many=True,read_only =True)
    
    class Meta:
        model = OrdersModel
 
        fields = '__all__'
 
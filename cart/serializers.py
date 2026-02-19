from rest_framework import serializers
from .models import BagModel,FavoritesModel
from products.serializers import ProductsSerializer


class BagSerializer(serializers.ModelSerializer):
    product = ProductsSerializer()
    
    class Meta:
        model = BagModel
        fields = '__all__'
        
    def validate_quantity(self,value):
        if value <= 0 :
            raise serializers.ValidationError("The Quantity Must Be More Than 1")
        
        
class FavoritesSerializer(serializers.ModelSerializer):
    product=ProductsSerializer()
    class Meta:
        model = FavoritesModel
        fields = '__all__'
        

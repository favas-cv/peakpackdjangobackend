from rest_framework import serializers
from .models import AddressModel

class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AddressModel
        fields = [
            "id",
            "streetAddress",
            "city",
            "pincode",
            "landmark",
            "phone",
        ]
        read_only_fields = ["id"] 
        
        
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate 


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True,min_length = 8)
    password2 = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ['username','email','password','password2']
        
    def validate(self,data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password2":"The Password Is Not Same "})
        return data
        
    def create(self,data):
        data.pop('password2')
        return User.objects.create_user(**data)
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)
    
    def validate(self,data):
        
        username = data.get('username')  
        password = data.get('password')  
        
        user = authenticate(username = username, password = password)
        
        if not user:
            raise serializers.ValidationError({"detail":"Invalid username or password "})
        
        data['user'] = user
        return data 
    
#for profile 
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id','username','email','is_staff'] 
        
        
        
class UserListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model =User
        fields = ['id','username','email','date_joined','is_active','is_staff']
        read_only_fields = ['id','username','date_joined']
        
        
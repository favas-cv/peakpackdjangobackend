from rest_framework import serializers 
from .models import ProductsModel,Category
from rest_framework.response import Response
import cloudinary.uploader

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only = True,required= False)
    category = CategorySerializer(read_only = True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(),
        source ='category',
        write_only =True
    )
    
    class Meta:
        model = ProductsModel
        fields = '__all__'
        read_only_fields = ['image_url']#this is giving for the imageurl cant give by the user auto
        #only it happeing in bckend auto convert this  from file to url 
        #so when need bulk updae comment this !
        
        
    def create(self,vdata):#using for when image is not in model so it will overide so we want to pop 
        image_file = vdata.pop('image',None)
        
        image_url =  None
        if image_file:
            upload_file =cloudinary.uploader.upload(
                image_file,
                folder='products'
            )
            image_url = upload_file.get('secure_url')
        vdata['image_url'] = image_url
        return ProductsModel.objects.create(**vdata)
    
    def validate_name(self,value):
        if len(value) < 3 :
            raise serializers.ValidationError("The Product Name Want Minimum 3 Characters")
        return value
    
    
        
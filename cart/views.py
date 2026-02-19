from django.shortcuts import render
from .serializers import BagSerializer,FavoritesSerializer
from rest_framework.views import APIView
from .models import BagModel,FavoritesModel
from rest_framework.response import Response
from rest_framework import status
from products.models import ProductsModel

from rest_framework.permissions import IsAuthenticated,AllowAny

class BagApiView(APIView):
    
    def get(self,req):
        products = BagModel.objects.filter(user=req.user).select_related('product')
            

        serializer = BagSerializer(products,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,req):
        
        product_id =req.data.get('product_id')
        
        product = ProductsModel.objects.get(id=product_id)
        
        bag_item,created = BagModel.objects.get_or_create(
            user=req.user,
            product=product,
            defaults={"quantity":1}
        )
        
        if not created:
            return Response(
                {"msg":"The item is already in bag"},
                status=status.HTTP_200_OK
                
            )
         
            
        return Response(
            {"msg":"product added to bag",
             "quantity":bag_item.quantity},
            status=status.HTTP_200_OK
        )
        
    def delete(self,req):
        
        product_id = req.data.get('product_id')
        
        bag_item = BagModel.objects.get(
            user=req.user,
            product_id =product_id
        )
        if not bag_item:
            return Response(
                {"msg":"the item not in yout bag"}
            )
        bag_item.delete()
        return Response(
            {"msg":"the item was deleted"},
            status=status.HTTP_200_OK
        )
        
        
        
 
    
class IncreaseBagQuantityApiView(APIView):
    
    def post(self,req,pk):
        bag_item = BagModel.objects.get(
            user=req.user,
            product_id = pk
        )    
        
        bag_item.quantity+=1
        bag_item.save()
        
        return Response(
            {
            "quantity":bag_item.quantity
            },
            status=status.HTTP_200_OK           
        )

class DecreaseBagQuantityApiView(APIView):
    
    
    def post(self,req,pk):
        
        bag_item = BagModel.objects.get(
            user=req.user,
            product_id = pk
        )
        
        bag_item.quantity -=1
        if bag_item.quantity <= 0:
            bag_item.delete()
            return Response({"msg":"item is removed from bag"},
                            status=status.HTTP_200_OK
                            )
        bag_item.save()
        
        return Response(
            {"quantity":bag_item.quantity},
            status=status.HTTP_200_OK
        )
            
            


    
class FavoritesApiView(APIView):
    
    
    
    def get(self,req):
        
        products = FavoritesModel.objects.filter(user=req.user).select_related('product')
            

        serializer = FavoritesSerializer(products,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,req):
        
        product_id = req.data.get("product_id")
        
        if not product_id:
            return Response(
                {"msg":"the item not found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        favorite_item,created = FavoritesModel.objects.get_or_create(
            user=req.user,
            product_id=product_id
        )
        
        if not created:
            return Response(
                {"msg":"the item is already in"},
                status=status.HTTP_200_OK
            )
            
        return Response(
            {"msg":"Added succesfulyy"}
            ,status=status.HTTP_200_OK
        )
        
    def delete(self, request, product_id=None):
        
        
        if product_id is None:
            FavoritesModel.objects.filter(
                user=request.user
            ).delete()
            
            return Response(
                {"msg":"the items are deleted"},
                status=status.HTTP_200_OK
            )
        
        
        try:
            favorite = FavoritesModel.objects.get(
            user=request.user,
            product_id=product_id
        )
            favorite.delete()
            return Response(
                {"msg": "Item deleted successfully"},
                status=status.HTTP_200_OK
            )
        except FavoritesModel.DoesNotExist:
            return Response(
            {"error": "Item not found"},
            status=status.HTTP_404_NOT_FOUND
        )

        

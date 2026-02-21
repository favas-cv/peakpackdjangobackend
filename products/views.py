from django.shortcuts import render
from .serializers import ProductsSerializer,CategorySerializer
from .models import ProductsModel,Category
# Create your views here.
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny

# class Products(ModelViewSet):
    
     
#     permission_classes = [AllowAny]
    
    
#     queryset = ProductsModel.objects.all()
#     serializer_class = ProductsSerializer
    
    
from .pagination import Pagination 
import cloudinary.uploader
    
class ProductsApiView(APIView):
    
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser,FormParser,JSONParser]
    
  
    def get(self,req):
        
        
        
        products = ProductsModel.objects.all().order_by('-id')
        
        # if not products.exists():
        #     return Response({"error":"Products not Exist"})

        
        category = req.GET.get('category') #from url parameter
        if category and category != "All":
            products = products.filter(category__name__iexact=category.strip())

        season = req.GET.get('season')
        if season and season != "All":
            products = products.filter(season__iexact=season.strip())

        search = req.GET.get('search')
        if search:
            products = products.filter(name__icontains=search)

        allowed_ordering = ['price', '-price', 'name', '-name']
        ordering = req.GET.get('ordering')
        if ordering in allowed_ordering:
            products=products.order_by(ordering)
    
        
        paginator = Pagination()
        
        
        page = paginator.paginate_queryset(products,req)
        
        if page is not None:
            serializer = ProductsSerializer(page,many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = ProductsSerializer(products,many =True)
        return Response(serializer.data)
    
#    only for admin jsut remind 
 
    def post(self,req):
        
        serializer = ProductsSerializer(data=req.data) #many=true for bulk update 
        #when add images dont give bcz it will change to error 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
class ProductDetailApiView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self,req,pk):
        
        try:
            product = ProductsModel.objects.get(pk=pk)
        except ProductsModel.DoesNotFound:
            raise Response({"errors":"The Product Does Not Found"})
        
        serializer = ProductsSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # for adminsection
    # for adminsection
    
    
    
class CategoryApiView(APIView):
    permission_classes=[AllowAny]
    
    def get(self,req):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,req):
        serializer = CategorySerializer(data= req.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    


class ProductAdminView(APIView):
    permission_classes = [AllowAny]
    
    def get(self,req,pk=None):
        
        if pk:
            try:
                product = ProductsModel.objects.get(pk=pk)
            except ProductsModel.DoesNotExist:
                return Response({"error":"the Prodcut Not found"})
            serializer=ProductsSerializer(product)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        products = ProductsModel.objects.all().order_by("-id")
        paginator = Pagination()
        page = paginator.paginate_queryset(products,req)
        serializer = ProductsSerializer(page,many=True)
        
   
        return paginator.get_paginated_response(serializer.data)
    
    
    
    def post(self,req):
        
        serializer = ProductsSerializer(data=req.data) #many=true for bulk update 
        #when add images dont give bcz it will change to error 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    
    def patch(self,req,pk):
        try:
            product = ProductsModel.objects.get(pk=pk)
        except ProductsModel.DoesNotExist:
            return Response({"errors":"The Product Does Not Found"})
        
        serializer = ProductsSerializer(product,data=req.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors)
    
    def delete(self,req,pk):
        try:
            product = ProductsModel.objects.get(pk=pk)


        except ProductsModel.DoesNotExist:
            return Response({"errors":"The Product Does Not Found"})
        product.delete()
        return Response({"msg":"The Product Was Deleted"},status=status.HTTP_200_OK)
        
from django.db.models import Count

class AdminDashboardProduct(APIView):
    permission_classes = [AllowAny]
    
    def get(self,req):
        count = ProductsModel.objects.count()
        categorybycount = (
            ProductsModel.objects.values('category__name')
            .annotate(total=Count('id')).order_by('-total')
        )
        return Response({
            "total_products":count,
            "category_data":categorybycount
        })
        
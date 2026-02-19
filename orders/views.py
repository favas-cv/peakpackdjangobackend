from django.shortcuts import render
from .models import OrderItemsModel,OrdersModel
from .serializers import OrderItemSerializer,OrdersSerializer


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.db import transaction
from cart.models import BagModel


class CreateOrderApiView(APIView):
    
    
    @transaction.atomic
    def post(self,req):
        
        user = req.user
        address_id = req.data.get('address_id')
        paymentmethod = req.data.get('paymentmethod')
        
        # status = req.data.get('status')
        
        cart_items = BagModel.objects.filter(user=user).select_related('product')
        
        if not cart_items.exists():
            return Response({"error":"The Bag Was Empty"})
        
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
    
        delivery = 40 if subtotal < 500 else 0

            
        total = subtotal+delivery
        
        order = OrdersModel.objects.create(
            user=user,
            address_id = address_id,
            subtotal = subtotal,
            delivery=delivery,
            total=total,
            paymentmethod=paymentmethod,
            status='PENDING'
            
        )
        
        for item in cart_items:
            
            OrderItemsModel.objects.create(
                order = order,
                product = item.product,
                quantity = item.quantity,
                order_time_price =item.product.price
            )
            
        cart_items.delete()
        
        serializer = OrdersSerializer(order)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        
            




from products.pagination import Pagination

class UserOrdersApiview(APIView):
    
    def get(self,req):
        
        orders = OrdersModel.objects.filter(user=req.user
                                            ).select_related(
                                            'address'
                                            ).prefetch_related(
                                            'items__product'
                                            ).order_by('id')
                                            
        paginator = Pagination() 
        page = paginator.paginate_queryset(orders,req)
        serializer = OrdersSerializer(page,many = True)
        return paginator.get_paginated_response(serializer.data)
    

class OrderDetailedApiView(APIView):
    
    
    def get(self,req,pk):
        
        try:
            
            order = OrdersModel.objects.select_related(
                'address'
                ).prefetch_related('items__product').get(pk=pk)
        except OrdersModel.DoesNotExist:
            return Response(
                {"error":"order not found "}
            )
        serializer = OrdersSerializer(order)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    
    
# from products.serializers import ProductsSerializer

class Orderitems(APIView):
    
    
    def get(self,req,pk):
        items = OrderItemsModel.objects.filter(order=pk).select_related('product')
        serializer = OrderItemSerializer(items ,many = True)
        
        return Response(serializer.data)



# //admin side module
# //admin side module
from rest_framework.pagination import PageNumberPagination

class UserOrdersAdminview(APIView):
    permission_classes = [AllowAny]
    
    def get(self,req,pk=None):
        
        if pk == None:
            
            orders = OrdersModel.objects.all().select_related(
                                            'address'
                                            ).prefetch_related(
                                            'items__product'
                                            ).order_by('-id')
                                            
            paginator = PageNumberPagination()
            paginator.page_size = 4
            page = paginator.paginate_queryset(orders,req)
            serializer = OrdersSerializer(page,many = True)
            return paginator.get_paginated_response(serializer.data)
        
        
        order = OrdersModel.objects.get(pk=pk)
        
        serializer = OrdersSerializer(order)
        return Response(serializer.data)
        
    
    def patch(self,req,pk):
        try:
            
            order = OrdersModel.objects.get(pk=pk)
        except OrdersModel.DoesNotExist:
            return Response({"error":"Order Not found"})
        
        serializer = OrdersSerializer(order,data=req.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
from django.db.models import Sum
    
class AdmindashboardOrders(APIView):
    permission_classes =[AllowAny]
    
    def get(self,req):
        count = OrdersModel.objects.count()
        revenuebydate = (
            OrdersModel.objects.values("created_at")
            .annotate(totalbydate = Sum('total')).order_by("-totalbydate")
        )
        total = OrdersModel.objects.aggregate(t=Sum('total'))
        
        return Response({
            "totalorder":count,
            "revenuedata":revenuebydate,
            "totalrevenue":total
        })
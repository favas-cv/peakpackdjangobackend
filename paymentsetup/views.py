from django.shortcuts import render
import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated


class CreateRazorpayOrder(APIView):
    
    
    def post(self,req):
        
        client = razorpay.Client(
            auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET)
        )
        cart_items = BagModel.objects.filter(user=req.user)
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        delivery = 40 if subtotal < 500 else 0
        total = delivery+subtotal
        amount = total * 100
        razorpay_order = client.order.create({
            "amount":amount,
            "currency":"INR",
            "payment_capture":1
        })
        return Response(
            {
                "order_id":razorpay_order['id'],
                "amount":razorpay_order['amount'],
                "key":settings.RAZORPAY_KEY_ID
            }
        )



from orders.models import OrderItemsModel,OrdersModel
from cart.models import BagModel

class VerifyPayment(APIView):
    
    def post(self,req):
        
        client = razorpay.Client(
            auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET)
        )
        
        razorpay_payment_id = req.data.get('razorpay_payment_id')
        razorpay_order_id = req.data.get('razorpay_order_id')
        razorpay_signature = req.data.get('razorpay_signature')
        address_id = req.data.get('address_id')
        
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id':razorpay_order_id,
                'razorpay_payment_id':razorpay_payment_id,
                'razorpay_signature':razorpay_signature
            })
        except:
            return Response({"error":"Payment Verification is Failed"},status=400)
        
        
        payment = client.payment.fetch(razorpay_payment_id)
        method_used = payment['method'].upper()
        
        # bag_items = BagModel.objects.filter(user=req.user)
        
         
        cart_items = BagModel.objects.filter(user=req.user).select_related('product')
        
        if not cart_items.exists():
            return Response({"error":"The Bag Was Empty"})
        
        subtotal = sum(
            item.product.price * item.quantity for item in cart_items
        )
        
            
        delivery = 40 if subtotal < 500 else 0
        
        
        total = subtotal+delivery
        
        order = OrdersModel.objects.create(
            user=req.user,
            address_id = address_id,
            subtotal = subtotal,
            delivery=delivery,
            total=total,
            paymentmethod=method_used,
            status='PENDING'
            
        )
        
        for item in cart_items:
            OrderItemsModel.objects.create(
                order =order,
                product=item.product,
                quantity = item.quantity,
                order_time_price = item.product.price
            )
            
        cart_items.delete()
        return Response({"msg":"Payment VErid=fiend & order Created"})
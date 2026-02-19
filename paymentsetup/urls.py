from .views import CreateRazorpayOrder,VerifyPayment

from django.urls import path

urlpatterns = [
    path('/create-razorpay-order/',CreateRazorpayOrder.as_view()),
    path('/verify-payment/',VerifyPayment.as_view()),
]

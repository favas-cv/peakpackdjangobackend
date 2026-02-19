from django.urls import path
from .views import (CreateOrderApiView,UserOrdersApiview,
                    OrderDetailedApiView,Orderitems,
                    UserOrdersAdminview,AdmindashboardOrders
                    )

urlpatterns = [
    path('/create/',CreateOrderApiView.as_view()),
    path('/userorder/',UserOrdersApiview.as_view()),
    path('/detailed/<int:pk>/',OrderDetailedApiView.as_view()),
    path('/items/<int:pk>/',Orderitems.as_view()),
    #adminsection
    path('/admin/orders/',UserOrdersAdminview.as_view()),
    path('/admin/order/<int:pk>/',UserOrdersAdminview.as_view()),
    path('/admin/dashboard/',AdmindashboardOrders.as_view()),
    
]
 
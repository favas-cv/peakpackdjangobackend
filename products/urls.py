from django.urls import path
from .views import (
    ProductsApiView,
    ProductDetailApiView,
    ProductAdminView,
    CategoryApiView,
    AdminDashboardProduct
)
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('items',Products)

urlpatterns = [
    path('', ProductsApiView.as_view()),
    path('<int:pk>/', ProductDetailApiView.as_view()),
    # admin
    # admin
    path('admin/products/',ProductAdminView.as_view()),
    path('admin/product/<int:pk>/',ProductAdminView.as_view()),
    path('admin/category/',CategoryApiView.as_view()),
    path('admin/dashboard/',AdminDashboardProduct.as_view()),
]

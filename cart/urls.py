from django.urls import path
from .views import (
                    BagApiView,FavoritesApiView,
                    IncreaseBagQuantityApiView,
                    DecreaseBagQuantityApiView,
                    )

urlpatterns = [
    path('bag/',BagApiView.as_view()),
    path('favorites/',FavoritesApiView.as_view()),
    path('favorites/<int:product_id>/',FavoritesApiView.as_view()),
    path('bag/increase/<int:pk>/',IncreaseBagQuantityApiView.as_view()),
    path('bag/decrease/<int:pk>/',DecreaseBagQuantityApiView.as_view()),
]

from django.urls import path

from .views import AddressListView,AddressDetailView

urlpatterns = [
    path('/',AddressListView.as_view()),
    path('/<int:pk>/',AddressDetailView.as_view()),
]

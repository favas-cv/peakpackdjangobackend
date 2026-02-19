from django.urls import path
from .views import LoginApiView,LogoutApiView,RegisterApiView,RefreshApiView,UsersListApiView,ProfileApiView
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('login/',LoginApiView.as_view()),
    path('refresh/',RefreshApiView.as_view()),
    path('logout/',LogoutApiView.as_view()),
    path('register/',RegisterApiView.as_view()),
    path('userslist/',UsersListApiView.as_view()),
    path('userslist/<int:pk>/',UsersListApiView.as_view()),
    path('profile/',ProfileApiView.as_view()),
]

from django.shortcuts import render
from .serializers import RegisterSerializer,LoginSerializer,UserListSerializer,UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import token_blacklist
from rest_framework_simplejwt.exceptions import TokenError
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from .models import User


class RegisterApiView(APIView):
    permission_classes = [AllowAny]
    
    
    def post(self,req):
        serializer = RegisterSerializer(data= req.data)
        if serializer.is_valid():
            user =  serializer.save()
            return Response({"msg":"The User Was Registered Successfully"},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
        
 


class LoginApiView(APIView):
    permission_classes = [AllowAny]
    
    
    def post(self,req):
        serializer = LoginSerializer(data=req.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
        
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            response = Response({
                "access":access_token,
                "user":{
                    "id":user.id,
                    "username":user.username,
                    "is_staff":user.is_staff
                }
            },status=status.HTTP_201_CREATED)
            
            response.set_cookie(  #inhere the responseobject contian headers this include 
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True, #change to true when the production time
                samesite='None',
                path='/'
                
            )
            
            return response
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class RefreshApiView(APIView):
    permission_classes = [AllowAny]
    

    def post(self, req):
        print("HEADERS:", req.headers)
        print("COOKIES:", req.COOKIES)

        refresh_token = req.COOKIES.get('refresh_token')
        print(refresh_token)

        if not refresh_token:
            return Response(
                {"error": "No refresh Token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken(refresh_token)
        new_access = str(refresh.access_token)
        return Response({"access": new_access})



class LogoutApiView(APIView):
    
    
    def post(self,req):
        try:
            refresh_token = req.COOKIES.get('refresh_token')
            if refresh_token:
                
                token = RefreshToken(refresh_token)
                token.blacklist()
                response = Response({"msg":"LogOut Successfull"},status=status.HTTP_200_OK)
                
                response.delete_cookie('refresh_token')
                return response
        except Exception as e:
            return Response({"error":str(e)},status=400)



class ProfileApiView(APIView):
    
    
    
    def get(self,req):
        user = req.user  #in here get userobject from token
        serializer = UserSerializer(user)
        return Response(serializer.data)


# admin module
# admin module
from django.core.mail import send_mail
from django.conf import settings


from products.pagination import Pagination

class UsersListApiView(APIView):
    
    permission_classes = [AllowAny]
    
    def get(self,req):
        users =User.objects.all().order_by('id')
        paginator = Pagination()
        page = paginator.paginate_queryset(users,req)        
        serializer = UserListSerializer(page,many=True)
        
        return paginator.get_paginated_response(serializer.data)
    
    def patch(self,req,pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error":"The user is not Here"})
        
        old_status = user.is_active
        
        
        serializer = UserListSerializer(user,data=req.data,partial=True)
        if serializer.is_valid():
            
            updated_user = serializer.save()
            if old_status == True and updated_user.is_active == False:
                subject = "Important Update Regarding Your PeakPack Account"

                message = (
                f"Hi {updated_user.username},\n\n"
                "We hope you're doing well.\n\n"
                "We wanted to inform you that your PeakPack account has been temporarily restricted "
                    "due to a policy review.\n\n"
                "At PeakPack, we are committed to maintaining a trusted and secure community for everyone. "
                "If you believe this action was taken in error or would like more details, "
                "please contact our support team.\n\n"
                    "We're here to help and ensure every adventurer gets back on track.\n\n"
                "Pack for the Peaks.\n\n"
                "Team PeakPack 🏔️"
                )

                
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [updated_user.email],
                    fail_silently=True
                    
                )
            
        
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,req,pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error":"The user is not Here"})
        
        user.delete()
        return Response({"msg":"The User Was Deleted"})
        
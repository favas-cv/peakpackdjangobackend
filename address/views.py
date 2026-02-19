from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AddressModel
from .serializers import AddressSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin



class AddressListView(GenericAPIView,ListModelMixin,CreateModelMixin):
    
    
    # queryset = AddressModel.objects.all()
    serializer_class = AddressSerializer
    
    def get_queryset(self):
        return AddressModel.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get(self,req):
        return self.list(req)
    
    def post(self,req):
        return self.create(req)
    
    
from rest_framework.generics import RetrieveUpdateDestroyAPIView

class AddressDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer

    def get_queryset(self):
        return AddressModel.objects.filter(user=self.request.user)


    
    
    
    
    
    
        


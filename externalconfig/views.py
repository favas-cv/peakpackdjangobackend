from django.shortcuts import render

# Create your views here.
import requests 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.conf import settings

class WeatherApiView(APIView):
    permission_classes = [AllowAny]
    
    
    def get_client_ip(self,req):
        x_forwarded_for = req.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = req.META.get('REMOTE_ADDR')
        return ip
    
    
    
    def get(self,req):
        ip = self.get_client_ip(req)
        
        ip_info = requests.get(f"http://ip-api.com/json/{ip}").json()
        
        if ip_info.get('status') == 'success':
            city = ip_info.get('city')
        else:
            
            city = 'gulmarg'
        
        # lat = req.query_params.get('lat')
        # lon = req.query_params.get('lon')
        
        url =  "https://api.weatherapi.com/v1/current.json"
        
        # if lat and lon:
        #     query = f"{lat},{lon}"
        # else:
        #     query = city if city else 'kochi'
            
        
        
        params = {
            "key":settings.WEATHER_API_KEY,
            "q":city


        }
        
        repsonce = requests.get(url,params=params)
        data = repsonce.json()
        print(data)
        temp = data['current']['temp_c']
        condition = data['current']['condition']['text']
        suggestion = "Perfect for local trip!"
        
        if temp> 30:
            suggestion = 'Escape the heat! Visit Kashmir or Manali '
        elif 'rain' in condition.lower():
            suggestion = 'Enjoy monsoon in Munnar or Coorg!'
        elif temp < 15:
            suggestion ='Best time for Rajasthan desert camp!'
        
        
        
        return Response({
            
            'location':{
                'name':data['location']['name'],
                'region':data['location']['region'],
                'country':data['location']['country']
                
                },
            'temp':temp,
            'condition':condition,
            'suggestion':suggestion
        })
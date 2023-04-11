from dataclasses import fields
from rest_framework import serializers
from .models import Cart
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["name","img","price","des","rating","link","quantity","item_total"]
        
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...
        


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer        
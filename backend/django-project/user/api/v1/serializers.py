from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ...models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomUserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email','password')
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

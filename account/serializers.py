
from rest_framework import serializers
from .models import User

# login serializers
class LoginSerializerUser(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'})
    class Meta:
        model = User
        fields = ['email','password']


# user register serailizer 
class UserRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password']

class OtpVerifySerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['user_id','otp']
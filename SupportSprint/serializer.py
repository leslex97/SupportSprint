from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework import serializers



class UserSerializer(serializers.HyperlinkedModelSerializer):
    phone_number = serializers.CharField(source="userprofile.phone_number", read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'phone_number']
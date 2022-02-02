from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Inventory

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
        )


class ChangeUserInventorySerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=16)
    date = serializers.CharField(max_length=4)
    cvv = serializers.CharField(max_length=3)

    class Meta:
        model = Inventory
        fields = (
            'code',
            'date',
            'cvv',
            'balans',
            'premium',
        )

class UserInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = (
            'balans',
            'premium'
        )
from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import CreateUserSerializer, ChangeUserInventorySerializer, UserInventorySerializer
from .services import create_user, change_balans
from .models import Inventory

User = get_user_model()


class CreateUser(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    def POST(self, request):
        serializer = self.get_serializer_class(data=request.data).is_valid(raise_exception=True)
        ser_data = serializer.validated_data()

        user = create_user(ser_data)
        return Response(data=user, status=status.HTTP_201_CREATED)


class ChangeInventory(mixins.ListModelMixin,viewsets.GenericViewSet):

    def get_serializer_class(self):
        if self.action == "change_balans":
            return ChangeUserInventorySerializer
        return UserInventorySerializer

    def get_queryset(self):
        return Inventory.objects.filter(owner=self.request.user)
 
    @action(methods=['PATCH', ], detail=False)
    def change_balans(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(request.data)
        data = serializer.data
        changed_data = change_balans(owner=self.request.user, data=data)
        if changed_data:
            return Response(data=changed_data, status=status.HTTP_200_OK)
        return Response(data=False, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import CreateUserSerializer, ChangeUserInventorySerializer, UserInventorySerializer
from .services import create_user, change_balans
from .models import Inventory
from shares.models import InventoryShare
from shares.serializers import InventoryShareSerializer
from offer.services import serialization

User = get_user_model()
admin = User.objects.get(username='admin')


class CreateUser(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    def POST(self, request):
        serializer = self.get_serializer_class(data=request.data).is_valid(raise_exception=True)
        ser_data = serializer.validated_data()

        user = create_user(ser_data)
        return Response(status=status.HTTP_201_CREATED)


class ChangeInventory(mixins.ListModelMixin,viewsets.GenericViewSet):

    def get_serializer_class(self):
        if self.action == "change_balans":
            return ChangeUserInventorySerializer
        return UserInventorySerializer

    def get_queryset(self):
        return Inventory.objects.filter(owner=admin)#self.request.user)
 
    @action(methods=['PATCH', ], detail=False)
    def change_balans(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(request.data)
        data = serializer.data
        changed_data = change_balans(owner=admin, data=data) #self.request.user
        if changed_data:
            return Response(data=changed_data, status=status.HTTP_200_OK)
        return Response(data=False, status=status.HTTP_400_BAD_REQUEST)


class FullInventoryAPI(viewsets.GenericViewSet):

    def get_serializer_class(self):
        pass

    @action(methods=('GET',), detail=False)
    def full_inventory(self, request):
        
        shares_data = serialization(
            serializer=InventoryShareSerializer, 
            queryset=InventoryShare.objects.filter(owner=admin)#self.request.user)
            )
            
        balans_data = UserInventorySerializer(Inventory.objects.get(owner=admin))#self.request.user))
        
        data = {
            'balans_data': balans_data.data,
            'shares_data': shares_data
        }
        return Response(data=data, status=status.HTTP_200_OK)

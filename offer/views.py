from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import mixins, viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core import serializers

from django.contrib.auth.models import User
from django.db.models import Q

from .models import SimpleOffer, PremiumOffer, Trade
from .serializers import (SimpleOfferSerializer, PremiumOfferSerializer,
                            CreatePremiumOfferSerialiazer, 
                            CreateSimpleOfferSerialiazer,
                            UpdateMySimpleOfferSerializer,
                            UpdateMyPremiumOfferSerializer,
                            DeletePremiumOfferSerializer,
                            DeleteSimpleOfferSerializer,
                            ActivateAllOfferSerializer,
                            TradeSerializer)
from .services import create_simple_offer, create_premium_offer, serialization, ActivateAllOffer


admin = User.objects.get(username='admin')

class ListAllOffer(viewsets.GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'simple':
            return CreateSimpleOfferSerialiazer
        elif self.action == 'premium':
            return CreatePremiumOfferSerialiazer

    @action(methods=['GET', ], detail=False)
    def my(self, request):
        
        simple_data = serialization(
            serializer=SimpleOfferSerializer, 
            queryset=SimpleOffer.objects.filter(user=admin, current_count__gt=0)#self.request.user)
            )

        premium_data = serialization(
            serializer=PremiumOfferSerializer, 
            queryset=PremiumOffer.objects.filter(user=admin, current_count__gt=0)#self.request.user)
            )

        data = {
            'simple_data': simple_data,
            'premium_data': premium_data 
        }

        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def simple(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(request.data)
        response_data = create_simple_offer(user=admin, data=serializer.data) #self.request.user
        if response_data:
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(data=False, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST', ], detail=False)
    def premium(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(request.data)
        response_data = create_premium_offer(user=admin, data=serializer.data) #self.request.user
        if response_data:
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(data=False, status=status.HTTP_400_BAD_REQUEST)


class ChangeMySimpleOffersAPI(mixins.UpdateModelMixin, viewsets.GenericViewSet):

    def get_serializer_class(self):
        return UpdateMySimpleOfferSerializer
    
    def get_queryset(self):
        return SimpleOffer.objects.filter(user=admin)#self.request.user)


class ChangeMyPremiumOffersAPI(mixins.UpdateModelMixin, viewsets.GenericViewSet):

    def get_serializer_class(self):
        return UpdateMyPremiumOfferSerializer
    
    def get_queryset(self):
        return PremiumOffer.objects.filter(user=admin)#self.request.user)


class DeleteSimpleOfferAPI(mixins.DestroyModelMixin, viewsets.GenericViewSet):

    def get_serializer_class(self):
        return DeleteSimpleOfferSerializer

    def get_queryset(self):
        return SimpleOffer.objects.filter(user=admin)#self.request.user)


class DeletePremiumOfferAPI(mixins.DestroyModelMixin, viewsets.GenericViewSet):

    def get_serializer_class(self):
        return DeletePremiumOfferSerializer

    def get_queryset(self):
        return PremiumOffer.objects.filter(user=admin)#self.request.user)




class ActivateAllOfferAPI(viewsets.GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'activate':
            return ActivateAllOfferSerializer

    @action(methods=['POST',], detail=False)
    def activate(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(request.data)
        ActivateAllOffer(serializer.data)
        if serializer.data:
            return Response(data=True, status=status.HTTP_200_OK)
        elif not serializer.data:
            return Response(data=False, status=status.HTTP_200_OK)

    
class TradeAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    
    def get_serializer_class(self):
        return TradeSerializer
    
    def get_queryset(self):
        return Trade.objects.filter(Q(buyer=admin) | Q(seller=admin))

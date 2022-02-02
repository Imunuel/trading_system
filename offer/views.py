from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import mixins, viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core import serializers

from .models import SimpleOffer, PremiumOffer
from .serializers import (SimpleOfferSerializer, PremiumOfferSerializer,
                            CreatePremiumOfferSerialiazer, 
                            CreateSimpleOfferSerialiazer)
from .services import create_simple_offer, create_premium_offer


class ListAllOffer(viewsets.GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'simple':
            return CreateSimpleOfferSerialiazer
        elif self.action == 'premium':
            return CreatePremiumOfferSerialiazer

    @action(methods=['GET', ], detail=False)
    def all_my(self, request):
        simple_serializer = SimpleOfferSerializer(SimpleOffer.objects.filter(user=self.request.user), many=True)
        premium_serializer = PremiumOfferSerializer(PremiumOffer.objects.filter(user=self.request.user), many=True)
        
        simple_data = simple_serializer.data
        premium_data = premium_serializer.data

        data = {
            'simple_data': simple_data,
            'premium_data': premium_data 
        }

        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def simple(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(request.data)
        response_data = create_simple_offer(user=self.request.user, data=serializer.data)
        return Response(data=response_data, status=status.HTTP_201_CREATED)
    
    @action(methods=['POST', ], detail=False)
    def premium(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(request.data)
        response_data = create_premium_offer(user=self.request.user, data=serializer.data)
        return Response(data=response_data, status=status.HTTP_201_CREATED)
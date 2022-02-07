from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import mixins, viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core import serializers

from .models import SimpleOffer, PremiumOffer
from .serializers import (SimpleOfferSerializer, PremiumOfferSerializer,
                            CreatePremiumOfferSerialiazer, 
                            CreateSimpleOfferSerialiazer,
                            UpdateDeleteMySimpleOfferSerializer,
                            UpdateDeleteMyPremiumOfferSerializer,
                            ActivateAllOfferSerializer)
from .services import create_simple_offer, create_premium_offer, serialization, ActivateAllOffer


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
            queryset=SimpleOffer.objects.filter(user=self.request.user)
            )

        premium_data = serialization(
            serializer=PremiumOfferSerializer, 
            queryset=PremiumOffer.objects.filter(user=self.request.user)
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
        response_data = create_simple_offer(user=self.request.user, data=serializer.data)
        if response_data:
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(data=False, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST', ], detail=False)
    def premium(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(request.data)
        response_data = create_premium_offer(user=self.request.user, data=serializer.data)
        if response_data:
            return Response(data=response_data, status=status.HTTP_201_CREATED)
        return Response(data=False, status=status.HTTP_400_BAD_REQUEST)


# class UpdateDeleteMySimpleOfferAPI(mixins.UpdateModelMixin, mixins.DestroyModelMixin ,viewsets.GenericViewSet):

#     def get_serializer_class(self):
#         return UpdateDeleteMySimpleOfferSerializer

#     def get_queryset(self):
#         return SimpleOffer.objects.filter(user=self.request.user)


# class UpdateDeleteMyPremiumOfferAPI(mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):

#     def get_serializer_class(self):
#         return UpdateDeleteMyPremiumOfferSerializer

#     def get_queryset(self):
#         return PremiumOffer.objects.filter(user=self.request.user)


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

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import mixins, viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core import serializers

from .models import SimpleOffer, PremiumOffer
from .serializers import SimpleOfferSerializer, PremiumOfferSerializer

import json



class ListAllOffer(viewsets.GenericViewSet):

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

from django.shortcuts import render
from rest_framework import mixins, viewsets, status, generics

from .models import Share
from .serializers import FullShareSerializer


class ShareListAPI(mixins.ListModelMixin, viewsets.GenericViewSet):

    def get_serializer_class(self):
        return FullShareSerializer
    
    def get_queryset(self):
        return Share.objects.all()



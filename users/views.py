from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .serializers import CreateUserSerializer
from .services import CreateUser

User = get_user_model()


class CreateUser(mixins.CreateModelMixin, viewsets.GenericViewSet):

    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

    def POST(self, request):
        serializer = self.get_serializer_class(data=request.data).is_valid(raise_exception=True)
        ser_data = serializer.validated_data()

        user = CreateUser(ser_data)
        return Response(data=user, status=status.HTTP_201_CREATED)

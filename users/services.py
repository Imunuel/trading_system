from django.contrib.auth import get_user_model

User = get_user_model()


def CreateUser(data):
    return User.objects.create(**data)
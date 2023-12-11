from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .serializers import UserSerializer


class ChefCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        response_data = {
            'user_id': user.id,
            'username': user.username,
            'token': Token.objects.get(user=user).key
        }
        return Response(response_data)

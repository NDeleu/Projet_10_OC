from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserRegisterSerializer, MyTokenObtainPairSerializer


class RegisterView(APIView):
    """
    N'autoriser que les methodes post
    """
    http_method_names = ['post']

    def post(self, *args, **kwargs):
        serializer = UserRegisterSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

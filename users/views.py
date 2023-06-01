from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUserModel
from .serializers import UserRegisterSerializer, UserLoginToken


# Create your views here.

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUserModel
    serializer_class = UserRegisterSerializer


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginToken

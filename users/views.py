from datetime import timedelta

from django.utils.crypto import get_random_string
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .eskiz import send_verify_code
from .models import CustomUserModel, VerificationCodeSMS
from .serializers import (UserRegisterSerializer, UserLoginToken,
                          SendVerificationCodeSMS, CheckVerificationCodeSMS,
                          UserSerializer)


# Create your views here.

class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUserModel.object.all()
    serializer_class = UserRegisterSerializer


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginToken


class SendVerificationSMS(generics.CreateAPIView):
    queryset = VerificationCodeSMS.objects.all()
    serializer_class = SendVerificationCodeSMS

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            phone = int(serializer.validated_data.get('phone'))
        except ValueError:
            return Response({'format': 'Invalid format phone number.'})
        else:
            code = get_random_string(allowed_chars='0123456789', length=6)
            verification_code, _ = (
                VerificationCodeSMS.objects.update_or_create(phone=phone,
                                                             defaults={'code': code, 'is_verified': False}))
            send_verify_code(phone, code)
            verification_code.expired_at = verification_code.last_sent_time + timedelta(seconds=90)
            verification_code.save(update_fields=['expired_at'])
            return Response({'status': 'Successfully sent email verification code.'}, status=status.HTTP_201_CREATED)


class CheckVerificationSMS(generics.CreateAPIView):
    queryset = VerificationCodeSMS.objects.all()
    serializer_class = CheckVerificationCodeSMS

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        phone = serializer.validated_data.get('phone')
        code = serializer.validated_data.get('code')
        verification_code = self.get_queryset().filter(phone=phone, is_verified=False).order_by(
            '-last_sent_time').first()
        if verification_code:
            if verification_code.code != code or verification_code.is_expire:
                raise ValidationError("Verification code invalid.")
            else:
                verification_code.is_verified = True
                verification_code.save(update_fields=["is_verified"])
                return Response({"detail": "Verification code is verified."})
        else:
            raise ValidationError("Verification code not found.")


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUserModel
    serializer_class = UserSerializer
    lookup_field = 'pk'

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['phone', 'email', 'profile_picture', 'first_name', 'last_name', 'gender', 'job', 'birth_date',
                  'country', 'region',
                  'address', 'is_verified']


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUserModel
        fields = ('first_name', 'last_name', 'phone', 'password1', 'password2')
        read_only_fields = ('id',)

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2', None)
        phone = attrs.get('phone')

        phone_exists = CustomUserModel.object.filter(phone=phone).exists()
        if phone_exists:
            raise ValidationError('Phone already exists.')
        if password1 != password2:
            raise ValidationError("Password didn't match.")

        return super().validate(attrs)

    def create(self, validated_data):
        password1 = validated_data.pop("password1", None)
        validated_data.pop("password2", None)
        user = CustomUserModel(**validated_data)
        user.set_password(password1)
        user.save()
        return user


class UserLoginToken(serializers.Serializer):
    token_class = RefreshToken

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone'] = serializers.CharField(max_length=15, required=False)
        self.fields['password'] = PasswordField(min_length=8, required=False)

    default_error_messages = {
        "no_active_account": "No Active Account."
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone is None:
            raise ValidationError('Send Phone Number')
        if password is None:
            raise ValidationError('Send Password.')

        user = authenticate(request=self.context.get('request'), phone=phone, password=password)
        if not api_settings.USER_AUTHENTICATION_RULE(user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        refresh = self.get_token(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["user"] = UserSerializer(user).data

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)
        return data

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


# ['phone', 'email', 'profile_picture', 'first_name', 'last_name',
# 'gender', 'job', 'birth_date', 'country', 'region','address', 'is_verified']

class SendVerificationCodeSMS(serializers.Serializer):
    phone = serializers.CharField(max_length=15)

    def validate(self, attrs):
        phone = attrs.get('phone')
        if not phone:
            raise ValidationError('Send phone number.')
        if not phone.startswith('998'):
            raise ValidationError("Available only to citizens of Uzbekistan")

        return attrs


class CheckVerificationCodeSMS(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        code = attrs.get('code')
        if not code:
            raise ValidationError('Enter the sent code.')
        if len(code) != 6:
            raise ValidationError('Invalid code.')

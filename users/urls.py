from django.urls import path

from .views import (UserRegisterView, UserLoginView,
                    SendVerificationSMS, CheckVerificationSMS,
                    ProfileView)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('sms/verification/', SendVerificationSMS.as_view(), name='verification'),
    path('sms/check-verification/', CheckVerificationSMS.as_view(), name='check-verification'),
]

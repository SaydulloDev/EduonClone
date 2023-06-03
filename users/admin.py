from django.contrib import admin

from .models import CustomUserModel, MyCourses, VerificationCodeSMS


# Register your models here.
@admin.register(CustomUserModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone']


@admin.register(MyCourses)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['course']


@admin.register(VerificationCodeSMS)
class VerificationCodeSMS(admin.ModelAdmin):
    list_display = ['phone', 'code', 'is_verified']

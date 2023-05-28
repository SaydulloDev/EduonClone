from django.contrib import admin

from .models import CustomUserModel, MyCourses


# Register your models here.
@admin.register(CustomUserModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone']


@admin.register(MyCourses)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['course']

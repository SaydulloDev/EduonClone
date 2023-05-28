from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from .manager import CustomUserManager


# Create your models here.


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    class GenderChoice(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', null=True, blank=True)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GenderChoice.choices, null=True, blank=True)
    job = models.CharField(max_length=128, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    region = models.CharField(max_length=128, null=True, blank=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['password']
    object = CustomUserManager()

    def clean(self):
        if not self.phone.startswith('998'):
            raise ValidationError('Available only to citizens of Uzbekistan')

    def natural_key(self):
        return self.phone

    def get_full_name(self):
        if self.first_name:
            return self.first_name + ' ' + self.last_name

    def __str__(self):
        if self.first_name is not None:
            return self.first_name
        else:
            return self.phone


class MyCourses(models.Model):
    course = models.ForeignKey('eduon.Course', related_name='enrolled_course', on_delete=models.CASCADE)

    def clean(self):
        course = self.course
        if MyCourses.objects.filter(course=course).exists():
            raise ValidationError('Course Already.')

    def __str__(self):
        return self.course.title

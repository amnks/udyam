from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager
from PIL import Image
# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile
# import sys

class User(AbstractUser):
    college_year = [
        ('SL', 'Select year'),
        ('1', '1st year'),
        ('2', '2nd year'),
        ('3', '3rd year'),
        ('4', '4th year')
    ]

    gender = [
        ('SL', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = models.CharField(max_length=30, unique=False)
    email = models.EmailField(verbose_name='College Email id', unique=True)
    Year = models.CharField(max_length=2, choices=college_year, default='SL')
    College_name = models.CharField(max_length=254, default='Type College Name')
    Gender = models.CharField(max_length=2, choices=gender, default='SL')
    Phone = models.CharField(max_length=10, validators=[MinLengthValidator(10), MaxLengthValidator(10)])
    image = models.ImageField(upload_to='profile_images/', blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Query(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=256)
    contact = models.CharField(max_length=10, validators=[MinLengthValidator(10), MaxLengthValidator(10)])
    query = models.CharField(max_length=256)

    def __str__(self):
        return "{}, {}".format(self.name, self.email)

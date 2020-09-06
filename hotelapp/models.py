from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
class Customer(AbstractUser):
    hotel_name = models.CharField(max_length=150,blank = True)
    REQUIRED_FIELDS = ['email']



class Hotels(models.Model):
    photo = models.ImageField(upload_to='hotel_images')
    name = models.CharField(max_length=50,blank=False)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    REQUIRED_FIELDS = ['photo','name']

class Rooms(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotels,on_delete=models.CASCADE)
    room_name = models.CharField(max_length=50)
    cost = models.IntegerField()
    photo = models.ImageField(upload_to='room_images')
    location = models.CharField(max_length=100,default="Banglore")
    booked = models.BooleanField(default=False)
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    available_from = models.DateField(default='2020-1-1')
    available_to = models.DateField(default='2020-12-31')
    REQUIRED_FIELDS = ['photo', 'room_name', 'cost', 'adults', 'children', 'available_from', 'available_to','location']

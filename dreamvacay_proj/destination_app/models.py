from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, null=True, unique=True)
    phone = models.CharField(max_length=15, null=True)
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Destination(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='destination_images/')
    weather = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='')
    gmap = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Dest_Images(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='destination_images/highlights')
from django.db import models
from django.contrib.auth.models import User
from bookapp.models import * 

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    phone = models.IntegerField(null=True)
    profile_pic = models.ImageField(null=True,blank=True)
    date_created = models.DateTimeField (auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):

    name=models.CharField(max_length=200,null=True)
    author=models.CharField(max_length=200,null=True)
    price= models.FloatField()
    


    def __str__(self):
        return '{}'.format(self.name)    
    

class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for Delivery','Out for Delivery'),
        ('Delivered','Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=True)
    date_created = models.DateTimeField (auto_now_add=True, null=True)
    status = models.CharField(max_length=200,null=True,choices=STATUS) 

    def __str__(self):
        return 'Order no.{}'.format(self.id)   

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    pname= models.CharField(max_length=100,null=True)
    category= models.CharField(max_length=100,null=True)
    price= models.FloatField(null=True)
    breed=models.CharField(max_length=100,null=True)
    description=models.CharField(max_length=500,null=True)
    date=models.DateField(auto_now=True,null=True)
    time=models.TimeField(auto_now=True,null=True)
    images=models.ImageField(upload_to='media',null=True)
    imag1=models.ImageField(upload_to='media',null=True)
    imag2=models.ImageField(upload_to='media',null=True)
    imag3=models.ImageField(upload_to='media',null=True)


    def __str__(self):
       return self.pname

class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=200,null=True)
    flat = models.CharField(max_length=300,null=True)
    landmark = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=100,null=True)
    pincode = models.IntegerField(null=True)
    contact = models.BigIntegerField(null=True)
    contactA = models.BigIntegerField(null=True)

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=200,null=True)


from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300)
    username = models.CharField(max_length=300,default='username')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class ProductType(models.Model):
    name = models.CharField(max_length=300)

class Product(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    type = models.ForeignKey(ProductType,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    department = models.ForeignKey('Department',on_delete=models.SET_NULL,null=True)

class Purchase(models.Model):
    product = models.ForeignKey('Product',on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    price  = models.FloatField()
    customer = models.ForeignKey('Customer',on_delete=models.SET_NULL,null=True)

class Sell(models.Model):
    product = models.ForeignKey('Product',on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    price  = models.FloatField()
    suppliers = models.ForeignKey('Suppliers',on_delete=models.SET_NULL,null=True)

class Customer(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    email = models.EmailField()

class Suppliers(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    email = models.EmailField()


class Department(models.Model):
    name = models.CharField(max_length=300)
    floor = models.IntegerField()

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    payment_id = models.CharField(max_length=300, unique=True)
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

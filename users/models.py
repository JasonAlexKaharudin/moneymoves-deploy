from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User, AbstractUser
from django.db.models.fields.related import OneToOneField
from phonenumber_field.modelfields import PhoneNumberField
from merchants.models import Merchant

# class User(AbstractUser):
#     is_user = models.BooleanField(default=False)
#     is_merchant = models.BooleanField(default=False)
#     email = models.EmailField()
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)

# class money_User(models.Model):
#     user = OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
#     phone_number = PhoneNumberField(blank=True)
#     wallet = models.DecimalField(max_digits=6, decimal_places=2, default=0)


# class Merchants_User(models.Model):
#     user = OneToOneField(User, on_delete=CASCADE, primary_key=True)
#     store = OneToOneField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    Phone_Number = PhoneNumberField(blank=True)
    wallet = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"

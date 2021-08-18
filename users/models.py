from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from referrals.models import Referral

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    Phone_Number = PhoneNumberField(blank=True)
    wallet= models.DecimalField(max_digits=6, decimal_places=2, default=0)
    num_of_refers = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"

class OrphanList(models.Model):
    Phone_Number = PhoneNumberField(blank=True)
    orphan_cashback = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    referral_obj = models.ForeignKey(Referral, on_delete=CASCADE, default=None)
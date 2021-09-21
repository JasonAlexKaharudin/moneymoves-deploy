from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Partner_Merchant(models.Model):
    name = models.CharField(max_length=200)
    date_joined = models.DateTimeField("Date Joined")
    store_link = models.URLField(max_length=200, null = True)

    class Meta:
        verbose_name_plural = "Partner Merchants"

    def __str__(self):
        return self.name

class Zalora_Brand(models.Model):
    brand_name = models.CharField(max_length=200)
    brand_link = models.CharField(max_length=500, default="None")
    cashback_amt = models.IntegerField(default=0)
    img_link = models.URLField(max_length=300)

    class Meta:
        verbose_name_plural = "Zalora Merchants"

    def __str__(self):
        return self.brand_name
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Merchant(models.Model):
    name = models.CharField(max_length=200)
    date_joined = models.DateTimeField("Date Joined")
    store_link = models.URLField(max_length=200, null = True)
    class Meta:
        verbose_name_plural = "Merchants"

    def __str__(self):
        return self.name


class Product(models.Model):
    product_ID = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    merchant = models.ForeignKey(Merchant, on_delete=CASCADE)

    class Meta:
        verbose_name_plural = "Products"
        
    def __str__(self):
        return self.name
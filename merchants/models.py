from django.db import models
from datetime import datetime
from django.db.models.deletion import CASCADE

# Create your models here.
def jsonfield_default_value(): 
    productList = {
        "product": 0
    }
    return productList

class Partner_Merchant(models.Model):
    name = models.CharField(max_length=200)
    date_joined = models.DateTimeField("Date Joined")
    store_link = models.URLField(max_length=200, null = True)
    img_link = models.URLField(max_length=200, null = True)
    cashback_amt = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Partner Merchants"

    def __str__(self):
        return self.name

class webhookOrders(models.Model):
    merchant = models.ForeignKey(Partner_Merchant, on_delete=CASCADE)
    order_id = models.IntegerField()
    customer_email = models.EmailField(max_length=60, default = "None")
    location = models.CharField(max_length=20, default="SG")
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    products = models.JSONField(default = jsonfield_default_value, null=True)
    date_published = models.DateTimeField(default=datetime.now, blank=True)
    
    class Meta:
        verbose_name_plural = "Webhook Orders"
        
    def __str__(self):
        return f"{self.merchant.name} order ID: #{self.order_id}"

class Amazon_Brand(models.Model):
    brand_name = models.CharField(max_length=200)
    brand_link = models.CharField(max_length=500, default="None")
    cashback_amt = models.IntegerField(default=0)
    img_link = models.URLField(max_length=300)

    class Meta:
        verbose_name_plural = "Amazon Merchants"

    def __str__(self):
        return self.brand_name
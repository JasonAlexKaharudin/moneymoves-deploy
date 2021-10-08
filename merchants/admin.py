from django.contrib import admin
from .models import Partner_Merchant, Amazon_Brand, webhookOrders
# Register your models here.
admin.site.register(webhookOrders)
admin.site.register(Partner_Merchant)
admin.site.register(Amazon_Brand)

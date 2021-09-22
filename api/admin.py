from django.contrib import admin
from .models import orderRef, invalidOrder

# Register your models here.
admin.site.register(orderRef)
admin.site.register(invalidOrder)
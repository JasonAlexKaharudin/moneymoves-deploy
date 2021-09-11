from django.contrib import admin
from .models import Referral, OrphanList
# Register your models here.
admin.site.register(Referral)
admin.site.register(OrphanList)
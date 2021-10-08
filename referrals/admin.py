from django.contrib import admin
from .models import Referral, OrphanList, receipts, orphanReceipt
# Register your models here.
admin.site.register(Referral)
admin.site.register(OrphanList)
admin.site.register(receipts)
admin.site.register(orphanReceipt)
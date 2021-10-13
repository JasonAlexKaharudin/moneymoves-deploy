from django.contrib import admin
from webapp.adminMixins import ExportCSVMixin
from .models import Referral, OrphanList, receipts, orphanReceipt

# Register your models here.
@admin.register(receipts)
class receiptsAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("referer", "referee", "is_verified", "date_published")
    list_filter = ("referer","is_verified", "date_published")
    actions = ["export_as_csv"]

@admin.register(orphanReceipt)
class orphanReceiptAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("referer", "referee", "referral_obj")
    list_filter = ("referer", "referee", "referral_obj")
    actions = ["export_as_csv"]

@admin.register(Referral)
class ReferralsAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("referer_username", "merchant", "orderID", "referee_has_account", "date_published")
    list_filter = ("merchant", "totalAmt", "is_Verified", "date_published")
    actions = ["export_as_csv"]

@admin.register(OrphanList)
class OrphanReferralsAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("refereeEmail", "referee_cashback", "referral_obj")
    list_filter = ("refereeEmail", "referee_cashback", "referral_obj")
    actions = ["export_as_csv"]

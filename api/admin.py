from webapp.adminMixins import ExportCSVMixin
from django.contrib import admin
from .models import orderRef, invalidOrder, trackWidget

@admin.register(trackWidget)
class widgetAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("merchant", "date_recorded")
    list_filter = ("merchant", "numClicks", "date_recorded")
    actions = ["export_as_csv"]

@admin.register(orderRef)
class orderRefAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("referrer","merchant_name", "orderID", "refereeEmail", "date_published", "webhook_obj")
    list_filter = ("referrer","merchant_name", "orderID", "refereeEmail", "date_published")
    actions = ["export_as_csv"]

@admin.register(invalidOrder)
class invalidOrderAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("referrer","merchant_name" ,"orderID", "refereeEmail", "date_published")
    list_filter = ("referrer","merchant_name" ,"orderID", "refereeEmail", "date_published")
    actions = ["export_as_csv"]
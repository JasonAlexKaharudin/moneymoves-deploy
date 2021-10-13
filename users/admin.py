from django.contrib import admin
from webapp.adminMixins import ExportCSVMixin
from .models import Profile


@admin.register(Profile)
class profileAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("user", "wallet", "num_of_refers", "signup_refs")
    list_filter = ("wallet", "num_of_refers", "signup_refs")
    actions = ['export_as_csv']
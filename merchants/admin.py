from django.contrib import admin
from django import forms
from webapp.adminMixins import ExportCSVMixin
from .models import Partner_Merchant, Amazon_Brand, webhookOrders

@admin.register(Partner_Merchant)
class partner_merchants(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("name", "cashback_amt", "date_joined")
    list_filter = ("name", "cashback_amt","date_joined")
    actions = ["export_as_csv"]

@admin.register(webhookOrders)
class webhookOrders(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("merchant", "order_id", "customer_email", "date_published")
    list_filter = ("merchant", "order_id", "customer_email", "location", "date_published")
    actions = ["export_as_csv"]

@admin.register(Amazon_Brand)
class Amazon_Brand_Admin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("brand_name", "cashback_amt")
    list_filter = ("brand_name", "cashback_amt")
    actions = ["export_as_csv"]

    # change_list_template = "merchants/amazon_change_list.html"

    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [
    #         path('import-csv/', self.import_csv),
    #     ]
    #     return my_urls + urls

    # def import_csv(self, request):
    #     if request.method == "POST":
    #         csv_file = request.FILES["csv_file"]

    #         if not csv_file.name.endswith('csv'):
    #             messages.warning(request, 'The wrong file type was uploaded')

    #         file_data = csv_file.read().decode("utf-8")
    #         csv_data = file_data.split("\n")

    #         for x in csv_data:
    #             fields = x.split(",")
    #             created_brand = Amazon_Brand.objects.update_or_create(
    #                 brand_name = fields[0],
    #                 cashback_amt = fields[1],
    #                 brand_link = fields[2],
    #                 img_link = fields[3]
    #             )
    #         self.message_user(request, "Your csv file has been imported")
    #         return redirect("..")
    #     form = CsvImportForm()
    #     payload = {"form": form}
    #     return render(
    #         request, "admin/csv_form.html", payload
    #     )

from django.contrib import admin
from webapp.adminMixins import ExportCSVMixin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


@admin.register(Profile)
class profileAdmin(admin.ModelAdmin, ExportCSVMixin):
    list_display = ("user", "wallet", "num_of_refers", "signup_refs", "links_created")
    list_filter = ("wallet", "num_of_refers", "signup_refs", "links_created")
    actions = ['export_as_csv']

class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'date_joined', 'last_login')
    list_filter = ('date_joined', 'last_login')

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
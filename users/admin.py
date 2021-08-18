from django.contrib import admin
from .models import Profile, OrphanList
# Register your models here.
admin.site.register(Profile)
admin.site.register(OrphanList)
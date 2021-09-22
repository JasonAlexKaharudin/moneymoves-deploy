from django.urls import path
from merchants import views as merchant_views

app_name = 'merchants'

urlpatterns = [
    path('sundayvalley/', merchant_views.webhook_sunday_valley, name="Sunday Valley orders"),
    path('dnc/', merchant_views.webhook_dnc, name="Do Not Cross orders"),
]
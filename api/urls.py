from django.urls import path
from api import views as api_views

app_name = 'api'

urlpatterns = [
    path('webhook/', api_views.api_view_webhook, name='api_view_webhook'),
]
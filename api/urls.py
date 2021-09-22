from django.urls import path
from api import views as api_views

app_name = 'api'

urlpatterns = [
    path('refs/', api_views.ref_api, name='ref_api'),
]
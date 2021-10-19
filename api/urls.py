from django.urls import path, re_path
from api import views as api_views
import api

app_name = 'api'

urlpatterns = [
    path('refs/', api_views.ref_api, name='ref_api'),
    path('widget/', api_views.widget, name='widget tracking'),
    path('links/', api_views.links_generated, name='links generated'),
    re_path(r'^postback/$', api_views.involveAsia, name='postbackURL')
]
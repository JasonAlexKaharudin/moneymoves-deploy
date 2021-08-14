from django.urls import path
from . import views
from .views import CreateReferral, ReferralListView, ReferralDetailView

app_name = 'referrals'

urlpatterns = [
    path('', ReferralListView.as_view(), name="referral-list"),
    path('<int:pk>/', ReferralDetailView.as_view(), name="referral-detail"),
    path('upload/', CreateReferral.as_view(), name= "upload-receipt"),
]
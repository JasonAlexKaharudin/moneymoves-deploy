from django.urls import path
from . import views
from .views import CreateReferral, ReferralListView, ReferralDetailView
from referrals import views as referral_views

app_name = 'referrals'

urlpatterns = [
    path('', ReferralListView.as_view(), name="referral-list"),
    path('<int:pk>/', ReferralDetailView.as_view(), name="referral-detail"),
    path('upload/', referral_views.UploadReceipt, name= "upload-receipt"),
]
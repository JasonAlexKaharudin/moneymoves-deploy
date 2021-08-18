from django.urls import path
from .views import ReferralDetailView
from referrals import views as referral_views

app_name = 'referrals'

urlpatterns = [
    path('', referral_views.wallet_referrals, name="referral-list"),
    path('<int:pk>/', ReferralDetailView.as_view(), name="referral-detail"),
    path('upload/', referral_views.UploadReceipt, name= "upload-receipt"),
]
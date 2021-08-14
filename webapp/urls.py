from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home page'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile page'),
    path('phone/', user_views.phone, name='phone'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('brands/', user_views.BrandListView.as_view(), name = 'brands page' ),
    path('referral/', include('referrals.urls'))
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

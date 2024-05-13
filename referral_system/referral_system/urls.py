from django.contrib import admin
from django.urls import path

from referral_app import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('authentication/', views.user_authentication, name='user_authentication'),
    path('account_access/', views.account_access, name='account_access'),
    path('admin/', admin.site.urls),
]

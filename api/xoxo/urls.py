from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from .import views

urlpatterns = [
    path('send/rewards/',views.get_vou,name="get_voucher")
]
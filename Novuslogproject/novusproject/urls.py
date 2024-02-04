from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views #new
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('novusapp.urls')),

]

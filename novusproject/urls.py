from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views #new
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('novusapp.urls')),
    path('api/', include('api.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




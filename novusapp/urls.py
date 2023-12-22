from django.urls import path
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from .import views


urlpatterns = [
    path('',views.login_view,name="login_view"),
    path('dashboard_redirect', views.dashboard_redirect, name='dashboard_redirect'),
    path('register',views.register,name="register"),
    path('hod_dashboard/confirm_registration/<str:id>',views.confirm_registration,name='confirm_registration'),
    path('logout/', views.logout_view, name='logout'),
    path('hod_dashboard',views.hod_dashboard, name='hod_dashboard'),
    path('hod_dashboard/tables',views.tables,name='tables'),
    path('hod_dashboard/userhod_data',views.userhod_data,name='userhod_data'),
    path('hod_dashboard/profile', views.profile, name='hod_dashboard/profile'),
    path('autocomplete', views.autocomplete, name='autocomplete'),
    path('autocomplete1', views.autocomplete1, name='autocomplete1'),
    path('autocomplete2', views.autocomplete2, name='autocomplete2'),
    path('user_dashboard',views.user_dashboard, name='user_dashboard'),
    path('userdata',views.userdata,name='userdata'),
    path('manager',views.manager,name='manager'),
    path('managerteam_data',views.managerteam_data,name='managerteam_data'),
    path('form_approved/<int:id>',views.form_approved,name='form_approved'),
    path('profile', views.profile,name='profile'),
    path('profile/change_password', views.change_password,name='change_password'),
    path('loginDemo/', views.loginDemo, name='loginDemo'),
    
]

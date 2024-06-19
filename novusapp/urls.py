from django.urls import path, include
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from .views import login_view, dashboard_redirect
from .import views
from api.xoxo.views import get_vouchers


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
    path('edit_respondent/<int:id>',views.edit_respondent,name='edit_respondent'),
    path('manager',views.manager,name='manager'),
    path('managerteam_data',views.managerteam_data,name='managerteam_data'),
    path('send-remark/<int:userid>/<int:respondentid>',views.sendremark,name='remark'),
    path('form_approved/<int:id>',views.form_approved,name='form_approved'),
    path('profile', views.profile,name='profile'),
    path('profile/change_password', views.change_password,name='change_password'),
    path('loginDemo/', views.loginDemo, name='loginDemo'),
    path('send_email',views.send_email, name="send_email"),
    path('reset-password/<str:token>/', views.reset_password_view, name="reset-password"),
    path('payment-page/', views.payment_page, name='payment_page'),
    path('process-payment/<int:pk>/', views.process_payment, name='process_payment'),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_cancelled, name='payment_cancelled'),
    
###############################Payment URL##################################################################    
    path('xoxo_login/', views.xoxo_login, name='xoxo_login'),
    path('xoday_payment/', views.process_xoxo_day_payment, name='xoxo_day_payment'),
    path('api/xoxo/vouchers/', get_vouchers, name='get_vouchers'),
    path('vouchers/dropdown/', views.voucher_dropdown_view, name='voucher_dropdown'),
    path('place_order/', views.place_order, name='place_order')

    
]

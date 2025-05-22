from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login/', views.login_view, name='login'),
    # path('register/', views.register_view, name='register'),
    # path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    # path('reset-password/', views.reset_password_view, name='reset_password'),
    path('login/', auth_views.LoginView.as_view(template_name='adminpanel/login.html'), name='admin_login'),
    # path('register/', views.admin_register, name='admin_register'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='admin_login'), name='admin_logout'),
]
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='user_login'),
    path('logout/', views.logout_view, name='_user_logout'),
    path('register/', views.register_view, name='user_register'),
    path('dashboard/', login_required(views.dashboard_view), name='user_dashboard'),
    path('my-bookings/', login_required(views.my_bookings_view), name='my_bookings'),
    path('wishlist/', login_required(views.wishlist_view), name='wishlist'),
    path('donations/', login_required(views.donations_view), name='donations'),
    path('events/', login_required(views.events_view), name='events'),
    path('notifications/', login_required(views.notifications_view), name='notifications'),
    path('account-settings/', login_required(views.account_settings_view), name='account_settings'),
    path('about/', views.about_view, name='about'),

    path('accounts/password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='frontend/pages/password_reset.html'
         ), 
         name='password_reset'),
]
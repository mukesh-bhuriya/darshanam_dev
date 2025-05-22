from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='user_login'),
    path('register/', views.register_view, name='user_register'),
    path('dashboard/', login_required(views.dashboard_view), name='user_dashboard'),
    path('my-bookings/', login_required(views.my_bookings_view), name='my_bookings'),
    path('wishlist/', login_required(views.wishlist_view), name='wishlist'),
    path('donations/', login_required(views.donations_view), name='donations'),
    path('events/', login_required(views.events_view), name='events'),
    path('notifications/', login_required(views.notifications_view), name='notifications'),
    path('account-settings/', login_required(views.account_settings_view), name='account_settings'),
    path('about/', views.about_view, name='about'),
]
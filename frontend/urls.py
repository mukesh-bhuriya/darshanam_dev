from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', login_required(views.dashboard_view), name='dashboard'),
    path('about/', views.about_view, name='about'),
]
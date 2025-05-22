from django.contrib import admin
from .models import Temple, Muhurat, Category, Event  # Add all your models here

# Create a custom admin site class (use Django's AdminSite, not AdminLTE3AdminSite)
class MyAdminSite(admin.AdminSite):
    site_header = "Darshanam Admin"
    site_title = "Darshanam Dashboard"
    index_title = "Welcome, Admin"

# Instantiate the custom admin site
admin_site = MyAdminSite(name='myadmin')

# Register your models
admin_site.register(Temple)
admin_site.register(Muhurat)
admin_site.register(Category)
admin_site.register(Event)

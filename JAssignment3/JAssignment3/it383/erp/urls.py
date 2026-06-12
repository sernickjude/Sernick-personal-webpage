from django.contrib import admin
from django.urls import path, include
from core.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', include('core.urls')),  # Assignment 2: includes asset and maintenance URLs
]

from django.urls import path
from core.views import asset_list_view, MaintenanceCreateView, export_assets_csv

urlpatterns = [
    path('assets/export/', export_assets_csv, name='export_assets_csv'),  # Part 3 - must come first
    path('assets/', asset_list_view, name='asset_list'),
    path('asset/<pk>/maintain/', MaintenanceCreateView.as_view(), name='maintenance_create'),
]

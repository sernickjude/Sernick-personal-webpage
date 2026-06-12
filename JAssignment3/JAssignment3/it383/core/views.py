import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.db.models import Sum, Avg, Count, Value
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.http import HttpResponse
from core.models import *

# Create your views here.

# --- Assignment 1: Dashboard view ---
def dashboard_view(request):
    stats = Project.objects.aggregate(
        total_budget=Sum('budget'),
        avg_budget=Avg('budget'),
        project_count=Count('id')
    )

    recent_assets = Asset.objects.select_related('assigned_to').all()[:5]

    # Cost grouped by department
    dept_costs = (
        Department.objects
        .annotate(total_cost=Sum('users__assets__cost'))
        .values('name', 'total_cost')
        .order_by('-total_cost')
    )

    context = {
        'stats': stats,
        'recent_assets': recent_assets,
        'dept_costs': dept_costs,
    }

    return render(request, 'core/dashboard.html', context)


# --- Assignment 2 + 3 Part 1: Asset list with pagination ---
def asset_list_view(request):
    # annotate adds a calculated 'repair_total' field to each asset
    # Coalesce replaces NULL with 0.00 when there are no maintenance logs
    assets_qs = Asset.objects.select_related('assigned_to').annotate(
        repair_total=Coalesce(Sum('maintenance_logs__cost'), Value(0, output_field=models.DecimalField()))
    )

    # Part 1: Paginate — 5 assets per page
    paginator = Paginator(assets_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/asset_list.html', {'page_obj': page_obj})


# --- Assignment 2: Add a maintenance log for a specific asset ---
class MaintenanceCreateView(CreateView):
    model = MaintenanceLog
    fields = ['description', 'cost', 'service_date']
    template_name = 'core/maintenance_form.html'

    def form_valid(self, form):
        # Auto-assign the asset from the URL (pk = asset's primary key)
        form.instance.asset = get_object_or_404(Asset, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('asset_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass asset info to the template so we can show its name
        context['asset'] = get_object_or_404(Asset, pk=self.kwargs['pk'])
        return context


# --- Assignment 3 Part 3: CSV Export ---
def export_assets_csv(request):
    # Tell the browser this is a downloadable file, not a webpage
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="asset_report.csv"'

    writer = csv.writer(response)

    # Header row
    writer.writerow(['Asset Name', 'Type', 'Cost', 'Assigned User'])

    # Data rows — one per asset
    assets = Asset.objects.select_related('assigned_to').all()
    for asset in assets:
        writer.writerow([
            asset.name,
            asset.serial_number,          # using serial_number as "Type" identifier
            asset.cost,
            asset.assigned_to.username if asset.assigned_to else 'Unassigned',
        ])

    return response

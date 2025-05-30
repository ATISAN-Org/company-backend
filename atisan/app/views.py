# app/views.py

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Investor, Project, Investment

@staff_member_required
def dashboard_view(request):
    return render(request, 'admin/dashboard.html', {
        'investors': Investor.objects.count(),
        'projects': Project.objects.count(),
        'total_investments': Investment.objects.count(),
        'total_amount': Investment.objects.aggregate(total=models.Sum('amount'))['total'] or 0,
    })

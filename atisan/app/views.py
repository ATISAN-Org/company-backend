# app/views.py
from pyexpat.errors import messages

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,redirect
from .models import Investor, Project, Investment
import django.db.models as models
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout



@staff_member_required
def dashboard_view(request):
    return render(request, 'admin/dashboard.html', {
        'investors': Investor.objects.count(),
        'projects': Project.objects.count(),
        'total_investments': Investment.objects.count(),
        'total_amount': Investment.objects.aggregate(total=models.Sum('amount'))['total'] or 0,
    })
def create_investment_view(request):
    if request.method == 'POST':
        investor_id = request.POST.get('investor')
        project_id = request.POST.get('project')
        amount = request.POST.get('amount')

        if not all([investor_id, project_id, amount]):
            messages.error(request, "All fields are required.")
            return redirect('create-investment')

        try:
            investor = Investor.objects.get(id=investor_id)
            project = Project.objects.get(id=project_id)
            Investment.objects.create(
                investor=investor,
                project=project,
                amount=amount
            )
            messages.success(request, "Investment recorded successfully!")
            return redirect('create-investment')
        except (Investor.DoesNotExist, Project.DoesNotExist):
            messages.error(request, "Invalid investor or project.")
            return redirect('create-investment')

    # For GET requests
    projects = Project.objects.all()
    investors = Investor.objects.all()
    return render(request, 'investor/investment_form.html', {
        'projects': projects,
        'investors': investors
    })

def home_view(request):
    return render(request, 'admin/home.html')

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def investment_reports_view(request):
    investments = Investment.objects.select_related('investor', 'project').all()
    return render(request, 'investor/reports.html', {
        'investments': investments
    })

from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InvestmentForm
from .models import Investor, InvestmentReport, Project, Investment


@login_required
def home_view(request):
    user = request.user
    try:
        investor = user.investor
    except Investor.DoesNotExist:
        investor = None

    # Show all active projects (for all investors)
    projects = Project.objects.filter(is_active=True)

    # Investors — show only logged-in investor info (so investor sees only themselves)
    investors_with_totals = []
    if investor:
        total = Investment.objects.filter(investor=investor).aggregate(s=Sum('amount'))['s'] or 0
        investors_with_totals.append({
            'username': investor.user.username if investor.user else investor.name,
            'email': investor.email,
            'total_invested': total,
        })

    # Overall total investments amount across all investors (optional)
    total_investments = Investment.objects.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'projects': projects,
        'investors': investors_with_totals,
        'total_investments': total_investments,
    }
    return render(request, 'investor/home.html', context)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_investment(request):
    try:
        investor = request.user.investor
    except Investor.DoesNotExist:
        raise Http404("Investor profile not found.")

    if request.method == "POST":
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.investor = investor
            investment.save()
            return redirect('dashboard')
    else:
        form = InvestmentForm()

    return render(request, 'investor/create_investment.html', {'form': form})

@login_required
def investor_dashboard(request):
    try:
        investor = Investor.objects.get(user=request.user)
    except Investor.DoesNotExist:
        raise Http404("Investor profile not found for the logged in user.")

    investments = investor.investments.select_related('project')
    total_invested = investments.aggregate(Sum('amount'))['amount__sum'] or 0
    reports = InvestmentReport.objects.filter(investment__in=investments)
    notifications = investor.notifications.all()
    return render(request, 'investor/dashboard.html', {
        'investor': investor,
        'investments': investments,
        'total_invested': total_invested,
        'reports': reports,
        'notifications': notifications,
    })

@login_required
def project_detail_view(request, pk):
    project = get_object_or_404(Project, pk=pk, is_active=True)

    # Get all investments for this project
    investments = Investment.objects.filter(project=project).select_related('investor')

    total_raised = investments.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'project': project,
        'investments': investments,
        'total_raised': total_raised,
    }
    return render(request, 'investor/project_detail.html', context)
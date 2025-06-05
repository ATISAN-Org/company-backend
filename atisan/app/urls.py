from django.urls import path
from . import views
from .views import create_investment_view, logout_view, investment_reports_view

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.home_view, name='home'),
    path('invest/', create_investment_view, name='create-investment'),
    path('reports/', investment_reports_view, name='investment-reports'),
    path('login/', views.login, name='login'),
    path('logout/', logout_view, name='logout'),
]

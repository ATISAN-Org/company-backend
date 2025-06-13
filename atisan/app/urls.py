from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
      path('', views.home_view, name='home'),
      path('project/<int:pk>/', views.project_detail_view, name='project_detail'),
      path('login/', views.login_view, name='login'),
      path('dashboard/', views.investor_dashboard, name='dashboard'),
      path('logout/', views.logout_view, name='logout'),
      path('invest/create/', views.create_investment, name='create-investment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

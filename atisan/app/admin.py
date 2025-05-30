# app/admin.py

from django.contrib import admin
from .models import Investor, Project, Investment, InvestmentReport

@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email')
    ordering = ('-created_at',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'investor', 'created_at')
    search_fields = ('title',)
    list_filter = ('investor',)

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('investor', 'project', 'amount', 'date')
    list_filter = ('project',)
    search_fields = ('investor__name', 'project__title')

@admin.register(InvestmentReport)
class InvestmentReportAdmin(admin.ModelAdmin):
    list_display = ('investment', 'report_date')
    search_fields = ('investment__investor__name',)

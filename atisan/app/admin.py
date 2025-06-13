from django.contrib import admin
from .models import Investor, Project, Investment, InvestmentReport, Notification, Transaction
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
import string


def generate_random_password(length=10):
    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(length))


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'investor_type', 'is_active', 'created_at')
    search_fields = ('name', 'email', 'nid')
    list_filter = ('investor_type', 'is_active')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            username = obj.email
            try:
                password = User.objects.make_random_password()
            except AttributeError:
                # Fallback if that method is missing
                password = generate_random_password()

            user = User.objects.create_user(username=username, email=obj.email, password=password)
            obj.user = user
            send_mail(
                'Your Investor Portal Access',
                f"Hello {obj.name},\n\nYour login credentials:\nUsername: {username}\nPassword: {password}",
                'noreply@yourdomain.com',
                [obj.email],
                fail_silently=False,
            )
        super().save_model(request, obj, form, change)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'amount_required', 'amount_raised', 'is_active', 'created_at')
    search_fields = ('title',)
    list_filter = ('category', 'status', 'is_active')


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('investor', 'project', 'amount','investment_type', 'date')
    list_filter = ('project',)
    search_fields = ('investor__name', 'project__title')
    ordering = ('-date',)


@admin.register(InvestmentReport)
class InvestmentReportAdmin(admin.ModelAdmin):
    list_display = ('investment', 'report_date')
    search_fields = ('investment__investor__name', 'investment__project__title')
    ordering = ('-report_date',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('investor', 'title', 'is_read', 'sent_at')
    list_filter = ('is_read',)
    search_fields = ('investor__name', 'title')
    ordering = ('-sent_at',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'investment', 'payment_method', 'amount', 'status', 'transaction_date')
    list_filter = ('payment_method', 'status')
    search_fields = ('transaction_id', 'investment__investor__name', 'investment__project__title')
    ordering = ('-transaction_date',)

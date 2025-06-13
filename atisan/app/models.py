from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Investor(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]

    INVESTOR_TYPE_CHOICES = [
        ('Regular', 'Regular'),
        ('Premium', 'Premium'),
        ('VIP', 'VIP'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investor', blank=True, null=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='investor_photos/', blank=True, null=True)

    nid = models.CharField(max_length=20, unique=True)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)

    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)
    spouse_name = models.CharField(max_length=250, blank=True, null=True)

    passport = models.CharField(max_length=250, blank=True, null=True)
    nominee = models.CharField(max_length=250, blank=True, null=True)

    present_address = models.CharField(max_length=250)
    permanent_address = models.CharField(max_length=250)

    investor_type = models.CharField(max_length=20, choices=INVESTOR_TYPE_CHOICES, default='Regular')
    total_invested = models.DecimalField(max_digits=15,decimal_places=2,default=0,null=True,blank=True)

    current_working_place = models.CharField(max_length=250, blank=True, null=True)
    department = models.CharField(max_length=250, blank=True, null=True)
    designation = models.CharField(max_length=250, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    joining_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class Project(models.Model):
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    CATEGORY_CHOICES = [
        ('Agriculture', 'Agriculture'),
        ('Technology', 'Technology'),
        ('Real Estate', 'Real Estate'),
        ('Retail', 'Retail'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    investors = models.ManyToManyField(Investor, related_name='projects')

    location = models.CharField(max_length=255, blank=True, null=True)

    amount_required = models.DecimalField(max_digits=15, decimal_places=2)
    amount_raised = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planned')
    is_active = models.BooleanField(default=True)

    document = models.FileField(upload_to='project_documents/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Investment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Bank Transfer', 'Bank Transfer'),
        ('Credit Card', 'Credit Card'),
        ('Mobile Payment', 'Mobile Payment'),
        ('Cash', 'Cash'),
        ('Other', 'Other'),
    ]
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='investments')
    investor = models.ForeignKey('Investor', on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    investment_type = models.CharField(max_length=50,choices=PAYMENT_METHOD_CHOICES,default='Bank Transfer')
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if not is_new:
            old = Investment.objects.get(pk=self.pk)
            amount_diff = self.amount - old.amount
            self.project.amount_raised += amount_diff
            self.investor.total_invested += amount_diff
        else:
            self.project.amount_raised += self.amount
            self.investor.total_invested += self.amount

        self.project.save()
        self.investor.save()
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.project.amount_raised -= self.amount
        self.investor.total_invested -= self.amount
        self.project.save()
        self.investor.save()
        super().delete(*args, **kwargs)


    def __str__(self):
        return f"{self.investor.name} invested {self.amount} in {self.project.title}"

    class Meta:
        ordering = ['-date']
        verbose_name = "Investment"
        verbose_name_plural = "Investments"

        def __str__(self):
            return f"{self.investor.name} invested {self.amount} in {self.project.title}"



class InvestmentReport(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name='reports')
    report_date = models.DateTimeField(auto_now_add=True)
    report_content = models.TextField()

    def __str__(self):
        return f"Report for {self.investment.investor.name} on {self.report_date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-report_date']
        verbose_name = "Investment Report"
        verbose_name_plural = "Investment Reports"

class Notification(models.Model):
    investor = models.ForeignKey('Investor', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.investor.name}: {self.title}"

    class Meta:
        ordering = ['-sent_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"


class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Bank Transfer', 'Bank Transfer'),
        ('Credit Card', 'Credit Card'),
        ('Mobile Payment', 'Mobile Payment'),
        ('Cash', 'Cash'),
        ('Other', 'Other'),
    ]

    TRANSACTION_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
    ]

    investment = models.ForeignKey('Investment', on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, default='Pending')
    transaction_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"

    class Meta:
        ordering = ['-transaction_date']
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

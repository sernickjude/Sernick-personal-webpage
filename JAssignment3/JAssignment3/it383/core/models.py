import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class TimeStampModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Assignment 1: Department model
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    def __str__(self):
        return f"{self.username} - {self.employee_id}"

class Asset(TimeStampModel):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, unique=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assets')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

# Assignment 2: MaintenanceLog model — one Asset can have many logs
class MaintenanceLog(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_logs')
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    service_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Maintenance on {self.asset.name} - ${self.cost}"

class Organization(TimeStampModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Project(TimeStampModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name

class LeaveRequest(TimeStampModel):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    reason = models.TextField()
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approvals')
    is_approved = models.BooleanField(default=False)

class Product(TimeStampModel):
    name = models.CharField(max_length=100)
    stock_qty = models.IntegerField(default=0)

class Warehouse(TimeStampModel):
    location = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='StockMovement')

class StockMovement(TimeStampModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.IntegerField(help_text='Positive to add, negative to remove')
    notes = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        self.product.stock_qty += self.quantity
        self.product.save()
        super().save(*args, **kwargs)

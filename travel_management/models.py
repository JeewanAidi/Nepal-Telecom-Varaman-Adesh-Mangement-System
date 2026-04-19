"""
models.py - Nepal Telecom Travel Management System
Defines Employee and TravelOrder database models.
"""

from django.db import models
from django.utils import timezone
from datetime import date


class Department(models.Model):
    """Departments in Nepal Telecom Mahendranagar Branch"""
    name = models.CharField(max_length=200, unique=True, verbose_name="विभाग")

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['name']

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Employee model for Nepal Telecom staff"""

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="कर्मचारी नं."
    )
    name = models.CharField(max_length=200, verbose_name="नाम")
    name_nepali = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="नाम (नेपाली)"
    )
    position = models.CharField(max_length=200, verbose_name="पद")
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="विभाग"
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="फोन")
    email = models.EmailField(blank=True, null=True, verbose_name="इमेल")
    is_active = models.BooleanField(default=True, verbose_name="सक्रिय")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ['name']

    def __str__(self):
        return f"{self.employee_id} - {self.name}"

    def get_department_name(self):
        return self.department.name if self.department else "N/A"


class TravelOrder(models.Model):
    """
    Travel Order (भ्रमण आदेश) model - Main feature of the system.
    Stores all travel order details for Nepal Telecom employees.
    """

    STATUS_CHOICES = [
        ('Pending', 'Pending - बाँकी'),
        ('Active', 'Active - सक्रिय'),
        ('Completed', 'Completed - सम्पन्न'),
        ('Cancelled', 'Cancelled - रद्द'),
    ]

    TRANSPORT_CHOICES = [
        ('Bus', 'Bus - बस'),
        ('Jeep', 'Jeep - जीप'),
        ('Motorcycle', 'Motorcycle - मोटरसाइकल'),
        ('Car', 'Car - कार'),
        ('Office Vehicle', 'Office Vehicle - कार्यालय सवारी'),
        ('Hired Vehicle', 'Hired Vehicle - भाडाको सवारी'),
        ('Other', 'Other - अन्य'),
    ]

    # Auto-generated Order ID (NTC-YYYY-0001 format)
    order_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        verbose_name="आदेश नं."
    )

    # Date of order issue
    date = models.DateField(
        default=date.today,
        verbose_name="मिति"
    )

    # Employee reference
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name="कर्मचारी"
    )

    # Travel details
    travel_location = models.CharField(
        max_length=500,
        verbose_name="भ्रमण स्थान"
    )
    purpose = models.TextField(
        verbose_name="भ्रमणको उद्देश्य"
    )
    from_date = models.DateField(verbose_name="मिति देखि")
    to_date = models.DateField(verbose_name="मिति सम्म")

    # Transport details
    transport_type = models.CharField(
        max_length=50,
        choices=TRANSPORT_CHOICES,
        verbose_name="यातायातको साधन"
    )
    vehicle_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="सवारी नं."
    )

    # Work description
    work_description = models.TextField(
        verbose_name="गर्नुपर्ने काम विवरण"
    )

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending',
        verbose_name="स्थिति"
    )

    # Approval
    approved_by = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="स्वीकृत गर्ने अधिकारी"
    )
    remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name="कैफियत"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Travel Order"
        verbose_name_plural = "Travel Orders"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_id} - {self.employee.name}"

    def get_duration_days(self):
        """Calculate trip duration in days"""
        if self.from_date and self.to_date:
            return (self.to_date - self.from_date).days + 1
        return 0

    def save(self, *args, **kwargs):
        """Auto-generate Order ID before saving"""
        if not self.order_id:
            self.order_id = self._generate_order_id()
        super().save(*args, **kwargs)

    def _generate_order_id(self):
        """Generate Order ID in format NTC-YYYY-NNNN"""
        year = timezone.now().year
        # Get last order for this year
        last_order = TravelOrder.objects.filter(
            order_id__startswith=f'NTC-{year}-'
        ).order_by('-order_id').first()

        if last_order:
            try:
                last_num = int(last_order.order_id.split('-')[-1])
                new_num = last_num + 1
            except (ValueError, IndexError):
                new_num = 1
        else:
            new_num = 1

        return f'NTC-{year}-{new_num:04d}'

    def get_status_badge(self):
        """Return Bootstrap badge class for status"""
        badge_map = {
            'Pending': 'warning',
            'Active': 'primary',
            'Completed': 'success',
            'Cancelled': 'danger',
        }
        return badge_map.get(self.status, 'secondary')

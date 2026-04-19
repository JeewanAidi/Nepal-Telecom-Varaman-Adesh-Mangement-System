"""
admin.py - Register models with Django admin
"""

from django.contrib import admin
from .models import Employee, TravelOrder, Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'name', 'position', 'department', 'is_active']
    list_filter = ['department', 'is_active']
    search_fields = ['name', 'employee_id', 'position']


@admin.register(TravelOrder)
class TravelOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'employee', 'travel_location', 'from_date', 'to_date', 'status']
    list_filter = ['status', 'transport_type', 'employee__department']
    search_fields = ['order_id', 'employee__name', 'travel_location']
    date_hierarchy = 'date'
    readonly_fields = ['order_id', 'created_at', 'updated_at']

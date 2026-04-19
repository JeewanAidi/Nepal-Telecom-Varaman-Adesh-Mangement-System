"""
views.py - Nepal Telecom Travel Management System
All view functions for the application.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count
from django.utils import timezone
from django.template.loader import render_to_string
from datetime import date
import json

from .models import Employee, TravelOrder, Department
from .forms import (
    LoginForm, EmployeeForm, TravelOrderForm,
    TravelOrderFilterForm, DepartmentForm
)


# ─────────────────────────────────────────────
# AUTH VIEWS
# ─────────────────────────────────────────────

def login_view(request):
    """Login page view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────

@login_required
def dashboard(request):
    """Main dashboard with statistics"""
    total_orders = TravelOrder.objects.count()
    active_trips = TravelOrder.objects.filter(status='Active').count()
    completed_trips = TravelOrder.objects.filter(status='Completed').count()
    pending_trips = TravelOrder.objects.filter(status='Pending').count()
    cancelled_trips = TravelOrder.objects.filter(status='Cancelled').count()
    total_employees = Employee.objects.filter(is_active=True).count()

    # Recent travel orders (last 5)
    recent_orders = TravelOrder.objects.select_related('employee', 'employee__department').order_by('-created_at')[:5]

    # Department-wise stats
    dept_stats = Department.objects.annotate(
        order_count=Count('employee__travelorder')
    ).order_by('-order_count')[:5]

    # This month's orders
    today = date.today()
    this_month_orders = TravelOrder.objects.filter(
        date__year=today.year,
        date__month=today.month
    ).count()

    context = {
        'total_orders': total_orders,
        'active_trips': active_trips,
        'completed_trips': completed_trips,
        'pending_trips': pending_trips,
        'cancelled_trips': cancelled_trips,
        'total_employees': total_employees,
        'recent_orders': recent_orders,
        'dept_stats': dept_stats,
        'this_month_orders': this_month_orders,
    }
    return render(request, 'dashboard/dashboard.html', context)


# ─────────────────────────────────────────────
# EMPLOYEE VIEWS
# ─────────────────────────────────────────────

@login_required
def employee_list(request):
    """List all employees with search"""
    search = request.GET.get('search', '')
    dept_filter = request.GET.get('department', '')

    employees = Employee.objects.select_related('department').all()

    if search:
        employees = employees.filter(
            Q(name__icontains=search) |
            Q(employee_id__icontains=search) |
            Q(position__icontains=search)
        )

    if dept_filter:
        employees = employees.filter(department__id=dept_filter)

    departments = Department.objects.all()

    context = {
        'employees': employees,
        'departments': departments,
        'search': search,
        'dept_filter': dept_filter,
    }
    return render(request, 'employees/employee_list.html', context)


@login_required
def employee_add(request):
    """Add new employee"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee "{employee.name}" added successfully!')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm()

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Add Employee',
        'action': 'Add',
    })


@login_required
def employee_edit(request, pk):
    """Edit existing employee"""
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employee "{employee.name}" updated successfully!')
            return redirect('employee_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employees/employee_form.html', {
        'form': form,
        'title': 'Edit Employee',
        'action': 'Update',
        'employee': employee,
    })


@login_required
def employee_delete(request, pk):
    """Delete employee (admin only)"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete employees.')
        return redirect('employee_list')

    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        name = employee.name
        employee.delete()
        messages.success(request, f'Employee "{name}" deleted successfully!')
        return redirect('employee_list')

    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})


@login_required
def employee_detail(request, pk):
    """View employee details"""
    employee = get_object_or_404(Employee, pk=pk)
    travel_orders = TravelOrder.objects.filter(employee=employee).order_by('-date')

    return render(request, 'employees/employee_detail.html', {
        'employee': employee,
        'travel_orders': travel_orders,
    })


@login_required
def get_employee_data(request, pk):
    """AJAX: Return employee data as JSON for auto-fill"""
    employee = get_object_or_404(Employee, pk=pk)
    data = {
        'name': employee.name,
        'name_nepali': employee.name_nepali or '',
        'position': employee.position,
        'department': employee.get_department_name(),
        'department_id': employee.department.id if employee.department else '',
        'employee_id': employee.employee_id,
        'phone': employee.phone or '',
        'email': employee.email or '',
    }
    return JsonResponse(data)


# ─────────────────────────────────────────────
# DEPARTMENT VIEWS
# ─────────────────────────────────────────────

@login_required
def department_list(request):
    """List all departments"""
    departments = Department.objects.annotate(
        employee_count=Count('employee')
    ).all()
    return render(request, 'employees/department_list.html', {'departments': departments})


@login_required
def department_add(request):
    """Add new department"""
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f'Department "{dept.name}" added!')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'employees/department_form.html', {'form': form})


@login_required
def department_delete(request, pk):
    """Delete department"""
    dept = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        dept.delete()
        messages.success(request, 'Department deleted.')
        return redirect('department_list')
    return render(request, 'employees/department_confirm_delete.html', {'dept': dept})


# ─────────────────────────────────────────────
# TRAVEL ORDER VIEWS
# ─────────────────────────────────────────────

@login_required
def travel_order_list(request):
    """List all travel orders with filtering"""
    filter_form = TravelOrderFilterForm(request.GET)
    orders = TravelOrder.objects.select_related(
        'employee', 'employee__department'
    ).all()

    if filter_form.is_valid():
        data = filter_form.cleaned_data

        # Date range filter
        if data.get('date_from'):
            orders = orders.filter(from_date__gte=data['date_from'])
        if data.get('date_to'):
            orders = orders.filter(to_date__lte=data['date_to'])

        # Employee filter
        if data.get('employee'):
            orders = orders.filter(employee=data['employee'])

        # Department filter
        if data.get('department'):
            orders = orders.filter(employee__department=data['department'])

        # Status filter
        if data.get('status'):
            orders = orders.filter(status=data['status'])

        # Search
        if data.get('search'):
            search_term = data['search']
            orders = orders.filter(
                Q(order_id__icontains=search_term) |
                Q(travel_location__icontains=search_term) |
                Q(employee__name__icontains=search_term) |
                Q(purpose__icontains=search_term)
            )

    orders = orders.order_by('-date', '-created_at')

    context = {
        'orders': orders,
        'filter_form': filter_form,
        'total_count': orders.count(),
    }
    return render(request, 'travel/travel_order_list.html', context)


@login_required
def travel_order_create(request):
    """Create a new travel order"""
    if request.method == 'POST':
        form = TravelOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, f'Travel Order "{order.order_id}" created successfully!')
            return redirect('travel_order_detail', pk=order.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TravelOrderForm(initial={'date': date.today()})

    # Pass employees JSON for auto-fill
    employees_data = {}
    for emp in Employee.objects.filter(is_active=True).select_related('department'):
        employees_data[str(emp.pk)] = {
            'name': emp.name,
            'name_nepali': emp.name_nepali or '',
            'position': emp.position,
            'department': emp.get_department_name(),
            'employee_id': emp.employee_id,
        }

    context = {
        'form': form,
        'title': 'Create Travel Order / नयाँ भ्रमण आदेश',
        'action': 'Create',
        'employees_json': json.dumps(employees_data),
    }
    return render(request, 'travel/travel_order_form.html', context)


@login_required
def travel_order_detail(request, pk):
    """View travel order details"""
    order = get_object_or_404(
        TravelOrder.objects.select_related('employee', 'employee__department'),
        pk=pk
    )
    return render(request, 'travel/travel_order_detail.html', {'order': order})


@login_required
def travel_order_edit(request, pk):
    """Edit existing travel order"""
    order = get_object_or_404(TravelOrder, pk=pk)

    if request.method == 'POST':
        form = TravelOrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            messages.success(request, f'Travel Order "{order.order_id}" updated!')
            return redirect('travel_order_detail', pk=order.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TravelOrderForm(instance=order)

    employees_data = {}
    for emp in Employee.objects.filter(is_active=True).select_related('department'):
        employees_data[str(emp.pk)] = {
            'name': emp.name,
            'name_nepali': emp.name_nepali or '',
            'position': emp.position,
            'department': emp.get_department_name(),
            'employee_id': emp.employee_id,
        }

    context = {
        'form': form,
        'title': f'Edit Travel Order - {order.order_id}',
        'action': 'Update',
        'order': order,
        'employees_json': json.dumps(employees_data),
    }
    return render(request, 'travel/travel_order_form.html', context)


@login_required
def travel_order_delete(request, pk):
    """Delete travel order"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete travel orders.')
        return redirect('travel_order_list')

    order = get_object_or_404(TravelOrder, pk=pk)

    if request.method == 'POST':
        order_id = order.order_id
        order.delete()
        messages.success(request, f'Travel Order "{order_id}" deleted.')
        return redirect('travel_order_list')

    return render(request, 'travel/travel_order_confirm_delete.html', {'order': order})


@login_required
def travel_order_print(request, pk):
    """Print-friendly view for भ्रमण आदेश"""
    order = get_object_or_404(
        TravelOrder.objects.select_related('employee', 'employee__department'),
        pk=pk
    )
    return render(request, 'travel/travel_order_print.html', {'order': order})


@login_required
def travel_order_status_update(request, pk):
    """AJAX: Quick status update"""
    if request.method == 'POST':
        order = get_object_or_404(TravelOrder, pk=pk)
        new_status = request.POST.get('status')
        valid_statuses = [s[0] for s in TravelOrder.STATUS_CHOICES]
        if new_status in valid_statuses:
            order.status = new_status
            order.save()
            return JsonResponse({'success': True, 'status': new_status})
    return JsonResponse({'success': False}, status=400)

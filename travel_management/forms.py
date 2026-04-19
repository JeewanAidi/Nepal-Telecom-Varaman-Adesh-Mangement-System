"""
forms.py - Nepal Telecom Travel Management System
Django forms for Employee and TravelOrder models.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Employee, TravelOrder, Department


class LoginForm(AuthenticationForm):
    """Custom login form with Bootstrap styling"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )


class DepartmentForm(forms.ModelForm):
    """Form for adding/editing departments"""
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Name'}),
        }


class EmployeeForm(forms.ModelForm):
    """Form for adding/editing employee details"""

    class Meta:
        model = Employee
        fields = [
            'employee_id', 'name', 'name_nepali',
            'position', 'department', 'phone', 'email', 'is_active'
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. NTC-001'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name (English)'
            }),
            'name_nepali': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'पूरा नाम (नेपाली)'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Junior Engineer'
            }),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@ntc.net.np'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'employee_id': 'Employee ID (कर्मचारी नं.)',
            'name': 'Full Name (नाम)',
            'name_nepali': 'Name in Nepali (नेपाली नाम)',
            'position': 'Position (पद)',
            'department': 'Department (विभाग)',
            'phone': 'Phone (फोन)',
            'email': 'Email (इमेल)',
            'is_active': 'Active Employee',
        }


class TravelOrderForm(forms.ModelForm):
    """Form for creating/editing travel orders (भ्रमण आदेश)"""

    class Meta:
        model = TravelOrder
        fields = [
            'date', 'employee', 'travel_location', 'purpose',
            'from_date', 'to_date', 'transport_type', 'vehicle_number',
            'work_description', 'status', 'approved_by', 'remarks'
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'employee': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_employee',
                'onchange': 'autoFillEmployee(this.value)'
            }),
            'travel_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Kathmandu, Dhangadhi'
            }),
            'purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Purpose of travel / भ्रमणको उद्देश्य'
            }),
            'from_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'to_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'transport_type': forms.Select(attrs={'class': 'form-select'}),
            'vehicle_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Ba 1 Cha 2345'
            }),
            'work_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detailed work description / काम विवरण'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'approved_by': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Approving Officer Name'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Additional remarks / कैफियत'
            }),
        }
        labels = {
            'date': 'Order Date (मिति)',
            'employee': 'Employee (कर्मचारी)',
            'travel_location': 'Travel Location (भ्रमण स्थान)',
            'purpose': 'Purpose (उद्देश्य)',
            'from_date': 'From Date (मिति देखि)',
            'to_date': 'To Date (मिति सम्म)',
            'transport_type': 'Transport Type (यातायात)',
            'vehicle_number': 'Vehicle Number (सवारी नं.)',
            'work_description': 'Work Description (काम विवरण)',
            'status': 'Status (स्थिति)',
            'approved_by': 'Approved By (स्वीकृत गर्ने)',
            'remarks': 'Remarks (कैफियत)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active employees
        self.fields['employee'].queryset = Employee.objects.filter(is_active=True).order_by('name')


class TravelOrderFilterForm(forms.Form):
    """Form for filtering travel orders"""
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='From Date'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='To Date'
    )
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.filter(is_active=True).order_by('name'),
        required=False,
        empty_label='-- All Employees --',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Employee'
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all().order_by('name'),
        required=False,
        empty_label='-- All Departments --',
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Department'
    )
    status = forms.ChoiceField(
        choices=[('', '-- All Status --')] + TravelOrder.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Status'
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by Order ID or Location...'
        }),
        label='Search'
    )

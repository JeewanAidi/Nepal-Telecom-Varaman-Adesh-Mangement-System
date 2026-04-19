"""
Management command: seed_data
Seeds initial departments, sample employees, and an admin user.
This command is IDEMPOTENT — safe to run on every Render deploy.
Run: python manage.py seed_data
"""

import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from travel_management.models import Department, Employee


class Command(BaseCommand):
    help = 'Seed initial data: admin user, departments, sample employees (idempotent)'

    def handle(self, *args, **kwargs):
        self.stdout.write('\n Seeding initial data for NTC Travel Management System...\n')

        admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        admin_email    = os.environ.get('ADMIN_EMAIL', 'admin@ntc.net.np')

        # 1. Create or Update Admin User
        user, created = User.objects.get_or_create(username=admin_username)
        user.set_password(admin_password)
        user.email = admin_email
        user.first_name = 'System'
        user.last_name = 'Administrator'
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Admin user created: {admin_username} / {admin_password}'))
        else:
            self.stdout.write(self.style.WARNING(f'Admin user already exists ({admin_username}), password refreshed.'))

        # 2. Create Departments
        departments_data = [
            'Technical Division',
            'Commercial Division',
            'Finance & Administration',
            'Customer Service',
            'Network Operations',
            'Information Technology',
            'Human Resources',
            'Internal Audit',
        ]

        created_depts = {}
        for dept_name in departments_data:
            dept, created = Department.objects.get_or_create(name=dept_name)
            created_depts[dept_name] = dept
            if created:
                self.stdout.write(self.style.SUCCESS(f'Department created: {dept_name}'))

        # 3. Create Sample Employees
        sample_employees = [
            {
                'employee_id': 'NTC-001',
                'name': 'Ram Bahadur Thapa',
                'name_nepali': 'Ram Bahadur Thapa',
                'position': 'Branch Manager',
                'department': 'Finance & Administration',
                'phone': '9858012345',
                'email': 'ram.thapa@ntc.net.np',
            },
            {
                'employee_id': 'NTC-002',
                'name': 'Sita Kumari Sharma',
                'name_nepali': 'Sita Kumari Sharma',
                'position': 'Senior Engineer',
                'department': 'Technical Division',
                'phone': '9858023456',
                'email': 'sita.sharma@ntc.net.np',
            },
            {
                'employee_id': 'NTC-003',
                'name': 'Hari Prasad Adhikari',
                'name_nepali': 'Hari Prasad Adhikari',
                'position': 'Junior Engineer',
                'department': 'Network Operations',
                'phone': '9858034567',
                'email': 'hari.adhikari@ntc.net.np',
            },
            {
                'employee_id': 'NTC-004',
                'name': 'Gita Devi Panta',
                'name_nepali': 'Gita Devi Panta',
                'position': 'Account Officer',
                'department': 'Finance & Administration',
                'phone': '9858045678',
                'email': 'gita.panta@ntc.net.np',
            },
            {
                'employee_id': 'NTC-005',
                'name': 'Krishna Bahadur Bista',
                'name_nepali': 'Krishna Bahadur Bista',
                'position': 'Customer Service Officer',
                'department': 'Customer Service',
                'phone': '9858056789',
                'email': 'krishna.bista@ntc.net.np',
            },
            {
                'employee_id': 'NTC-006',
                'name': 'Laxmi Prasad Joshi',
                'name_nepali': 'Laxmi Prasad Joshi',
                'position': 'Technical Officer',
                'department': 'Technical Division',
                'phone': '9858067890',
                'email': 'laxmi.joshi@ntc.net.np',
            },
        ]

        for emp_data in sample_employees:
            dept_name = emp_data.pop('department')
            dept = created_depts.get(dept_name)
            emp, created = Employee.objects.get_or_create(
                employee_id=emp_data['employee_id'],
                defaults={**emp_data, 'department': dept}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Employee created: {emp.name} ({emp.employee_id})'))
            else:
                self.stdout.write(self.style.WARNING(f'Employee already exists: {emp.name}'))

        self.stdout.write(self.style.SUCCESS('\nData seeding complete!\n'))
        self.stdout.write(f'  Username : {admin_username}')
        self.stdout.write(f'  Password : {admin_password}\n')

"""
urls.py - Nepal Telecom Travel Management System
URL routing for all views.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('employees/<int:pk>/data/', views.get_employee_data, name='get_employee_data'),

    # Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/add/', views.department_add, name='department_add'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),

    # Travel Order URLs
    path('travel-orders/', views.travel_order_list, name='travel_order_list'),
    path('travel-orders/create/', views.travel_order_create, name='travel_order_create'),
    path('travel-orders/<int:pk>/', views.travel_order_detail, name='travel_order_detail'),
    path('travel-orders/<int:pk>/edit/', views.travel_order_edit, name='travel_order_edit'),
    path('travel-orders/<int:pk>/delete/', views.travel_order_delete, name='travel_order_delete'),
    path('travel-orders/<int:pk>/print/', views.travel_order_print, name='travel_order_print'),
    path('travel-orders/<int:pk>/status/', views.travel_order_status_update, name='travel_order_status'),
]

from django.shortcuts import redirect
from django.urls import path
from student.views import (
    student_registration,
    registration_success,
    student_login,
    student_logout,
    maintenance_request,
    request_success
)

app_name = 'student'

urlpatterns = [
    # Home page
    path('', student_login, name='home'),

    # Register
    path('register/', student_registration, name='student_registration'),
    path('registration-success/', registration_success, name='registration_success'),

    # Login/Logout
    path('login/', student_login, name='student_login'),
    path('logout/', student_logout, name='student_logout'),

    # Maintenance Request
    path('maintenance/', maintenance_request, name='maintenance_request'),
    path('request-success/', request_success, name='request_success'),
]
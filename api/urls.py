from django.contrib import admin
from django.urls import path
from .views import get_job_postings, get_departments, get_employee_profile, software_engineer, cloud_engineer

urlpatterns = [
    path('job_postings/', get_job_postings, name='job_postings'),
    path('departments/', get_departments, name='departments'),
    path('employee/<int:pk>/', get_employee_profile, name='employee'),
    path('software_engineer/', software_engineer, name='software_engineer'),
    path('cloud_engineer/', cloud_engineer, name='cloud_engineer'),
]
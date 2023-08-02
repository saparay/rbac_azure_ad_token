from django.contrib import admin
from .models import Department,Employee, JobPosting
# Register your models here.
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id','name']

admin.site.register(Department, DepartmentAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id','name','mail','role','age','salary','department']

admin.site.register(Employee, EmployeeAdmin)

class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','department']

admin.site.register(JobPosting, JobPostingAdmin)

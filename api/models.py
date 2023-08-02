from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'department'
        


class Employee(models.Model):
    name = models.CharField(max_length=20)
    mail = models.EmailField()
    role = models.CharField(max_length=20)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=8,decimal_places=2)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'employee'

class JobPosting(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'jobposting'
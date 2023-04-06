from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class Account(AbstractUser):

    email = models.EmailField(unique=True)
    is_auditee = models.BooleanField(default=False)
    is_auditor = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_other   = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
# Create your models here.




class UserRole(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    user_sector = models.ForeignKey("Employee",on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
     
     
   
class Position(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank= True)
    gender = models.CharField(max_length=10)
    employee_id = models.CharField(max_length=50, blank= True)
    inactive_employee = models.CharField(max_length=50, blank= True)
    start_date = models.DateField(default=datetime.now, blank=True)
    location = models.CharField(max_length=50, blank= True)
    position = models.ForeignKey("Position", on_delete=models.SET_NULL, null = True)
    department = models.CharField(max_length=50, blank= True)
    report_to = models.CharField(max_length=50, blank= True)
    mobile_number = models.CharField(max_length=50, blank= True)
    
    
    
    def __str__(self) -> str:
        return '{0} {1}'.format( self.first_name, self.last_name)
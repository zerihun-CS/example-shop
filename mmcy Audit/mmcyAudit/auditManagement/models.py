from django.db import models
from .models import *
    
class Criterion(models.Model):
    criterion_name  = models.CharField(max_length=100)
    project_required = models.BooleanField(default=True) 
    description_required = models.BooleanField(default=False)
    

    
    def __str__(self) -> str:
        return self.criterion_name   

class Measurement(models.Model):
   points = models.CharField(max_length=50)
    
   def __str__(self) -> str:
        return self.points  

class CriterionMeasurement(models.Model):
   tracker = models.ForeignKey(Criterion, on_delete=models.CASCADE)
   point = models.ForeignKey(Measurement, on_delete=models.CASCADE)
   notify = models.BooleanField(default=False)

   def __str__(self) -> str:
       return "{0}->{1}".format(self.tracker, self.point) 
     
     
class AccountManagerAudit(models.Model):
   criterion  =  models.ForeignKey(CriterionMeasurement, on_delete=models.CASCADE)
   project = models.ForeignKey("dataManagement.Project", on_delete=models.SET_NULL, null=True)
   auditor = models.ForeignKey("userManagement.Account",on_delete=models.CASCADE,)
   auditives = models.ForeignKey("userManagement.Employee",   on_delete=models.CASCADE,  related_name='auditee')
   date  = models.DateField()
   added_at = models.DateTimeField(auto_now=True)
   notice = models.BooleanField(default=False,)
   text_description = models.TextField(blank=True,null=True)
   
   image_uploaded = models.ImageField(blank=True,upload_to='screenshot/')
   
   def __str__(self) -> str:
       return "{0}".format(self.criterion.point)
   
   def return_criterion(self):
       return self.criterion.tracker.id


class DateRange(models.Model):
   start_date = models.DateField()
   ending_date = models.DateField()

   def __str__(self) -> str:
       return "{0},{1}".format(self.start_date, self.ending_date)


    
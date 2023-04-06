from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=50, blank =True, null=True)
    status = models.CharField(max_length=50, blank= True, null=True)
    mmcy_contact = models.CharField(max_length=50, blank= True, null=True)
    onenote_link = models.URLField(null=True, blank= True)
    resource_model = models.CharField(max_length=50, blank= True, null=True)
    additional_description = models.TextField(max_length=250, blank=True, null=True)
    def __str__(self) -> str:
        return self.name
     
     
class Project(models.Model): 
   project_title = models.CharField(max_length=150)
   members = models.ManyToManyField("userManagement.Employee")
   client = models.ForeignKey("Client", on_delete=models.CASCADE)
   estimation = models.CharField(max_length=50, null=True)
   total_hour = models.CharField(max_length=50, null=True)
   start_date = models.DateField(blank = True, null=True)
   launch_date = models.DateField(blank = True, null=True)
   first_draft_date = models.DateField(blank = True, null=True)
   status = models.BooleanField(default=True)
   
   def __str__(self) -> str:
        return self.project_title

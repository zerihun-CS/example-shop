from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render
from .models import Client,Project
import requests
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from auditManagement.models import AccountManagerAudit
from userManagement.models import Employee
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
# Create your views here.
from django.db.models import Count
import json
import random

@login_required
def index(request):
   emp_count = Employee.objects.all().count()
   client_count = Client.objects.all().count()
   project_count = Project.objects.all().count() 
   audits_data = AccountManagerAudit.objects.all().order_by('added_at')[:10]
   audit_count = AccountManagerAudit.objects.all().count() 
   
   project_counts = AccountManagerAudit.objects.filter(project__status = True).values('project__project_title').annotate(count=Count('project')).order_by('project__project_title')   
   # Extract the project names and their count values
   project_names = [project['project__project_title'] for project in project_counts]
   project_counts = [project['count'] for project in project_counts]   
   # Pass the data to the template

   data = AccountManagerAudit.objects.values('notice').annotate(count=Count('id'))
   chart_data = [{'name': 'True', 'y': 0}, {'name': 'False', 'y': 0}]
   for item in data:
        if item['notice']:
            chart_data[0]['y'] = item['count']
        else:
            chart_data[1]['y'] = item['count']


   audit_counts = AccountManagerAudit.objects.filter(project__status = True, notice = True).values('auditives__first_name', 'auditives__last_name').annotate(count=Count('id'))
   auditive_names = [f"{count['auditives__first_name']} {count['auditives__last_name']}" for count in audit_counts]
   audit_counts = [count['count'] for count in audit_counts]
   data = []
   for i in range(len(auditive_names)):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        data.append({
            'name': auditive_names[i],
            'value': audit_counts[i],
            'color':hex_color
        })
        
   data={'emp_count':emp_count,'client_count':client_count,'project_count':project_count,'audit_count':audit_count,'chart_data': chart_data,'project_names': json.dumps(project_names) ,'project_counts':json.dumps(project_counts),'data': data,'audits_data':audits_data }
   
   return render(request, "index.html", data)


class ClientListView(ListView):
    model = Client
    template_name = 'client_list.html'
        
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            # url = 'https://api.myintervals.com/client?active=true&projectsonly=true&limit=10'
            # headers = {'Accept': 'application/json'}
            # auth = ('7jprbtwij3w', 'B')
            # response = requests.get(url, headers=headers, auth=auth,)
            # context["interval_client"] = response.json()
            # print(response.json())
            return context
        

        
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):        
        return super(ClientListView, self).dispatch(request, *args, **kwargs)


class ClientCreateView(CreateView):
    model = Client
    template_name = 'client_create.html'
    fields = ('name', 'status', 'mmcy_contact', 'onenote_link','resource_model','additional_description')
    success_url = reverse_lazy('client_list_url')    
    
class ClientDetailView(DetailView):
    model = Client
    fields = ('name', 'type', 'active_project', 'hour_billable','hour_unbillable','additional_description')
    template_name = 'client_view.html'


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('name', 'status', 'mmcy_contact', 'onenote_link','resource_model','additional_description')
    template_name = 'client_detail.html'
    success_url = reverse_lazy('client_list_url') 
    
    
class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'client_delete.html'
    success_url = reverse_lazy('client_list_url') 
    

class ProjectListView(ListView):
    model = Project 
    template_name = 'project_list.html'  


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'project_create.html'
    fields = ('project_title', 'members', 'client', 'estimation','total_hour','start_date','launch_date','first_draft_date','status')
    success_url = reverse_lazy('project_list_url')    

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ('project_title', 'members', 'client', 'estimation','total_hour','start_date','launch_date','first_draft_date','status')
    template_name = 'project_detail.html'
    success_url = reverse_lazy('project_list_url') 

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project_delete.html'
    success_url = reverse_lazy('project_list_url') 

class ProjectDetailView(DetailView):
    model = Project
    fields = ('project_title', 'members', 'client', 'estimation','total_hour','start_date','launch_date','first_draft_date','status')
    template_name = 'project_view.html'
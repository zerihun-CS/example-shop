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


@login_required
def index(request):
   emp_count = Employee.objects.all().count()
   client_count = Client.objects.all().count()
   project_count = Project.objects.all().count() 
   audit_count = AccountManagerAudit.objects.all().count() 
   
   data={'emp_count':emp_count,'client_count':client_count,'project_count':project_count,'audit_count':audit_count}
   
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
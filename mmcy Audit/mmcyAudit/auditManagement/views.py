from django.shortcuts import render, get_object_or_404, redirect
from userManagement.models import Employee, Position
from dataManagement.models import Project, Client
from .models import *
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django.http import HttpResponse
import json
from django.http import HttpResponse
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from .helper import *
from django.core.cache import cache
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
# Create your views here.

def json_view(request,criterion_id=0,project_id=0,position_id=0):
  
    """
  json_view: This view returns a JSON response of data used to render an HTML table. 
  It takes criterion_id, project_id, 
  and position_id as parameters. 
  The view first retrieves CriterionMeasurement objects based on the criterion ID or 
  retrieves all objects with criterion names containing "Interval" if the criterion ID is not provided. 
  Then, it retrieves date ranges and employee, project, position, and criterion objects from the database. 
  Depending on the values of project_id and position_id, the view filters employees, 
  retrieves employee IDs from a project, or returns all employees. 
  The view then generates a dictionary containing the retrieved data and 
  uses the render_to_string function to render an HTML table with the data. 
  Finally, the view returns an HTTP response containing the JSON-encoded dictionary.

    """
    date_list = []
    if criterion_id != None and criterion_id != '' and criterion_id != 'none' and criterion_id !='0':
      criterion_m = CriterionMeasurement.objects.filter(tracker__pk = int(criterion_id))
    else:
      criterion_m = CriterionMeasurement.objects.filter(tracker__criterion_name__contains = 'Interval')
      
    date = DateRange.objects.all().first()
    date_list = date_range_append(date)
    
    
    criterion= Criterion.objects.all()
    position = Position.objects.all()
    project  = Project.objects.filter(status = True)
    
    if position_id ==0 and project_id==0:
      employee = Employee.objects.all().prefetch_related('auditee')
    elif project_id==0:
      employee = Employee.objects.filter(position__id =int(position_id)).prefetch_related('auditee')
    elif position_id == 0:
      employee_id_list = Project.objects.filter(id = project_id).values_list('members',flat=True)
      employee = Employee.objects.filter(pk__in =employee_id_list).prefetch_related('auditee')
    else:
      employee_id_list = Project.objects.filter(id = project_id).values_list('members',flat=True)
      employee = Employee.objects.filter(position__id =int(position_id), pk__in =employee_id_list).prefetch_related('auditee')
      
    data ={'project':project,'employee':employee,'criterion':criterion,'position':position,'date_list':date_list,'criterion_m':criterion_m}
    context = {}
    context['data'] = render_to_string("table.html",data)
    
    return HttpResponse(json.dumps(context), content_type="application/json")

      
  

def audit_view(request):
    date_list = []
    error_message_status = False
    date = DateRange.objects.all().first()
    criterion_m = CriterionMeasurement.objects.filter(tracker__criterion_name__contains = 'Interval')
    date = DateRange.objects.all().first()
    date_list = date_range_append(date)
    project  = Project.objects.filter(status = True)
    employee = Employee.objects.all().prefetch_related('auditee')
    criterion= Criterion.objects.all()
    position = Position.objects.all()
    project_id = position_id = criterion_id = 0
    employee_id_cache_key = 'employee_id_list'
    employee_id_list = cache.get(employee_id_cache_key)
    if employee_id_list is None:
        # If not cached, perform the query and cache the result
        employee_id_list = list(Employee.objects.all().values_list('id', flat=True))
        cache.set(employee_id_cache_key, employee_id_list)
    if request.method == 'POST':

        project_id = request.POST.get('single_project')
        position_id = request.POST.get('single_position')
        criterion_id = request.POST.get('single_criterion')
        
        for single_id in employee_id_list:
          for single_date in date_list:
            
            value_id = request.POST.get('tracker'+str(single_id)+str(single_date.strftime("%m-%d")))
            if value_id != None and value_id != '' and value_id != 'none' and value_id !='0':
              date = request.POST.get('date'+str(single_id)+str(single_date.strftime("%m-%d")))
              emp_id = request.POST.get('name'+str(single_id)+str(single_date.strftime("%m-%d")))
              
              employee_obj = get_object_or_404(Employee, id= emp_id)
              criterions = get_object_or_404(CriterionMeasurement, id= int(value_id))
              
              image  = request.FILES.get('img'+str(single_id)+str(single_date.strftime("%m-%d")))
              description =  request.POST.get('text'+str(single_id)+str(single_date.strftime("%m-%d")))

              if is_image(image):
                image = image
              else:
                image = None
              

              if criterions.tracker.project_required == False:
                bj, created = AccountManagerAudit.objects.update_or_create(
                  criterion__tracker = criterions.tracker,
                  auditives=employee_obj,
                  date=date,
                  defaults={'criterion':criterions,'auditor':request.user,'notice':criterions.notify,'text_description':description,'image_uploaded':image},)
              elif  criterions.tracker.project_required == True and (project_id != None and project_id != '' and project_id != 'none' and project_id !='0'):
                project_obj = get_object_or_404(Project, id= int(project_id))
                bj, created = AccountManagerAudit.objects.update_or_create(
                  criterion__tracker = criterions.tracker,
                  auditives=employee_obj,
                  date=date,
                  project=project_obj,
                  defaults={'criterion':criterions,'auditor':request.user,'notice':criterions.notify,'text_description':description,'image_uploaded':image},)
              else:
                error_message_status = True

        if error_message_status == True:
          messages.error(request, "Invalid Input or Please Select a Project for the criterion's ")
        else:
          messages.success(request, "You have Audited Successfully.")
        
        return redirect('audit_view_history_url',project_id,position_id,criterion_id)

            

    data ={'project':project,'employee':employee,'criterion':criterion,'position':position,'date_list':date_list,'criterion_m':criterion_m}
    return render(request,'audit_view.html',data)
  
  
def audit_view_history(request,project_id,position_id,criterion_id):
    date_list = []
    error_message_status = False
    date = DateRange.objects.all().first()
    if criterion_id != None and criterion_id != '' and criterion_id != 'none'  and criterion_id!=0:
      criterion_m = CriterionMeasurement.objects.filter(tracker__pk = int(criterion_id))
    else:
      criterion_m = CriterionMeasurement.objects.filter(tracker__criterion_name__contains = 'Interval')
      
    start_date = date.start_date if date else datetime.today()
    end_date = date.ending_date if date else datetime.today() + timedelta(days=3)
    date_list = [single_date for single_date in date_range(start_date, end_date)]
    # date range from the admin
    for single_date in date_range(start_date, end_date):
      date_list.append(single_date)
    

    project  = Project.objects.filter(status = True)
    
    if position_id ==0 and project_id==0:
      employee = Employee.objects.all().prefetch_related('auditee')
      print('works...........')
    elif project_id==0:
      employee = Employee.objects.filter(position__id =int(position_id)).prefetch_related('auditee')
    elif position_id == 0:
      employee_id_list = Project.objects.filter(id = project_id).values_list('members',flat=True)
      employee = Employee.objects.filter(pk__in =employee_id_list).prefetch_related('auditee')
    else:
      employee_id_list = Project.objects.filter(id = project_id).values_list('members',flat=True)
      employee = Employee.objects.filter(position__id =int(position_id), pk__in =employee_id_list).prefetch_related('auditee')
    

    criterion= Criterion.objects.all()
    position = Position.objects.all()

    data ={'project':project,'employee':employee,'criterion':criterion,'position':position,'date_list':date_list,'criterion_m':criterion_m}
    return render(request,'audit_view.html',data)    
  
  
  
  
def audit_history(request):
  audit_data  = AccountManagerAudit.objects.all()[0:200]
  criterion= Criterion.objects.all()
  position = Position.objects.all()
  project  = Project.objects.filter(status = True)
  data ={'project':project,'criterion':criterion,'position':position,'audit_data':audit_data}
  return render(request, 'audit_history.html', data)
  
  

@csrf_exempt
def get_account_manager_audits(request):
    if request.method == 'GET':
        audits = AccountManagerAudit.objects.all()[0:200]
        data = [{ 'auditives': str(audit.auditives),'criterion':  str(audit.criterion), 'project': str(audit.project), 'auditor': str(audit.auditor),  'date': audit.date.strftime('%Y-%m-%d')} for audit in audits]
        return JsonResponse({'data': data})
  


@csrf_exempt
def filter_account_manager_audits(request, criterion_id=0, project_id=0, position_id=0, start_date=None, end_date=None):
    
    if request.method == 'GET':
        
        filters = {}

        if position_id != 0:
            filters['auditives__position__id'] = int(position_id)
            print(position_id)
        if project_id != 0:
            filters['project__id'] = int(project_id)  
            print(project_id)
        if criterion_id != 0:
            filters['criterion__tracker__id'] = int(criterion_id)
            print(criterion_id)
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            print(start_date)
            print(end_date)
            filters['date__range'] = [start_date, end_date]

        audits = AccountManagerAudit.objects.filter(**filters)
      
        data = [{ 'auditives': str(audit.auditives),'criterion':  str(audit.criterion), 'project': str(audit.project), 'auditor': str(audit.auditor),  'date': audit.date.strftime('%Y-%m-%d')} for audit in audits]

        return JsonResponse({'data': data})
  
@csrf_exempt
def filter_account_manager_audits(request, criterion_id=0, project_id=0, position_id=0, start_date=None, end_date=None):
    
    if request.method == 'GET':
        
        filters = {}

        if position_id != 0:
            filters['auditives__position__id'] = int(position_id)
            print(position_id)
        if project_id != 0:
            filters['project__id'] = int(project_id)  
            print(project_id)
        if criterion_id != 0:
            filters['criterion__tracker__id'] = int(criterion_id)
            print(criterion_id)
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            print(start_date)
            print(end_date)
            filters['date__range'] = [start_date, end_date]

        audits = AccountManagerAudit.objects.filter(**filters)
      
        data = [{ 'auditives': str(audit.auditives),'criterion':  str(audit.criterion), 'project': str(audit.project), 'auditor': str(audit.auditor),  'date': audit.date.strftime('%Y-%m-%d')} for audit in audits]

        return JsonResponse({'data': data})
      
      
      
def single_employee(request,auditid):
  audit_counts = AccountManagerAudit.objects.values('added_at').annotate(count=Count('id'))
  name_list = auditid.split(" ")
  print(name_list)
  audit_data  = AccountManagerAudit.objects.filter(auditives__first_name = name_list[0],auditives__last_name = name_list[1] )[0:200]
  criterion1= Criterion.objects.all()
  project  = Project.objects.filter(status = True)

#  auditee_counts = AccountManagerAudit.objects.values('auditives__first_name', 'auditives__last_name').annotate(count=Count('id'))
  criteria = Criterion.objects.all()
  data = []
  for criterion in criteria:
        audits = AccountManagerAudit.objects.filter(criterion__tracker__criterion_name=criterion.criterion_name,auditives__first_name = name_list[0],auditives__last_name = name_list[1] ).count()
        data.append({
            'name': criterion.criterion_name,
            'y': audits
        })
  data ={'project':project,'criterion':criterion1,'audit_data':audit_data,  
        'data': data}
  return render(request, 'single_employee_analysis.html', data)
  
@csrf_exempt
def filter_single_employee_audits(request, criterion_id=0, project_id=0, start_date=None, end_date=None):
    
    if request.method == 'GET':
        
        filters = {}

        if project_id != 0:
            filters['project__id'] = int(project_id)  
            print(project_id)
        if criterion_id != 0:
            filters['criterion__tracker__id'] = int(criterion_id)
            print(criterion_id)
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            print(start_date)
            print(end_date)
            filters['date__range'] = [start_date, end_date]

        audits = AccountManagerAudit.objects.filter(**filters)
      
        data = [{ 'auditives': str(audit.auditives),'criterion':  str(audit.criterion), 'project': str(audit.project), 'auditor': str(audit.auditor),  'date': audit.date.strftime('%Y-%m-%d')} for audit in audits]

        return JsonResponse({'data': data})
      
      
def calender_view(request):
    criterion= Criterion.objects.all()
    position = Position.objects.all()
    project  = Project.objects.filter(status = True)
    data ={'project':project,'criterion':criterion,'position':position}
    return render(request,'calender_view.html',data)
            




        





def calender_json(request):

  # audit = AccountManagerAudit.objects.all()
        event_arr = []
        for single_audit in AccountManagerAudit.objects.filter(criterion__tracker__criterion_name__contains = 'Interval', notice= True):
          
            event_sub_arr = {}
            event_sub_arr["title"] =  single_audit.criterion.point.points+'->' +single_audit.auditives.first_name
            event_sub_arr["start"] = single_audit.date
            event_sub_arr["backgroundColor"]='#DB7093'
            event_sub_arr["description"] = 'long description'
            event_arr.append(event_sub_arr)
        return JsonResponse(event_arr, safe=False)






def calender_update_json(request,criterion_id=0,project_id=0,position_id=0):
    # if position_id ==0 and project_id==0 :
    #   audit = AccountManagerAudit.objects.filter(criterion__tracker__criterion_name__contains = 'Interval', notice= True)
    # elif position_id == 0:
    #     audit = AccountManagerAudit.objects.filter(project__id = int(project_id), criterion__tracker__id = int(criterion_id) , notice= True)
    # elif project_id ==0:
    #   audit = AccountManagerAudit.objects.filter(auditives__position__id = int(position_id), notice= True,criterion__tracker__id = int(criterion_id)) 
    # elif position_id and project_id:
    #   audit = AccountManagerAudit.objects.filter(project__id = int(project_id),auditives__position__id = int(position_id), notice= True,criterion__tracker__id = int(criterion_id))
    # else:
    #   audit = AccountManagerAudit.objects.filter(criterion__tracker__criterion_name__contains = 'Interval', notice= True)
    filters = {
        (0, 0): {'criterion__tracker__criterion_name__contains': 'Interval', 'notice': True},
        (0, project_id): {'project__id': project_id, 'criterion__tracker__id': criterion_id, 'notice': True},
        (position_id, 0): {'auditives__position__id': position_id, 'criterion__tracker__id': criterion_id, 'notice': True},
        (position_id, project_id): {'project__id': project_id, 'auditives__position__id': position_id, 'criterion__tracker__id': criterion_id, 'notice': True},
    }
    audit = AccountManagerAudit.objects.filter(**filters.get((position_id, project_id), filters[(0, 0)]))
          
  
    event_arr = []
    for single_audit in audit:
          event_sub_arr = {}
          event_sub_arr["title"] =  single_audit.criterion.point.points+'->' +single_audit.auditives.first_name
          event_sub_arr["start"] = single_audit.date
          event_sub_arr["backgroundColor"]='#DB7093'
          event_sub_arr["description"]='long description'
          event_arr.append(event_sub_arr)
    return JsonResponse(event_arr, safe=False)
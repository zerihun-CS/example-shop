from django.urls import path
from .views import *
    
urlpatterns = [
      
      path('',audit_view,name="audit_view_url"),
      path('history/<int:project_id>/<int:position_id>/<int:criterion_id>/',audit_view_history, name="audit_view_history_url"),
      path('audit_history/',audit_history, name="audit_history_url"),
      path('get_account_manager_audits/',get_account_manager_audits,name="get_account_manager_audits_url"),
      
      path('audit_history/get_employee_audits/<str:auditid>/',single_employee,name="get_single_employee_audits_url"),
      path('json_filter/<int:criterion_id>/<int:project_id>/<int:position_id>/<str:start_date>/<str:end_date>/',filter_account_manager_audits, name="filter_response"),
      
            
      path('json/<int:criterion_id>/<int:project_id>/<int:position_id>/',json_view, name="data_response"),
      
      path('calender_view/', calender_view, name="calender_view_url"),
      path('calender_json/', calender_json, name="calender_json_url"),
      path('calender_json/<int:criterion_id>/<int:project_id>/<int:position_id>/', calender_update_json, name="calender_update_json_url"),
      
            
]
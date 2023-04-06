from django.urls import path
from .views import *
    
urlpatterns = [
      path('',index,name="home_url"),
      
      
      path('client-list/', ClientListView.as_view(), name='client_list_url'),
      path('client-create/', ClientCreateView.as_view(), name='client_create_url'),
      path('client-detail/<int:pk>', ClientDetailView.as_view(),name='client_detail_url'),
      path('client-update/<int:pk>', ClientUpdateView.as_view(),name='client_update_url'),
      path('client-delete/<int:pk>', ClientDeleteView.as_view(),name='client_delete_url'),
      
      
      path('project-list/', ProjectListView.as_view(), name='project_list_url'),
      path('project-create/', ProjectCreateView.as_view(), name='project_create_url'),
      path('project-update/<int:pk>', ProjectUpdateView.as_view(),name='project_update_url'),
      path('project-delete/<int:pk>', ProjectDeleteView.as_view(),name='project_delete_url'),
      path('project-detail/<int:pk>', ProjectDetailView.as_view(),name='project_detail_url'),
]          
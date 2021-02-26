from django.urls import path

from . import views

app_name = "processconfig"
urlpatterns = [
    path('', views.FileConfigurationView.as_view(), name='index'),
    path('<int:pk>/', views.FileConfigurationForProjectView.as_view(), name='project'),
    path('<int:pk>/update/', views.FileConfigurationUpdateView.as_view(), name='update_flow'),
    path('<int:pk>/create/', views.CreateFlowView.as_view(), name='create_flow'),
    path('sas_program/delete/<int:pk>/', views.FileDeleteView.as_view(), name='sas_program_delete'),
    path('sas_program/change_order/', views.ChangeSASProgramOrderView.as_view(), name="change_order"),
    path('generate/<int:pk>/', views.GenerateFile.as_view(), name="generate_file"),
]

from django.urls import path

from . import views

app_name = "processconfig"
urlpatterns = [
    path('', views.FileConfigurationView.as_view(), name='index'),
    path('<int:pk>/', views.FileConfigurationForProjectView.as_view(), name='project'),
    path('<int:pk>/update/', views.FileConfigurationUpdateView.as_view(), name='update_flow'),
    path('<int:pk>/create/', views.CreateFlowView.as_view(), name='create_flow'),
]

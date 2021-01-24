from django.urls import path

from . import views

app_name = "processconfig"
urlpatterns = [
    path('', views.FileConfigurationView.as_view(), name='index'),
]

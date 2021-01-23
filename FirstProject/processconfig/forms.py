from django.forms import ModelForm
from . import models


class FileUploadForm(ModelForm):
    class Meta:
        model = models.ProcessFlows
        fields = [
            "project_name",
            "sas_program"
        ]
from django import forms
from . import models


class FileUploadForm(forms.Form):
    flow_name = forms.CharField(max_length=250)
    sas_program = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class FileUploadWithProjectNameForm(FileUploadForm):
    project_name = forms.CharField(max_length=250)
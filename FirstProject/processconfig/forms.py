from django import forms
from . import models


class FileUploadForm(forms.Form):
    sas_program = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class FileUploadWithProjectNameForm(FileUploadForm):
    project_name = forms.CharField(max_length=100)
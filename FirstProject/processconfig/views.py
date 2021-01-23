from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.template import loader
from . import forms
from . import models

class FileConfigurationView(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template("main.html")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        form = forms.FileUploadWithProjectNameForm(request.POST, request.FILES)
        if form.is_valid():
            project_name = models.ProcessFlows.objects.create(
                project_name=request.POST["project_name"]
            )
            for i, file in enumerate(request.FILES.getlist("sas_program")):
                new_file = models.SASPrograms.objects.create(
                    sas_program=file,
                    order_number=i,
                    sas_program_name=file
                )
                project_name.sas_program.add(new_file)
        return render(request, "main.html", context={})

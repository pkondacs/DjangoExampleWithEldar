from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.template import loader
from . import forms
from . import models

class FileConfigurationView(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template("sas_config.html")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        form = forms.FileUploadWithProjectNameForm(request.POST, request.FILES)
        table = None
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
            table = project_name.sas_program.all()
        return render(request, "sas_config.html", context={"table": table})

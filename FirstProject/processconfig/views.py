from django.http import HttpResponse, FileResponse, JsonResponse
from django.views import View, generic
from django.shortcuts import render, redirect, reverse
from django.template import loader
from django.db.models import Max
from . import forms
from . import models
import json
from .utils import get_table


class FileConfigurationView(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template("sas_config_main.html")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        form = forms.FileUploadWithProjectNameForm(request.POST, request.FILES)
        if form.is_valid():
            project_name = models.ProcessFlows.objects.create(
                project_name=request.POST["project_name"]
            )
            flow = models.ProgramFlows.objects.create(
                flow_name=request.POST["flow_name"]
            )
            project_name.flows.add(flow)
            for i, file in enumerate(request.FILES.getlist("sas_program")):
                new_file = models.SASPrograms.objects.create(
                    sas_program=file,
                    order_number=i,
                    sas_program_name=file
                )
                flow.sas_programs.add(new_file)
            return redirect(reverse('processconfig:project', kwargs={"pk":project_name.id}))
        return redirect(reverse('processconfig:index'))


class FileConfigurationForProjectView(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template("sas_config_project.html")
        project = models.ProcessFlows.objects.get(id=kwargs.get("pk"))
        flows = project.flows.all()
        context = {
            "flows": flows,
            "project": project,
            "pk": kwargs.get("pk"),
        }
        return HttpResponse(template.render(context, request))


class FileConfigurationUpdateView(View):
    def post(self, request, *args, **kwargs):
        flow = models.ProgramFlows.objects.get(pk=kwargs.get("pk"))
        form = forms.FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            flow.flow_name = request.POST.get("flow_name")
            flow.save()
            start = flow.sas_programs.all().aggregate(max_flow=Max('order_number'))["max_flow"] + 1
            for i, file in enumerate(request.FILES.getlist("sas_program"), start=start):
                new_file = models.SASPrograms.objects.create(
                    sas_program=file,
                    order_number=i,
                    sas_program_name=file
                )
                flow.sas_programs.add(new_file)
        return redirect(reverse('processconfig:project', kwargs={"pk": flow.processflows_set.all().first().id}))


class CreateFlowView(View):
    def post(self, request, *args, **kwargs):
        project = models.ProcessFlows.objects.get(id=kwargs.get("pk"))
        form = forms.FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            flow = models.ProgramFlows.objects.create(flow_name=request.POST.get("flow_name"))
            project.flows.add(flow)
            for i, file in enumerate(request.FILES.getlist("sas_program")):
                new_file = models.SASPrograms.objects.create(
                    sas_program=file,
                    order_number=i,
                    sas_program_name=file
                )
                flow.sas_programs.add(new_file)
        return redirect(reverse('processconfig:project', kwargs={"pk": kwargs.get("pk")}))


class FileDeleteView(generic.DeleteView):
    model = models.SASPrograms
    queryset = model.objects.all()

    def delete(self, request, *args, **kwargs):
        file = self.get_object()
        program_flow = models.ProgramFlows.objects.get(sas_programs=file)
        file.delete()
        if program_flow.sas_programs.all().count() == 0:
            project = models.ProcessFlows.objects.get(flows=program_flow)
            program_flow.delete()
            return JsonResponse({"response": "refresh"})
        return JsonResponse({"response": "deleted"})


class ChangeSASProgramOrderView(View):

    def post(self, request, *args, **kwargs):
        for element in json.load(request):
            sas_program = models.SASPrograms.objects.get(id=element.get("id"))
            sas_program.order_number = element.get("order_number")
            sas_program.save()
        return HttpResponse("changed")


class GenerateFile(View):
    def get(self, request, *args, **kwargs):
        file = get_table(kwargs.get("pk"))
        return FileResponse(file, as_attachment=True)
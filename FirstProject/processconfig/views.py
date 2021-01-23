from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect, reverse
from django.template import loader
from . import forms


class FileConfigurationView(View):
    def get(self, request, *args, **kwargs):
        template = loader.get_template("main.html")
        context = {}
        return HttpResponse(template.render(context, request))

    def post(self, request, *args, **kwargs):
        files = request.FILES
        form = forms.FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
        return render(request, "main.html", context={})

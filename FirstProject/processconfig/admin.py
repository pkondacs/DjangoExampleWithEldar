from django.contrib import admin
from . import models
# If you want your models to appear on admin, then you can register them here.

admin.site.register(models.SASPrograms)
admin.site.register(models.ProcessFlows)
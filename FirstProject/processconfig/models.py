from django.db import models


class SASPrograms(models.Model):
    sas_program = models.FileField(upload_to="files")
    order_number = models.IntegerField(default=0)
    sas_program_name = models.CharField(max_length=100, default="")

# Create your models here.

class ProcessFlows(models.Model):
    project_name = models.CharField(max_length=100, default="")
    process_flow_int = models.IntegerField(default=0)
    sas_program = models.ManyToManyField(SASPrograms, blank=True)

    @classmethod
    def create(cls, project_name):
        item = cls(project_name=project_name)
        return item

    class Meta:
        verbose_name = "Process Flow"
        verbose_name_plural = "Process Flows"

    def __str__(self):
        return f"Process Flow {self.process_flow_int} for the project {self.project_name}"


item = ProcessFlows.create("Test Entry")
print(item)

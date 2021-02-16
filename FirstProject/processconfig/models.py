from django.db import models


class SASPrograms(models.Model):
    sas_program = models.FileField(upload_to="files")
    order_number = models.IntegerField(default=0)
    sas_program_name = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name = "SASProgram"
        verbose_name_plural = "SASPrograms"

    def __str__(self):
        return f"{self.sas_program_name}"


class ProgramFlows(models.Model):
    flow_order_number = models.IntegerField(default=0)
    flow_name = models.IntegerField(default="")
    sas_programs = models.ManyToManyField(SASPrograms, blank=True)

    class Meta:
        verbose_name = "Flow number"
        verbose_name_plural = "Flows number"

    def __str__(self):
        return f"{self.flow_order_number} with {self.sas_programs.all().count()}"


class ProcessFlows(models.Model):
    project_name = models.CharField(max_length=100, default="")
    flows = models.ManyToManyField(ProgramFlows, blank=True)

    class Meta:
        verbose_name = "Process Flow"
        verbose_name_plural = "Process Flows"

    def __str__(self):
        return f"{self.project_name}"



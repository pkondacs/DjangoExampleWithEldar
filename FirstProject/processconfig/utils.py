from .models import ProcessFlows
from .egp_package_web import *
import pandas as pd
from django.conf.global_settings import *
import os


def get_table(project_id):
    data = [["ProcessFlow", "ProgramName", "Subfolder"]]
    project = ProcessFlows.objects.get(id=project_id)
    flows = project.flows.all()
    for flow in flows:
        data.extend(
            [[flow.flow_name, file.sas_program_name, os.path.join(MEDIA_ROOT, 'files')]
             for file in flow.sas_programs.all()]
        )
    df = pd.DataFrame(data=data[1:], columns=data[0])
    os.mkdir(MEDIA_ROOT + f"\{project.project_name}")
    os.mkdir(MEDIA_ROOT + f"\{project.project_name}\\00_EGP_Packager")
    basePath = os.path.join(MEDIA_ROOT, project.project_name)
    path = os.path.join(basePath, "00_EGP_Packager", project.project_name + ".csv")
    df.to_csv(path, index=False)
    files = selectModules(basePath)
    createEGP(files[0], basePath)
    file = open(path, "rb")
    return file

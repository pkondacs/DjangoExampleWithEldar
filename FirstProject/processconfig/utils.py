from .models import ProcessFlows
from .egp_package_web import *
import pandas as pd
from django.conf import settings
import os


def get_table(project_id):
    data = [["ProcessFlow", "ProgramName", "Subfolder"]]
    project = ProcessFlows.objects.get(id=project_id)
    flows = project.flows.all()
    for flow in flows:
        data.extend(
            [[
                flow.flow_name, file.sas_program.name.split("/")[1],
                os.path.join(settings.MEDIA_ROOT, 'files')
            ] for file in flow.sas_programs.all().order_by('order_number')]
        )
    df = pd.DataFrame(data=data[1:], columns=data[0])
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, project.project_name)):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, project.project_name))
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, '00_EGP_Packager')):
        os.mkdir(os.path.join(settings.MEDIA_ROOT, '00_EGP_Packager'))
        os.mkdir(os.path.join(settings.MEDIA_ROOT, '00_EGP_Packager', 'IRBMA_Template_Project'))
    path = os.path.join(settings.MEDIA_ROOT, "00_EGP_Packager", project.project_name + ".csv")
    df.to_csv(path, index=False)
    createEGP(project.project_name, settings.MEDIA_ROOT)
    file = open(os.path.join(settings.MEDIA_ROOT, project.project_name + '.egp'), "rb")
    return file

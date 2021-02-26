import os
import shutil
from xml.etree.ElementTree import parse
import copy
import math
import pandas as pd


def printLine():
    print('\n######################################\n')


def selectModules(basePath):
    """Select modules that have changed from last time (files in src or datalines are newer than EGP)"""
    allModulesList = [f.replace('.csv', '') for f in os.listdir(os.path.join(basePath, '00_EGP_Packager')) if
                      f.endswith('.csv')]
    selectedModulesList = []
    # Check if creating new EGP is necessary (EGP is older than csv, src and datalines)
    for module in allModulesList:
        egpPath = os.path.join(basePath, module, module + '.egp')
        if not os.path.exists(egpPath):
            selectedModulesList.append(module)
        else:
            T_egp = os.path.getmtime(egpPath)
            csvPath = os.path.join(basePath, '00_EGP_Packager', module + '.csv')
            progTable = pd.read_csv(csvPath)
            # Create list of scripts to check modification date
            scriptPaths = [csvPath]
            for index, row in progTable.iterrows():
                script = row['ProgramName']
                scriptPath = row['Subfolder']
                # Adjust path
                if scriptPath.startswith('src'):
                    scriptPaths.append(os.path.join(basePath, module, scriptPath, script+'.sas'))
                else:
                    scriptPaths.append(os.path.join(basePath, scriptPath, script+'.sas'))
            T = max([os.path.getmtime(f) for f in scriptPaths])

            # Because of git synchronisation order,
            # we will check if egp was created earlier than other files with a 2 sec lag
            T_egp = math.floor(T_egp) + 2
            T = math.floor(T)

            if T_egp < T:
                selectedModulesList.append(module)

    return selectedModulesList


def creteEGPStructure(module, modulePath, scriptListPath, templatePath):
    """Create project folder structure and copy scripts
        based on scriptListPath csv with scripts order
        and templatePath template project in given module"""
    progTable = pd.read_csv(scriptListPath)

    targetLevel1 = os.path.join(modulePath, module)
    # Create main folder - clear if exists
    if os.path.exists(targetLevel1):
        shutil.rmtree(targetLevel1)
    os.mkdir(targetLevel1)

    # Create folder for each script
    for index, row in progTable.iterrows():
        process = row['ProcessFlow']
        script = row['ProgramName']
        scriptPath = row['Subfolder']
        # Adjust path
        # if scriptPath.startswith('src'):
        #     scriptPath = os.path.join(modulePath, scriptPath)
        # else:
        #     scriptPath = os.path.join(basePath, scriptPath)
        # Create folder for script
        targetLevel2 = os.path.join(targetLevel1, str('Codetask-' + script))
        if os.path.exists(targetLevel2):
            shutil.rmtree(targetLevel2)
        os.mkdir(targetLevel2)

        # Copy script
        # sourceFileName = os.path.join(scriptPath, script + '.sas')
        sourceFileName = os.path.join(scriptPath, script)
        targetFileName = os.path.join(targetLevel2, 'code.sas')
        shutil.copyfile(sourceFileName, targetFileName)

        print(process, script)

    # Copy log folder
    projectLog = [f for f in os.listdir(templatePath) if f.startswith("ProjectLog")][0]
    projectLogSrc = os.path.join(templatePath, projectLog)
    projectLogDst = os.path.join(targetLevel1, projectLog)
    if os.path.exists(projectLogDst):
        shutil.rmtree(projectLogDst)
    shutil.copytree(src=projectLogSrc, dst=projectLogDst)


def xmlParsing(module, modulePath, templatePath, xmlFileName, scriptListPath):
    """Create xml file for process flow structure in EGP"""

    progTable = pd.read_csv(scriptListPath)
    processFlows = progTable['ProcessFlow'].unique()

    doc = parse(os.path.join(templatePath, xmlFileName))

    # Change project label
    doc.getroot().find('Element/Label').text = module

    ### Update External objects node
    # External objects - children: ProjectTreeView (with EGTreeNodes), ProcessFlowView (with Containers), MainForm (empty)
    root_ext_objects = doc.find(".//External_Objects")
    # Process flow - children: NodeType (NODETYPE_ELEMENT), ElementID, Expanded, label, EGTreeNode (program folder)
    elem_pfd = root_ext_objects.find(".//EGTreeNode")
    # Program folder - children: NodeType (NODETYPE_PROGRAMFOLDER), Expanded, Label, EgTreeNodes (with CodeTasks)
    elem_programfolder = elem_pfd.find(".//EGTreeNode")
    # Code Task - children: NodeType (NODETYPE_ELEMENT), ElementID, Expanded, Label
    elem_codetask = elem_programfolder.find(".//EGTreeNode")
    # Containers
    elem_containers = root_ext_objects.find(".//Containers")
    # Properties
    elem_properties = elem_containers.find(".//Properties")

    # Clear elements
    for elem in root_ext_objects.find('ProjectTreeView').findall('EGTreeNode'):
        root_ext_objects.find('ProjectTreeView').remove(elem)

    for elem in elem_containers.findall('Properties'):
        elem_containers.remove(elem)

    for elem in elem_pfd.findall('EGTreeNode'):
        elem_pfd.remove(elem)

    for elem in elem_programfolder.findall('EGTreeNode'):
        elem_programfolder.remove(elem)

    # For each process flow create node and append it to root_ext_objects
    for pf in processFlows:
        new_elem_pfd = copy.deepcopy(elem_pfd)
        new_elem_pfd.find('ElementID').text = 'PFD-' + pf
        new_elem_pfd.find('Label').text = pf
        new_elem_programfolder = copy.deepcopy(elem_programfolder)


        # For each program create node
        pfCodes = list(progTable['ProgramName'][progTable['ProcessFlow'] == pf])
        for p in pfCodes:
            new_elem_codetask = copy.deepcopy(elem_codetask)
            new_elem_codetask.find('ElementID').text = 'CodeTask-' + p
            new_elem_codetask.find('Label').text = p
            # Add to ProgramFolder
            new_elem_programfolder.append(new_elem_codetask)

        new_elem_pfd.append(new_elem_programfolder)
        root_ext_objects.find('ProjectTreeView').append(new_elem_pfd)

        # Add new node to Containers
        new_elem_properties = copy.deepcopy(elem_properties)
        new_elem_properties.find('ID').text = 'PFD-' + pf
        elem_containers.append(new_elem_properties)

    ### Update Elements node
    # Elements - children: Element of different types (PFD / CodeTask / Link)
    root_node = doc.find(".//Elements")

    # Element type PFD - children: Element ContainerElement PFD
    elem_pfd = root_node.find(".//Element/[@Type='SAS.EG.ProjectElements.PFD']")
    # PFD - children: Process with children Element and Dependecies (from 2nd child)
    elem_pfd_process1 = elem_pfd.findall('.//Process')[0]
    elem_pfd_process2 = elem_pfd.findall('.//Process')[1]
    # Element type CodeTask - children: Label Type Container ID and technical ones
    elem_codetask = root_node.find(".//Element/[@Type='SAS.EG.ProjectElements.CodeTask']")
    # Element type Link - children: Element Log
    elem_link = root_node.find(".//Element/[@Type='SAS.EG.ProjectElements.Link']")

    # Clear templates
    for elem in root_node.findall('Element'):
        root_node.remove(elem)

    for elem in elem_pfd.find('PFD').findall('Process'):
        elem_pfd.find('PFD').remove(elem)

    # Add Process Flow elements
    for pf in processFlows:
        new_elem_pfd = copy.deepcopy(elem_pfd)
        new_elem_pfd.find('Element').find('Label').text = pf
        new_elem_pfd.find('Element').find('ID').text = 'PFD-' + pf

        # Add first program to PFD
        pfCodes = list(progTable['ProgramName'][progTable['ProcessFlow'] == pf])
        new_elem_process = copy.deepcopy(elem_pfd_process1)
        new_elem_process.find('.//ID').text = 'CodeTask-' + pfCodes[0]
        new_elem_pfd.find('PFD').append(new_elem_process)

        # Add other programs to PFD
        for i in range(1, len(pfCodes)):
            new_elem_process = copy.deepcopy(elem_pfd_process2)
            new_elem_process.find('.//ID').text = 'CodeTask-' + pfCodes[i]
            new_elem_process.find('.//DepID').text = 'CodeTask-' + pfCodes[i - 1]
            new_elem_pfd.find('PFD').append(new_elem_process)

        root_node.append(new_elem_pfd)

    # Add Code Task elements
    for index, row in progTable.iterrows():
        new_elem_codetask = copy.deepcopy(elem_codetask)
        new_elem_codetask.find('Element').find('Label').text = row['ProgramName']
        new_elem_codetask.find('Element').find('Container').text = 'PFD-' + row['ProcessFlow']
        new_elem_codetask.find('Element').find('ID').text = 'CodeTask-' + row['ProgramName']

        root_node.append(new_elem_codetask)

    # Add Link elements
    for i in range(1, len(progTable)):
        pf = progTable['ProcessFlow'][i]
        pf_prev = progTable['ProcessFlow'][i - 1]
        # If code tasks are in the same process flow, connect them
        if pf == pf_prev:
            ct = progTable['ProgramName'][i]
            ct_prev = progTable['ProgramName'][i - 1]
            new_elem_link = copy.deepcopy(elem_link)
            # Update Element child
            new_elem_link.find('Element').find('Label').text = 'Link to ' + ct
            new_elem_link.find('Element').find('Container').text = 'PFD-' + pf
            new_elem_link.find('Element').find('ID').text = 'Link-' + ct
            new_elem_link.find('Element').find('InputIDs').text = 'CodeTask-' + ct_prev
            # Update Log child
            new_elem_link.find('Log').find('Parent').text = 'CodeTask-' + ct_prev
            new_elem_link.find('Log').find('LinkFrom').text = 'CodeTask-' + ct_prev
            new_elem_link.find('Log').find('LinkTo').text = 'CodeTask-' + ct

            root_node.append(new_elem_link)

    ### Update Containers node
    # Containers - children: IDs
    elem_containers = doc.find(".//Containers")
    # ID
    elem_ID = elem_containers[0]

    elem_containers.clear()
    for pf in processFlows:
        new_elem_ID = copy.deepcopy(elem_ID)
        new_elem_ID.text = 'PFD-' + pf
        elem_containers.append(new_elem_ID)

    ### Clear Graphics element
    doc.find('.//Graphics').clear()

    ### Writing complete xml file
    doc.write(os.path.join(modulePath, module, xmlFileName))


def zipModExt(path):
    """Zip, change extension to .egp and delete source folder"""
    shutil.make_archive(path, 'zip', path)
    if os.path.exists(path + ".egp"):
        os.remove(path + ".egp")
    os.rename(path + ".zip", path + ".egp")
    shutil.rmtree(path)


def createEGP(module, basePath):
    """Create EGP - zip structure folder and change extension"""

    # Read EGP structure
    basePath = basePath
    xmlFileName = 'project.xml'
    modulePath = os.path.join(basePath, module)
    scriptListPath = os.path.join(basePath, '00_EGP_Packager', module + '.csv')
    templatePath = os.path.join(basePath, '00_EGP_Packager', 'IRBMA_Template_Project')

    # Create EGP structure in folder
    print('Creating structure...')
    creteEGPStructure(
        module=module,
        modulePath=basePath,
        scriptListPath=scriptListPath,
        templatePath=templatePath)

    # Add xml file
    print('Writing xml...')
    xmlParsing(
        module=module,
        modulePath=basePath,
        templatePath=templatePath,
        xmlFileName=xmlFileName,
        scriptListPath=scriptListPath
    )

    # Make EGP file
    print('Encapsulating in egp...')
    zipModExt(
        path=os.path.join(basePath, module)
    )


if __name__ == "__main__":
    xmlFileName = 'project.xml'

    # For manual execution
    # basePath = r'H:\Documents\irb-ma-sas'  # for manual execution
    # module = 'Dragging_estimation'
    # createEGP(
    #     module=module,
    #     basePath=basePath
    # )

    # For cmd execution
    basePath = ''
    # Read module list
    fileList = selectModules(basePath)

    if len(fileList) == 0:
        printLine()
        print('All EGPs are up-to-date')
    else:
        printLine()
        print('Modules selected for update:')
        for f in fileList:
            print(' - ' + f)

    # Create EGP for each module
    for module in fileList:
        printLine()
        print(module)
        createEGP(
            module=module,
            basePath=basePath
        )

    printLine()

import pymel.core as pm
import maya.mel as mel
import os,json


data = {}
with open("config.json","r") as f:
    data = json.load(f)
pathFile = data["PathFile"]

def main():
    global data
    global pathFile

    scenePath =  pm.sceneName()
    mayaName = os.path.basename(scenePath)
    selectionList = pm.ls(sl=True)
    printList=''

    if selectionList: # Check selection


        tempPath = searchPath(mayaName,pathFile)

        exportPath = pm.fileDialog2(ff="*.folder",dir=tempPath, fm=2)
        if exportPath:
            mel.eval('shelfButton  -e -enable true shelfButton3')
            data[mayaName] = exportPath[0]
            with open(pathFile,"w") as f:
                json.dump(data, f,indent=4, sort_keys=True)
            
            for s in selectionList:
                
                pm.select(s)
                if "|" in s:
                    s = s.split("|")[-1]
                transFrom = s.getTransformation()
                s.resetFromRestPosition()
                pm.exportSelected(exportPath[0]+'\\'+str(s)+".fbx",f=True) #Export FBXs
                printList += str(s) + '\n'
                s.setTransformation(transFrom)

            confirm = pm.confirmDialog(title="Success",b=["Done","Open Folder"], message="Exported:\t\t\n\n" + printList,messageAlign ="left")
            if confirm == "Open Folder":
                os.startfile(exportPath[0])
        else:
            print("user cancelled")
    else:
        pm.confirmDialog(title="error",message="No objects be selected")



def searchPath(maya_name,path_file):
    global data
    with open(path_file,"r") as f:
        data = json.loads(f.read())

    if maya_name in data:
        exportPath = data[maya_name]
    else:
        exportPath = data["tempPath"]

    return exportPath
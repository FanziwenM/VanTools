#Author: Fanziwen (120416678@qq.com)
#Created: 08/21/2019
#Updated: 09/20/2019 
#Last Change: Add JSON file to save Export path

import pymel.core as pm
import maya.mel as mel
import os,json
from VanTools.general.exportFBX import searchPath, pathFile,prefFile

data = {}

def main():
    global data
    scenePath =  pm.sceneName()
    mayaName = os.path.basename(scenePath)
    selectionList = pm.ls(sl=True)
    printList=''

    if selectionList:


        exportPath = searchPath(mayaName,pathFile)
        with open(prefFile, "r") as f:
            prefData = json.load(f)

        ifExportInCenter = prefData["centerExport"]

        if exportPath != "D:/":
            if ifExportInCenter:
                # Export files in center
                for s in selectionList:
                    pm.select(s)

                    mel.eval('BakeCustomPivot')
                    oTrans = s.getTransformation()
                    s.resetFromRestPosition()
                    if "|" in s:
                        s2 = s.split("|")[-1]
                        try:
                            pm.exportSelected(exportPath+'\\'+str(s2)+".fbx",f=True)
                        except Exception as e:
                            print(e)
                        s.setTransformation(oTrans)
                        printList += str(s2) + '\n'
                    else:
                        try:
                            pm.exportSelected(exportPath+'\\'+str(s)+".fbx",f=True)
                        except Exception as e:
                            print(e)
                        s.setTransformation(oTrans)
                        printList += str(s) + '\n'
                

                pm.inViewMessage( 
                    amg= '{}:\n<font color="#48AAB5">{}</font>\n'.format(exportPath,printList) 
                    + "<font color='yellow'>Exprot IN Center</font>".center(int(len(exportPath)*2),"-"),
                     pos='topCenter', fade=True )
            else:
                # normal Export files
                for s in selectionList:
                    pm.select(s)
                    # Check the file whether has the same name in the scene
                    if "|" in s:
                        s = s.split("|")[-1]

                    pm.exportSelected(exportPath+'\\'+str(s)+".fbx",f=True)
                    # update export info
                    printList += "\n{}".format(str(s))

                pm.inViewMessage( amg='{}:<font color="#48AAB5">{}</font>'.format(exportPath,printList), 
                pos='topCenter', fade=True )

        else:
            pm.confirmDialog(title="error",message="The path is unspecified ")
    else:
        pm.confirmDialog(title="error",message="No objects be selected")


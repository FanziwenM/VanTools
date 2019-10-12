#Author: Fanziwen (120416678@qq.com)
#Created: 08/21/2019
#Updated: 09/20/2019 
#Last Change: Change the code to Class type

import pymel.core as pm 
import maya.mel as mel
import json,os

# load config.json to get path file
with open("config.json","r") as f:
    data = json.load(f)
pathFile = data["PathFile"]

with open("config.json","r") as f:
    data = json.load(f)
prefFile = data["MayaPref"]

def main():
    global pathFile, prefFile
    # search whether the export path has been saved in file.
    scenePath =  pm.sceneName()
    mayaName = os.path.basename(scenePath)
    tempPath = searchPath(mayaName,pathFile)

    # beginning export,when something is selected
    selectionList = pm.ls(sl=True)
    if selectionList:
        myWindow = ExportWindow(selectionList,mayaName,pathFile,prefFile) # createUI
        myWindow.path = tempPath
        myWindow.updateText()

    else:
        pm.confirmDialog(title="error",message="No objects be selected")

class ExportWindow():
    global data
    '''
    Create Export window
    '''
    def __init__(self,selectionList,mayaName,pathFile,prefFile):
        '''
        Init Export window
        '''
        self.path = "D:\\"
        self.scrollHeight = min(len(selectionList)*15, 100)
        self.printList = ""
        self.selectionList = selectionList
        self.mayaName = mayaName
        self.pathFile = pathFile
        self.prefFile = prefFile
        self.prefData = {}

        with pm.window(title = "Export FBX", toolbox=True, sizeable=False ,topLeftCorner =(200,320),w=490, h = self.scrollHeight) as self.window:
            with pm.formLayout() as self.form:
                with pm.scrollLayout(h = self.scrollHeight) as self.scroll:
                    for s in selectionList:
                        pm.nameField(object = s, w=350)

                with pm.rowLayout(numberOfColumns=3, adjustableColumn=2, ) as self.row:
                    pm.text(label = "Path:")
                    self.pathField = pm.textField(searchField=True,text = self.path)
                    pm.button("...", c=self.changePath, w=50)

                self.exportBut = pm.button("Export",c=self.export,w=50, bgc=(0.28, 0.66, 0.71))
                self.expCheck = pm.checkBox(label='Export in Center')
                self.updateCheckBox()

                pm.formLayout(
                    self.form,edit=True,
                    attachForm=[
                        (self.scroll,"left", 5),
                        (self.scroll,"top", 5),
                        (self.exportBut, "right", 5),
                        (self.exportBut, "top", 5),
                        (self.expCheck, "right", 5),
                        (self.row,"bottom", 5),
                        (self.row,"left", 5),
                        (self.row,"right", 5)
                    ],
                    attachControl=[
                        (self.scroll,"right", 5, self.exportBut),
                        (self.scroll,"right", 5, self.expCheck),
                        (self.scroll,"bottom", 5, self.row),
                        (self.exportBut,"bottom", 5, self.expCheck),
                        (self.exportBut,"left", 5, self.scroll),
                        (self.expCheck, "bottom", 5, self.row ),
                    ]
                    )
            pm.showWindow()
    
    def updateText(self):
        self.pathField.setText(self.path)

    def updateCheckBox(self):
        with open(self.prefFile, "r") as f:
            self.prefData = json.loads(f.read())
        pm.checkBox(self.expCheck, e = True, value = self.prefData["centerExport"])
        return self.prefData["centerExport"]

    def changePath(self,*args):
        newPath = pm.fileDialog2(ff="*.folder",dir=self.path, fm=2)
        if newPath:
            self.path = newPath[0]
            self.updateText()
        else:
            pass
        
    
    def export(self,*args):
        self.path = pm.textField(self.pathField,q = True, text = True)
        if self.path:
            shelfVan = pm.shelfLayout("Van",q=True,ca=True)
            mel.eval('shelfButton -e -enable true {}'.format(shelfVan[2]))

            centerExport = pm.checkBox(self.expCheck, q=True, value=True)
            self.prefData["centerExport"] = centerExport
            if centerExport:
                for s in self.selectionList:
                    pm.select(s)

                    mel.eval('BakeCustomPivot')
                    oTrans = s.getTransformation()
                    s.resetFromRestPosition()
                    if "|" in s:
                        s2 = s.split("|")[-1]
                        try:
                            pm.exportSelected(self.path+'\\'+str(s2)+".fbx",f=True)
                        except Exception as e:
                            print(e)
                        s.setTransformation(oTrans)
                        self.printList += str(s2) + '\n'
                    else:
                        try:
                            pm.exportSelected(self.path+'\\'+str(s)+".fbx",f=True)
                        except Exception as e:
                            print(e)
                        s.setTransformation(oTrans)
                        self.printList += str(s) + '\n'

                self.printList += "\nExport in Center"
            else:
                for s in self.selectionList:
                    pm.select(s)
                    if "|" in s:
                        s = s.split("|")[-1]
                    pm.exportSelected(self.path+'\\'+str(s)+".fbx",f=True) #Export FBXs

                    self.printList += str(s) + '\n'

            self.window.delete()

            data[self.mayaName] = self.path

            # save path & prefer into json file
            with open(self.pathFile,"w") as f:
                json.dump(data, f,indent=4, sort_keys=True)
            with open(self.prefFile,"w") as f:
                json.dump(self.prefData, f,indent=4, sort_keys=True)
        
            confirm = pm.confirmDialog(title="Success",b=["Done","Open Folder"], message="Exported:\t\t\n\n" + self.printList,messageAlign ="left")
            if confirm == "Open Folder":
                os.startfile(self.path)
        else:
            self.changePath()

# ------------------------------------------------------------------ #

def searchPath(maya_name,path_file):
    '''
    Each Maya file has a path which saved in a JSON file named 'Path.json' used to export FBX.
    This function is used to search whether the export path has been saved in the JSON file.
    '''
    global data
    with open(path_file,"r") as f:
        data = json.loads(f.read())

    if maya_name in data:
        exportPath = data[maya_name]
    else:
        exportPath = data["tempPath"]

    return exportPath



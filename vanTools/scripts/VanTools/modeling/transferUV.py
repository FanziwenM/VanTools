#Author: Fanziwen (120416678@qq.com)
#Created: 08/13/2019
#Updated: 08/23/2019 
#Last Change: Created a preference["MayaPref" in "config.json"] file to save the transfer sample space 

import pymel.core as pm
import json


'''
    transferAttributes()

    - sampleSpace : spa              (int)           [create,edit]
        Selects which space the attribute transfer is performed in. 0 is world space, 1 is model space, 4 is component-based, 5
        is topology-based. The default is world space.

    - transferUVs : uvs              (int)           [create,edit]
        Controls UV set transfer. 0 means no UV sets are transferred, 1 means that a single UV set (specified by sourceUVSet and
        targetUVSet) is transferred, and 2 means that all UV sets are transferred.                  Flag can have multiple
        arguments, passed either as a tuple or a list.
'''

with open("config.json","r") as f:
    data = json.load(f)
prefFile = data["MayaPref"]

def main():

    UI = TransferWindow()

class TransferWindow():
    global prefFile
    def __init__(self, *args, **kwargs):
        '''
        Create a initialize window
            - Load prefences file to get Sample Space (if saved)
        '''
        self.sObject = None
        # load prefences file
        with open(prefFile, "r") as f:
            self.prefData = json.loads(f.read())

        # initialize window
        with pm.window(title="TransferUV", sizeable = False, toolbox = True ) as self.window:
            with pm.formLayout() as self.form:
                self.getButton = pm.button("Get UV",w=100,h=25, c=self.getUV)
                self.getName = pm.textField(placeholderText = "Null",editable=False, h=25)
                self.setButton = pm.button("Set UV",h=40, c= self.setUV,bgc = (0.28, 0.66, 0.71))
            with pm.frameLayout( label='Sample Space' ) as self.frame:
                    pass
            with pm.rowLayout(nc=6 ,adj=2) as self.row:
                
                # pm.text(label = "Sample Space: ")
                self.collection = pm.radioCollection()
                pm.radioButton("ss0", label='World' )
                pm.radioButton("ss1", label='Local' )
                pm.radioButton("ss4", label='Component' )
                pm.radioButton("ss5",  label='Topology' )
                pm.radioCollection(self.collection, e=True, select = self.prefData["sampleSpace"])
            pm.formLayout(
                self.form,edit=True,
                af = [
                    (self.getButton, "top", 5),
                    (self.getButton, "left", 5),
                    (self.getName, "top", 5),
                    (self.getName, "right", 5),
                    (self.setButton,"bottom", 5),
                    (self.setButton,"left", 5 ),
                    (self.setButton, "right", 5),
                    (self.row,"left", 5 ),
                    (self.row, "right", 5),
                    (self.frame,"left",5),
                    (self.frame, "right", 5),
                ],
                ac = [
                    (self.getName, "left", 5, self.getButton),
                    (self.frame, "top", 5, self.getButton),
                    (self.row, "top", 5, self.frame),
                    (self.setButton, "top", 5, self.row),
                ]
            )
        pm.showWindow(self.window)
    
    def getUV(self, *args):

        selectionList = pm.ls(sl=True)
        if selectionList:
            self.sObject = selectionList[-1]
            # pm.textField(self.getName, e=True, text = selectionList[-1])
            self.getName.setText(selectionList[-1])
        else:
            pm.confirmDialog(title="warning",message="Please select Object to Get UV", p = self.window)

    def setUV(self, *args):
        if self.sObject:
            selectionList = pm.ls(sl=True)
            if selectionList:
                # sObject = self.getName.getText()
                sample = pm.radioCollection(self.collection, q=True, sl=True)
                sampleSpace = sample.split("ss")[-1]
                for s in selectionList:
                    pm.transferAttributes(self.sObject, s, transferUVs = 2 ,sampleSpace = int(sampleSpace) )
                    pm.delete(s, ch = True)
                self.prefData["sampleSpace"] = sample
                with open(prefFile,"w") as f:
                    json.dump(self.prefData, f,indent=4, sort_keys=True)
            else:
                pm.confirmDialog(title="warning",message="Please select Object to Set UV", p = self.window)
        else:
            pm.confirmDialog(title="warning",message="Please get UV first", p = self.window)


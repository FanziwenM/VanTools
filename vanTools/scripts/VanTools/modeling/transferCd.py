# Author: Fanziwen (120416678@qq.com)
# Created: 04/15/2020


import pymel.core as pm


'''
    transferAttributes()

    - sampleSpace : spa              (int)           [create,edit]
        Selects which space the attribute transfer is performed in.
         0 is world space, 1 is model space, 4 is component-based, 5
        is topology-based. The default is world space.

    - transferColors : col	(int)
        Controls color set transfer. 0 means no color sets are transferred,
        1 means that a single color set (specified by sourceColorSet
         and targetColorSet) is transferred,
        and 2 means that all color sets are transferred.
'''


def main():

    UI = TransferWindow()
    UI.show()


class TransferWindow():
    global prefFile

    def __init__(self, *args, **kwargs):
        '''
        Create a initialize window
        '''
        self.sObject = None
        # initialize window
        with pm.window(
            title="Transfer Color", sizeable=False, toolbox=True
        ) as self.window:
            with pm.formLayout() as self.form:
                self.getButton = pm.button(
                    "Get Color", w=100, h=25, c=self.getUV)
                self.getName = pm.textField(
                    placeholderText="Null", editable=False, h=25)
                self.setButton = pm.button(
                    "Set Color", h=40, c=self.setUV, bgc=(0.28, 0.66, 0.71))

            pm.formLayout(
                self.form, edit=True,
                af=[
                    (self.getButton, "top", 5),
                    (self.getButton, "left", 5),
                    (self.getName, "top", 5),
                    (self.getName, "right", 5),
                    (self.setButton, "bottom", 5),
                    (self.setButton, "left", 5),
                    (self.setButton, "right", 5),

                ],
                ac=[
                    (self.getName, "left", 5, self.getButton),

                ]
            )
            pm.window(self.window, e=True, h=80)

    def show(self, *args):
        pm.showWindow(self.window)

    def getUV(self, *args):
        selectionList = pm.ls(sl=True)
        if selectionList:
            self.sObject = selectionList[-1]
            # pm.textField(self.getName, e=True, text = selectionList[-1])
            self.getName.setText(selectionList[-1])
        else:
            pm.confirmDialog(
                title="warning",
                message="Please select Object to Get UV",
                p=self.window
                )

    def setUV(self, *args):
        if self.sObject:
            selectionList = pm.ls(sl=True)
            if selectionList:
                # sObject = self.getName.getText()
                for s in selectionList:
                    pm.transferAttributes(
                        self.sObject, s, transferColors=2, sampleSpace=0)
                    pm.delete(s, ch=True)
            else:
                pm.confirmDialog(
                    title="warning",
                    message="Please select Object to Set UV",
                    p=self.window
                    )
        else:
            pm.confirmDialog(
                title="warning", message="Please get UV first", p=self.window)

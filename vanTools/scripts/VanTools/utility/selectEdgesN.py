#Author: fanziwen
#Created: 09/25/2019


import pymel.core as pm
import maya.mel as mel


class SelectEdgesWindow():

    def __init__(self, *args, **kwargs):
        
        with pm.window(title = "Select Edges",toolbox=True, sizeable=False) as self.window:
            with pm.columnLayout(adj=True,co = ("both",2),rs=3) as self.column:
                with pm.rowLayout(nc=3) as self.colRow:
                    pm.text("Mode:")
                    self.collection = pm.radioCollection()
                    pm.radioButton("Ring", label='Ring' )
                    pm.radioButton("Loop", label='Loop' )
                    pm.radioCollection(self.collection, e=True, sl="Ring")
                with pm.rowLayout(nc=2) as self.intRow:
                    pm.text("Edge Interval:")
                    self.interval =  pm.intField(value = 2,w=57)
                pm.button("Select Edge",c=self.selectEdges,bgc = (0.28, 0.66, 0.71))
        pm.showWindow(self.window)
    
    def selectEdges(self,*args):
        selectMode = pm.radioCollection(self.collection, q=True, sl=True)
        intervalEdge = pm.intField(self.interval, q=True, v=True)

        mel.eval('polySelectEdgesEveryN "edge{}" {}'.format(selectMode,intervalEdge))

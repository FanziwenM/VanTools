#Author: Fanziwen (120416678@qq.com)
#Created: 10/11/2019

import pymel.core as pm 
import re


class VanMesh():
    '''
    The properties of mesh my commonly used
    '''
    def __init__(self,selectionList, *args, **kwargs):
        self.selList = pm.ls(selectionList, fl=True)
        self.obj = pm.ls(selectionList, o=True)[0]
        self.vxtSum = pm.polyEvaluate(self.obj, v=True)

        # Return a list of Vertices in Maya format, like: "polyCube.vtx[1]"
        self.vtxList = ["{}.vtx[{}]".format(self.obj, i) for i in range(self.vxtSum)]

    def getVFList(self, vertex,*args):
        '''
        Get VertexFace through vertex
        '''
        oVtxIdx = vertex.split(".vtx")[1]
        vfInfo = pm.polyInfo(vertex, vf=True)
        vfIdx = re.findall("\s([0-9]+)\s", vfInfo[0])
        vfList = ["{}.vtxFace{}[{}]".format(self.obj, oVtxIdx, vfI) for vfI in vfIdx]
        return vfList
    
    def normalCompare(self,vertex1, vertex2, *args):
        '''
        Compare two vectors whether is the same
        '''
        v1N = pm.polyNormalPerVertex(vertex1, q=True, xyz=True)
        v2N = pm.polyNormalPerVertex(vertex2, q=True, xyz=True)
        res = (v1N[0]-v2N[0])*(v1N[0]-v2N[0]) + (v1N[1]-v2N[1])*(v1N[1]-v2N[1]) + (v1N[2]-v2N[2])*(v1N[2]-v2N[2])
        if res == 0:
            return True
        else:
            return False

    def smartUnlockNormal(self,*args):
        '''
        Unlock Normal with smooth/hard edges
        '''
        softEdges = []
        for vtx in self.vtxList:
            vfList = self.getVFList(vtx)
            vfOld = vfList[-1]
            for vf in vfList:
                if self.normalCompare(vf, vfOld):
                    softEdges.append(pm.polyListComponentConversion(vf, te=True))
                vfOld = vf
        pm.polyNormalPerVertex(self.obj, ufn = True)
        pm.polySoftEdge(self.obj, a=0)
        
        if softEdges:
            pm.select(softEdges)
            pm.polySoftEdge(a=180)
        pm.select(self.selList)
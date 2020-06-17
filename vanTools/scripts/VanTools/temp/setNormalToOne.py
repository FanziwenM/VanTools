import pymel.core as pm

def getVFList(obj, vertex, *args):
    '''
    Get VertexFace through vertex
    '''
    import re
    oVtxIdx = vertex.split(".vtx")[1]
    vfInfo = pm.polyInfo(vertex, vf=True)
    vfIdx = re.findall("\s([0-9]+)\s", vfInfo[0])
    vfList = [
        "{}.vtxFace{}[{}]".format(obj, oVtxIdx, vfI) for vfI in vfIdx
        ]
    return vfList


def setNormaltoOne(vtxFace_list):
    unlockNs = []
    hasLockN = False
    for vf in vtxFace_list:
        Locked = pm.polyNormalPerVertex(vf, q=True, fn=True)
        if Locked[0]:
            hasLockN = True
            lockN = pm.polyNormalPerVertex(vf, q=True, xyz=True)
        else:
            unlockNs.append(vf)
    if hasLockN:
        for unlvf in unlockNs:
            pm.polyNormalPerVertex(unlvf, xyz=lockN)
                
    


selList = pm.ls(sl=True, fl=True)
obj = pm.ls(sl=True, o=True)


for s in selList:
    vf = getVFList(obj[0], s)
    setNormaltoOne(vf)


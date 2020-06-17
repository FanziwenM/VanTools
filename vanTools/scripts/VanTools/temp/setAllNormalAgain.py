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


def setNormalAgain():
    selList = pm.ls(sl=True, fl=True)
    selObj = pm.ls(sl=True, o=True)[0]
    selVtx = pm.polyListComponentConversion(selList, tv=True)
    pm.select(selVtx)
    vtxs = pm.ls(sl=True, fl=True)
    allVF = []
    allVFnormal = []
    for vtx in vtxs:
        if all(pm.polyNormalPerVertex(vtx, q=True, fn=True)):
            vfs = getVFList(selObj, vtx)
            allVF += vfs
            for vf in vfs:
                allVFnormal.append(pm.polyNormalPerVertex(vf, q=True, xyz=True))

        else:
            speVFlist = getVFList(selObj, vtx)
            allVF += speVFlist
            for vf in speVFlist:
                Locked = pm.polyNormalPerVertex(vf, q=True, fn=True)
                if Locked[0]:
                    lockN = pm.polyNormalPerVertex(vf, q=True, xyz=True)
                    break
            for _ in speVFlist:
                allVFnormal.append(lockN)

    i = 0
    for vf in allVF:
        pm.polyNormalPerVertex(vf, xyz=allVFnormal[i])
        i += 1

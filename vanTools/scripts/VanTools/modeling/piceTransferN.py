# Author: Fanziwen (120416678@qq.com)
# Created: 05/25/2020

import pymel.core as pm

orig_N = None


def main():
    global orig_N
    orig_N = None
    try:
        pm.deleteUI("transferNormalPices231")
    except Exception as e:
        print(e)

    with pm.window(
        "transferNormalPices231",
        title="Transfer Normal Pices", sizeable=False, toolbox=True
    ) as window:
        with pm.formLayout() as form:
            getButton = pm.button(
                "Copy Normal", w=100, h=25,
                c=getNormal
                )
            getName = pm.textField(
                "NormalField",
                placeholderText="Null", editable=False, h=25
                )
            setButton = pm.button(
                "Set Normal", h=40, bgc=(0.28, 0.66, 0.71),
                c=setNormal
                )

        pm.formLayout(
            form, edit=True,
            af=[
                (getButton, "top", 5),
                (getButton, "left", 5),
                (getName, "top", 5),
                (getName, "right", 5),
                (setButton, "bottom", 5),
                (setButton, "left", 5),
                (setButton, "right", 5),
            ],
            ac=[
                (getName, "left", 5, getButton),
            ]
        )
        pm.window(window, e=True, h=80)

    pm.showWindow(window)


def getNormal(*args):
    global orig_N
    selList = pm.ls(sl=True)
    pm.textField("NormalField", e=True, placeholderText=str(selList))
    orig_N = selList


def setNormal(*args):
    '''
    if the ' pm.textField(meshName) ' is define,
     setting selected mesh normal from the defined name
    '''
    selList = pm.ls(sl=True)
    pm.select(orig_N)
    obj = pm.ls(sl=True, o=True)[0]
    if pm.nodeType(obj) != "transform":
        obj = obj.getParent()
    oTrans = obj.getTransformation()
    obj.resetFromRestPosition()

    if orig_N:
        '''
        transferAttributes()
            - sampleSpace : spa       (int)      [create,edit]
                Selects which space the attribute transfer is performed in
                0 is world space,
                1 is model space,
                4 is component-based,
                5 is topology-based.
                The default is world space.
        '''
        # selList = pm.polyListComponentConversion(selList, tvf=True)
        sScale = 1.01
        pm.transferAttributes(
            orig_N, selList,
            transferNormals=1, sampleSpace=0,
            sm=0,
            ssx=sScale,
            ssy=sScale,
            ssz=sScale
            )
    else:
        pm.warning("Please get Normal first")

    pm.select(selList)
    tarObj = pm.ls(sl=True, o=True)[0]
    # pm.delete(obj, ch=True)
    pm.delete(tarObj, ch=True)
    obj.setTransformation(oTrans)
    # setNormalAgain(selList)
    pm.select(selList)
    pm.select(tarObj)
    # selVtx = pm.polyListComponentConversion(selList, tv=True)
    # pm.select(selVtx)


def getVFList(obj, vertex, *args):
    '''
    Get VertexFace through vertex
    '''
    import re
    oVtxIdx = vertex.split(".vtx")[1]
    vfInfo = pm.polyInfo(vertex, vf=True)
    vfIdx = re.findall("\\s([0-9]+)\\s", vfInfo[0])
    vfList = [
        "{}.vtxFace{}[{}]".format(obj, oVtxIdx, vfI) for vfI in vfIdx
        ]
    return vfList


def setNormalAgain(selList):
    allVF = []
    allVFnormal = []
    hardEdge = []
    pm.select(selList)
    selObj = pm.ls(sl=True, o=True)[0]
    selVtx = pm.polyListComponentConversion(selList, tv=True)
    selEdge = pm.polyListComponentConversion(selList, te=True)
    pm.select(selVtx)
    vtxs = pm.ls(sl=True, fl=True)

    for vtx in vtxs:
        if all(pm.polyNormalPerVertex(vtx, q=True, fn=True)):
            vfs = getVFList(selObj, vtx)
            allVF += vfs
            vfOld = vfs[-1]
            for vf in vfs:
                allVFnormal.append(
                    pm.polyNormalPerVertex(vf, q=True, xyz=True)
                    )
                if not normalCompare(vf, vfOld):
                    hardEdge.append(
                        pm.polyListComponentConversion(vf, te=True)
                    )
                vfOld = vf

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

    pm.polySoftEdge(selEdge, a=180)

    if hardEdge:
        pm.select(hardEdge)
        pm.polySoftEdge(a=0)

    smartUnlockNormal(selObj, vtxs)


def normalCompare(vertex1, vertex2, *args):
    '''
    Compare two vectors whether is the same
    '''
    v1N = pm.polyNormalPerVertex(vertex1, q=True, xyz=True)
    v2N = pm.polyNormalPerVertex(vertex2, q=True, xyz=True)
    res = (v1N[0]-v2N[0])*(v1N[0]-v2N[0])\
        + (v1N[1]-v2N[1])*(v1N[1]-v2N[1])\
        + (v1N[2]-v2N[2])*(v1N[2]-v2N[2])
    if res == 0:
        return True
    else:
        return False


def smartUnlockNormal(obj, vtxList, *args):
    '''
    Unlock Normal with smooth/hard edges
    '''
    softEdges = []
    for vtx in vtxList:
        vfList = getVFList(obj, vtx)
        vfOld = vfList[-1]
        for vf in vfList:
            if normalCompare(vf, vfOld):
                softEdges.append(
                    pm.polyListComponentConversion(vf, te=True)
                    )
            vfOld = vf
    # pm.polyNormalPerVertex(obj, ufn=True)
    selEdges = pm.polyListComponentConversion(vtxList, te=True)
    pm.polySoftEdge(selEdges, a=0)

    if softEdges:
        pm.select(softEdges)
        pm.polySoftEdge(a=180)

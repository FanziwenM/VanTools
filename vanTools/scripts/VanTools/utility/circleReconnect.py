import pymel.core as pm



selList = pm.ls(sl=True, fl=True)

if isinstance(selList[0], pm.MeshEdge):
    print("edge")
    selFaces = pm.polyListComponentConversion(selList,fe=True, tf=True)
    pm.select(selFaces)
    selFaces = pm.ls(sl=True, fl=True)
    pm.delete(selList)
    pm.select(selFaces[0])

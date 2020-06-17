import pymel.core as pm

selList = pm.ls(sl=True)
uvSet = 1
for s in selList:
    mesh = s.getShape()
    uvNames = mesh.getUVSetNames()
    pm.polyUVSet(mesh, currentUVSet=True, uvSet=uvNames[uvSet])

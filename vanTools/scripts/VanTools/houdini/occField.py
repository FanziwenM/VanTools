import pymel.core as pm


def main():
    selList = pm.ls(sl=True)

    if selList:
        hdaPath = r"C:\Users\fanziwen\Documents\houdini18.0\otls\occCommon.hda"
        sopName = r"Sop/occCommon"
        hdaTool = None
        hdaTool = pm.houdiniAsset(loadAsset=(hdaPath, sopName))

        for i in range(len(selList)):
            pm.hide(selList[i])
            inputMesh(i, selList[i], hdaTool)

        pm.houdiniAsset(sync=hdaTool)
        pm.select(hdaTool)
        houNode = pm.ls(sl=True)[0]
        pm.setAttr(houNode.splitGeosByGroup, 1)
        pm.houdiniAsset(sync=hdaTool)

    else:
        pm.PopupError("No object selection, or too many objects selected")


def inputMesh(i, trans_node, houdini_HDA):
    # try:
    houNode = pm.createNode("houdiniInputGeometry")
    trans_node.getShape().outMesh >> houNode.inputGeometry
    trans_node.worldMatrix[0] >> houNode.inputTransform
    houNode.outputNodeId >> (
        houdini_HDA + ".input[" + str(i) + "].inputNodeId"
        )

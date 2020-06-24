# Author: fanziwen (120416678@qq.com)
# Created: 04/03/2020
# Updated: 06/22/2020
# Last change:
#       06/22/2020:
#       - Modify input check, don't care if "hair" is inputed
#       - Add cage mesh display
#       04/07/2020:
#       - Add input check. Checking if all input has a valid value

import pymel.core as pm
import os


def main():

    selList = pm.ls(sl=True)

    if not ((len(selList) == 4) or (len(selList) == 3)):
        pm.PopupError("Incorrect Number of Selection")
        return 0

    inDict = sortingSelection(selList)

    inputCheck = True
    for k, v in inDict.items():
        if v == 0:
            if k != "hair":
                inputCheck = False
                pm.PopupError("The input [{}] not found".format(str(k)))
                break

    if inputCheck:
        # houdini setting
        # pm.loadPlugin("houdiniEngine.mll")
        hdaPath = r"C:\Users\fanziwen\Documents\houdini18.0\otls\S1_Occ2VtxCd.hda"
        # hdaPath = os.getcwd() + r"\HDA\S1_Occ2VtxCd.hda"
        sopName = r"Sop/S1_Occ2VtxCd"
        hdaTool = None
        hdaTool = pm.houdiniAsset(loadAsset=(hdaPath, sopName))
        if inDict["hair"]:
            inputMesh(0, inDict["hair"], hdaTool)
        inputMesh(1, inDict["head"], hdaTool)
        inputMesh(2, inDict["eyes"], hdaTool)
        inputMesh(3, inDict["haircap"], hdaTool)

        pm.select(hdaTool)
        houNode = pm.ls(sl=True)[0]
        pm.setAttr(houNode.splitGeosByGroup, 1)
        # Determine whether a `Cage model` is required from `check box`
        useCage = pm.checkBox("charOccCheckBox", q=True, v=True)
        if useCage:
            # create Shading Group for Cage
            if not pm.objExists("cageSG"):
                pm.sets(
                    renderable=True,
                    noSurfaceShader=True,
                    empty=True,
                    name="cageSG"
                )
                pm.connectAttr('lambert1.outColor', 'cageSG.surfaceShader')
            pm.setAttr(houNode.houdiniAssetParm_useCage, 1)
            pm.houdiniAsset(sync=hdaTool)
            renameOutput(houNode)
            setCageMat()

        else:
            pm.houdiniAsset(sync=hdaTool)
            renameOutput(houNode)

    else:
        print("Cooking failed")


def nameCheck(name):
    if "|" in name:
        return name.split("|")[-1]
    else:
        return name


def inputMesh(i, trans_node, houdini_HDA):
    # try:
    houNode = pm.createNode("houdiniInputGeometry")
    trans_node.getShape().outMesh >> houNode.inputGeometry
    trans_node.worldMatrix[0] >> houNode.inputTransform
    houNode.outputNodeId >> (
        houdini_HDA + ".input[" + str(i) + "].inputNodeId")
    # except AttributeError:
    #     pass


def sortingSelection(selection_list):

    inputDic = {
        "hair": 0,
        "head": 0,
        "eyes": 0,
        "haircap": 0
    }

    for s in selection_list:
        rName = nameCheck(s)
        prefix = rName.split("_")[0]

        if prefix in inputDic:
            inputDic[prefix] = s
        else:
            pm.PopupError("Error Name: {}".format(s))
            return 0
    return inputDic


def renameOutput(houdini_asset):
    group = houdini_asset.getChildren()[0]
    outputGeo = group.getChildren()
    for s in outputGeo:

        rName = nameCheck(s)
        prefix = rName.split("_")[0]
        pm.rename(s, prefix + "_0_lod0")


def setCageMat():
    if not pm.objExists("cage_mat"):
        cageMat = pm.shadingNode(
            "blinn", asShader=True, name="cage_mat"
        )
        pm.setAttr("{}.color".format(cageMat), 0.45, 0.45, 0.45)
        pm.setAttr("{}.transparency".format(cageMat), 0.6, 0.6, 0.6)

    pm.disconnectAttr("cageSG.surfaceShader")
    pm.connectAttr("{}.outColor".format("cage_mat"), "cageSG.surfaceShader")
    pm.polyOptions("cage_0_lod0", colorShadedDisplay=False)



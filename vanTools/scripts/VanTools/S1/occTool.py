# Author: fanziwen (120416678@qq.com)
# Created: 04/03/2020
# Updated: 04/07/2020
# Last change:
#       - Add input check. Checking if all input has a valid value

import pymel.core as pm


def main():

    selList = pm.ls(sl=True)
    if len(selList) != 4:
        pm.PopupError("Incorrect Number of Selection")
        return 0

    inDict = sortingSelection(selList)

    inputCheck = True
    for k, v in inDict.items():
        if v == 0:
            inputCheck = False
            pm.PopupError("The input [{}] not found".format(str(k)))
            break

    if inputCheck:
        # houdini setting
        # pm.loadPlugin("houdiniEngine.mll")


        hdaPath = r"Z:\S1\artist\artTools\maya_scripts\vanTools\scripts\VanTools\HDA\S1_Occ2VtxCd.hda"
        sopName = r"Sop/S1_Occ2VtxCd"
        hdaTool = None
        hdaTool = pm.houdiniAsset(loadAsset=(hdaPath, sopName))

        inputMesh(0, inDict["hair"], hdaTool)
        inputMesh(1, inDict["head"], hdaTool)
        inputMesh(2, inDict["eyes"], hdaTool)
        inputMesh(3, inDict["haircap"], hdaTool)

        # pm.setAttr(hdaTool.splitGeosByGroup, 1)
        pm.select(hdaTool)
        houNode = pm.ls(sl=True)[0]
        pm.setAttr(houNode.splitGeosByGroup, 1)
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

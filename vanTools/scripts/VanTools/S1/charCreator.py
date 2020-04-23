# Author: fanziwen (120416678@qq.com)
# Created: 04/09/2020
# Updated: 04/16/2020
#       - add function `closeSubWin()`
#           to close all other sub-windows like tone, face, and hair


import pymel.core as pm
import os
import json
from functools import partial


sourcePath = "D:\\S1Tool\\source\\"
defaultImg200 = sourcePath + "default200x200.png"
defaultImg100 = sourcePath + "default100x100.png"
hdaTool = None
# headType = "btB"


linkTexName = None


def main():
    global hdaTool
    hdaPath = r"C:\Users\fanziwen\Documents\
        \houdini18.0\otls\S1_CharacterCreator.hda"
    sopName = r"Sop/S1_CharacterCreator"
    hdaTool = pm.houdiniAsset(loadAsset=(hdaPath, sopName))
    pm.select(hdaTool)
    houNode = pm.ls(sl=True)[0]
    pm.setAttr(houNode.splitGeosByGroup, 1)
    pm.houdiniAsset(sync=hdaTool)
    mainWin()


def mainWin():
    ww = 250
    hh = 200
    # delete old main windows
    try:
        pm.deleteUI("mainWin3912")
    except Exception as e:
        print(e)

    # create a new Main Windows
    with pm.window("mainWin3912", t="S1 Character Creator") as mainWin:
        with pm.columnLayout() as mainLayout:
            with pm.frameLayout(label="Head Type", w=ww) as _:
                with pm.rowLayout(nc=3) as _:
                    pm.radioCollection("headTypeCollection")
                    pm.radioButton(
                        "black", label='Black', w=ww/3, cc=headSwitch
                        )
                    pm.radioButton(
                        "white", label='White', w=ww/3, cc=headSwitch
                        )
                    pm.radioButton(
                        "yellow", label='Yellow', w=ww/3, cc=headSwitch
                        )
                    pm.radioCollection(
                        "headTypeCollection", e=True, sl="white"
                        )

            with pm.frameLayout(label="Hair", w=ww) as _:
                with pm.rowLayout(nc=2, adj=1) as _:
                    pm.textField(
                        "hairTextField",
                        placeholderText="default", editable=False, h=25
                    )
                    pm.button("Change", command=showHairWin)
            with pm.frameLayout(label="Face", w=ww) as _:
                with pm.rowLayout(nc=2, adj=1) as _:
                    pm.textField(
                        "skinTextField",
                        placeholderText="default", editable=False, h=25
                    )
                    pm.button("Change", c=showSkinWin)
                with pm.rowLayout(nc=2, adj=1) as _:
                    pm.textField(
                        "faceTextField",
                        placeholderText="default", editable=False, h=25
                    )
                    pm.button(
                        "Change",
                        command=partial(showFaceWin)
                        )

            pm.columnLayout(mainLayout, e=True, w=ww, h=hh)
        pm.window(mainWin, e=True, w=ww, h=hh, sizeable=False, toolbox=True)

    pm.showWindow(mainWin)


# --------------head part-----------------#
def headSwitch(*args):
    hairType = pm.radioCollection("headTypeCollection", q=True, sl=True)
    # setAttr "S1_CharacterCreator1.houdiniAssetParm_headType" 0
    typeDict = {
        "black": 0,
        "white": 1,
        "yellow": 2
    }
    pm.setAttr(hdaTool + ".houdiniAssetParm_headType", typeDict[hairType])
    pm.houdiniAsset(sync=hdaTool)
    resetMat()


# ----------------hair part----------------------#
def showHairWin(*args):
    headType = pm.radioCollection("headTypeCollection", q=True, sl=True)
    # hairPathDict = {
    #     "black": sourcePath + "black\\hair\\",
    #     "white": sourcePath + "white\\hair\\",
    #     "yellow": sourcePath + "yellow\\hair\\"
    # }
    # try delete unclose hair windows
    closeSubWin()

    # hairPath = hairPathDict[headType]
    with open(sourcePath + "_config.json", "r") as f:
        data = json.load(f)
        hairData = data[headType]["hair"]

    # create hair windows
    with pm.window(
        "hairWin122", t="Hair", toolbox=True, sizeable=False
    ) as hairWin:
        with pm.scrollLayout(w=350) as _:
            i = 0.0
            numHair = float(len(hairData.keys()))
            for k in sorted(hairData.keys()):
                image = "{}{}/hair/{}.png".format(
                    sourcePath, headType, k
                    )
                # image check
                if not os.path.exists(image):
                    image = defaultImg200
                v = (i + 0.5)/numHair
                pm.iconTextButton(
                    style="iconAndTextHorizontal",
                    image1=image, label=k, w=330,
                    ann=hairData[k]["mesh"],
                    # use the partial function
                    # to pass your arguments in the function
                    command=partial(switchHair, v, k)
                )
                i += 1.0

        pm.window(hairWin, e=True, h=700)
    pm.showWindow(hairWin)


def switchHair(velue, name):
    matH = "lambert1"
    matHC = "lambert1"
    pm.setAttr(hdaTool + ".houdiniAssetParm_hairSelect", velue)
    pm.deleteUI("hairWin122")
    pm.textField("hairTextField", e=True, placeholderText=name)

    hairMat = name + "_H"
    haircapMat = name + "_HC"

    if pm.objExists(hairMat):
        matH = hairMat
    if pm.objExists(haircapMat):
        matHC = haircapMat

    pm.disconnectAttr("hairSG.surfaceShader")
    pm.connectAttr("{}.outColor".format(matH), "hairSG.surfaceShader")
    pm.disconnectAttr("haircapSG.surfaceShader")
    pm.connectAttr("{}.outColor".format(matHC), "haircapSG.surfaceShader")
    pm.houdiniAsset(sync=hdaTool)

    if pm.objExists(hairMat):
        global linkTexName
        pm.select("hair_2")
        selList = pm.ls(sl=True)
        uvSet = selList[0].getShape().uvSet[1].uvSetName
        linkTexName = name + "_tex_d"
        pm.uvLink(uvSet=uvSet, texture=linkTexName)
        pm.select(cl=True)


# ----------------skin part----------------------#
def showSkinWin(*args):
    skinType = pm.radioCollection("headTypeCollection", q=True, sl=True)

    # reading skin data
    with open(sourcePath + "_config.json", "r") as f:
        Data = json.load(f)[skinType]["skin"]

    # delete old skin windows
    closeSubWin()
    # creating new skin windows
    with pm.window(
        "skinWin3920", t="Skin", toolbox=True, sizeable=False,
    ) as skinWin:
        with pm.scrollLayout() as _:
            dictNum = float(len(Data.keys()))
            i = 0
            for skinTone in sorted(Data.keys()):
                skinImage = (
                    sourcePath + str(skinType)
                    + "\\skin\\" + str(skinTone) + ".png"
                )
                if not os.path.exists(skinImage):
                    skinImage = defaultImg100
                v = (i + 0.5)/dictNum
                pm.iconTextButton(
                    style="iconAndTextHorizontal",
                    image1=skinImage, label=skinTone, w=180,
                    command=partial(switchSkin, v, skinTone)
                )
                i += 1
        pm.window(skinWin, e=True, w=200)

    pm.showWindow(skinWin)


def switchSkin(velue, tone):
    pm.setAttr(hdaTool + ".houdiniAssetParm_toneSwitch", velue)
    pm.houdiniAsset(sync=hdaTool)
    pm.deleteUI("skinWin3920")
    pm.textField("skinTextField", e=True, placeholderText=tone)
    showFaceWin(tone)
    if linkTexName:
        refreshUVlink()


# ----------------face part---------------------#
def showFaceWin(tone, *args):
    headType = pm.radioCollection("headTypeCollection", q=True, sl=True)

    with open(sourcePath + "_config.json", "r") as f:
        data = json.load(f)[headType]["skin"]

    # try delete unclose hair windows
    closeSubWin()
    # load skin json file

    tone = pm.textField("skinTextField", q=True, placeholderText=True)
    faceData = data[tone]
    dataNum = float(len(faceData.keys()))
    hh = min(dataNum * 200 + 50, 700)
    # creating face windows
    with pm.window(
        "faceWin982", t="Face", toolbox=True, sizeable=False
    ) as faceWin:
        with pm.scrollLayout(w=350) as _:
            i = 0.0
            for k in sorted(faceData.keys()):
                image = faceData[k].split(".")[0] + ".png"
                # image check
                if not os.path.exists(image):
                    image = defaultImg200
                v = (i + 0.5)/dataNum
                pm.iconTextButton(
                    style="iconAndTextHorizontal",
                    image1=image, label=k, w=330,
                    ann=faceData[k],
                    # use the partial function
                    # to pass your arguments in the function
                    command=partial(switchFace, k, v)
                )
                i += 1.0
        pm.window(faceWin, e=True, h=hh)
    pm.showWindow(faceWin)


def switchFace(k, v, *args):
    mat = "lambert1"
    pm.setAttr(hdaTool + ".houdiniAssetParm_faceSwitch", v)
    pm.textField("faceTextField", e=True, placeholderText=k)
    if pm.objExists(k):
        mat = k
    pm.disconnectAttr("faceSG.surfaceShader")
    pm.connectAttr("{}.outColor".format(mat), "faceSG.surfaceShader")
    pm.houdiniAsset(sync=hdaTool)
    pm.deleteUI("faceWin982")

    if linkTexName:
        refreshUVlink()


def closeSubWin(*args):
    subwinList = ["hairWin122", "skinWin3920", "faceWin982"]
    for subWin in subwinList:
        try:
            pm.deleteUI("%s" % subWin)
        except Exception as e:
            print(e)


def refreshUVlink(*args):
    '''
    uvlink is always lost when the houdini asset is synchronized.
    So create a function to avoid link lost
    '''
    pm.select("hair_2")
    selList = pm.ls(sl=True)
    uvSet = selList[0].getShape().uvSet[1].uvSetName
    pm.uvLink(uvSet=uvSet, texture=linkTexName)
    pm.select(cl=True)
    # pm.sets("eyesSG", e=True, forceElement="hair_2")
    # pm.sets("hairSG", e=True, forceElement="hair_2")


def resetMat(*args):
    shaderGrpList = ["faceSG", "hairSG", "eyesSG", "haircapSG"]
    for sg in shaderGrpList:
        pm.disconnectAttr("%s.surfaceShader" % sg)
        pm.connectAttr('lambert1.outColor', '%s.surfaceShader' % sg)

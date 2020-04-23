# Author: fanziwen (120416678@qq.com)
# Created: 04/15/2020
# Updated: 04/16/2020
#       - add shader group `eyesSG`


import pymel.core as pm
import json

sourcePath = r"D:/S1Tool/source/"
headType = ["black", "white", "yellow"]
with open(sourcePath + "_config.json", "r") as f:
    data = json.load(f)


def main():

    # import skin texture and create shader
    for t in headType:
        for tone in data[t]["skin"].keys():
            for texName, texFile in data[t]["skin"][tone].items():

                if pm.objExists(texName):
                    pm.select(texName)
                    pm.delete()
                # create material
                mat = pm.shadingNode("blinn", asShader=True, name=texName)
                pm.setAttr("{}.specularColor".format(mat), 0.02, 0.02, 0.02)

                if pm.objExists(texName + "_tex"):
                    pm.select(texName + "_tex")
                    pm.delete()
                # import textures
                texNode = pm.shadingNode(
                    "file", asTexture=True, name=texName + "_tex"
                )
                pm.setAttr("{}.fileTextureName".format(texNode), texFile)
                # set texture to material
                pm.connectAttr("%s.outColor" % texNode, "%s.color" % mat)

    for t in headType:
        for hairName, cont in data[t]["hair"].items():
            if cont.__contains__("tex_a"):
                createHairMat(cont["tex_d"], cont["tex_a"], hairName)

    checkShaderGroup()


def createEyesMat():

    return 0


def createHairMat(tex_d, tex_a, hair_name, *args):
    cleanOldNode(
        hair_name + "_H",
        hair_name + "_HC",
        hair_name + "_tex_d",
        hair_name + "_tex_a",
        hair_name + "_rev"
    )
    hairMat = pm.shadingNode(
        "blinn", asShader=True, name=hair_name + "_H"
        )
    haircapMat = pm.shadingNode(
        "blinn", asShader=True, name=hair_name + "_HC"
        )
    pm.setAttr("{}.specularColor".format(hairMat), 0.02, 0.02, 0.02)
    pm.setAttr("{}.specularColor".format(haircapMat), 0.02, 0.02, 0.02)

    texNodeD = pm.shadingNode(
        "file", asTexture=True, name=hair_name + "_tex_d"
    )
    pm.setAttr("{}.fileTextureName".format(texNodeD), tex_d)
    texNodeA = pm.shadingNode(
        "file", asTexture=True, name=hair_name + "_tex_a"
    )
    pm.setAttr("{}.fileTextureName".format(texNodeA), tex_a)

    revNode = pm.shadingNode(
        "reverse", asUtility=True, name=hair_name + "_rev"
    )

    pm.connectAttr("%s.outColor" % texNodeD, "%s.color" % hairMat)
    pm.connectAttr("%s.outColor" % texNodeD, "%s.color" % haircapMat)
    pm.connectAttr("%s.outColor" % texNodeA, "%s.input" % revNode)
    pm.connectAttr("%s.outputY" % revNode, "%s.transparencyR" % hairMat)
    pm.connectAttr("%s.outputY" % revNode, "%s.transparencyG" % hairMat)
    pm.connectAttr("%s.outputY" % revNode, "%s.transparencyB" % hairMat)
    pm.connectAttr("%s.outputX" % revNode, "%s.transparencyR" % haircapMat)
    pm.connectAttr("%s.outputX" % revNode, "%s.transparencyG" % haircapMat)
    pm.connectAttr("%s.outputX" % revNode, "%s.transparencyB" % haircapMat)
    # pm.uvLink(make=True, uvSet='hair_2.uvSet[1].uvSetName', texture=texNodeD)


def checkShaderGroup():
    '''
    check or create Shader Group
    '''
    shaderGrpList = ["faceSG", "hairSG", "eyesSG", "haircapSG"]
    for sg in shaderGrpList:
        if not pm.objExists("%s" % sg):
            pm.sets(renderable=True, noSurfaceShader=True,
                    empty=True, name="%s" % sg)
            pm.connectAttr('lambert1.outColor', '%s.surfaceShader' % sg)
        else:
            try:
                pm.connectAttr('lambert1.outColor', '%s.surfaceShader' % sg)
            except Exception as e:
                print(e)


def cleanOldNode(*args):
    for i in args:
        if pm.objExists(i):
            pm.select(i)
            pm.delete()

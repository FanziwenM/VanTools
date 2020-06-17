# Author: Fanziwen (120416678@qq.com)
# Created: 08/11/2019

import pymel.core as pm


def main():
    selectionList = pm.ls(sl=True)      # select faces
    if selectionList and isinstance(selectionList[0], pm.MeshFace):
        originalMesh = pm.ls(selectionList, o=True)[0]     # get the mesh by selected faces
        originalTran = pm.listRelatives(originalMesh, p=True)[0]    # get TransformName

        duplicateMesh = pm.duplicate(originalTran, n=originalTran + "_dup")

        facesIndex = getFacesIndex2(selectionList)
        duplicateFaces = []
        for i in facesIndex:
            duplicateFaces.append(duplicateMesh[0] + ".f" + i)

        pm.select(duplicateFaces)
        newSelected = pm.ls(sl=True)
        invertSelection(newSelected)
        pm.delete()
        pm.select(selectionList)
        pm.select(duplicateMesh)
        pm.xform(cp=True)
        pm.makeIdentity(duplicateMesh, apply=True, t=True)

    else:
        pm.confirmDialog(title="error", message="No faces be selected")
        return


def getFacesIndex2(faces):
    if isinstance(faces[0], pm.MeshFace):
        index = []
        for f in faces:
            i = f.split(".f")[-1]
            index.append(i)
        return index  # return type:list
    else:
        print("Please select faces!")
        return 0


def invertSelection(selectionList):
    if isinstance(selectionList[0], pm.MeshFace):
        print("faces")
        mesh = pm.ls(selectionList, o=True)
        pm.select(mesh[0]+".f[*]")
        pm.select(selectionList, tgl=True)

    elif isinstance(selectionList[0], pm.MeshEdge):
        print("edges")
        mesh = pm.ls(selectionList, o=True)
        pm.select(mesh[0]+".e[*]")
        pm.select(selectionList, tgl=True)

    elif isinstance(selectionList[0], pm.MeshVertex):
        print("verts")
        mesh = pm.ls(selectionList, o=True)
        pm.select(mesh[0]+".vtx[*]")
        pm.select(selectionList, tgl=True)

    else:
        print("Please select faces,edges or verts")




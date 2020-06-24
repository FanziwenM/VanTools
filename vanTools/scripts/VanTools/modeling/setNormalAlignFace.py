import pymel.core as pm
import collections


def main(*args):

    selList = pm.ls(sl=True, fl=True)

    vtxDict = collections.defaultdict(list)
    if isinstance(selList[0], pm.MeshFace):
        sEdges, hEdges = splitEdge(selList)
        hFace = pm.polyListComponentConversion(hEdges, tf=True)
        hFace = pm.filterExpand(hFace, sm=34)

        if hFace:
            hFace = map(pm.MeshEdge, hFace)
        for f in selList:
            fArea = f.getArea()
            fNormal = f.getNormal()
            if hFace and (f in hFace):
                print f
                specialVFs(f, fNormal)
            else:
                vtx = pm.polyListComponentConversion(f, tv=True)
                vtx = pm.filterExpand(vtx, sm=31)
                for v in vtx:
                    vtxDict[v].append([fNormal, fArea])

        if vtxDict:
            for k, v in vtxDict.items():
                if len(v) <= 1:
                    pm.polyNormalPerVertex(k, xyz=v[0][0])
                else:
                    a = 0
                    b = 0
                    for i in v:
                        a += i[0]*i[1]
                        b += i[1]
                    normal = a/b
                    pm.polyNormalPerVertex(k, xyz=normal)

        pm.select(selList)
    else:
        pm.warning("Please Select Face")


def specialVFs(sel_face, normal, *args):
    """
    A growing selection of Vertex Face by a found soft edge
    """
    vtxs = pm.polyListComponentConversion(sel_face, tv=True)
    vfs = pm.polyListComponentConversion(vtxs, tvf=True)
    vfs = pm.filterExpand(vfs, sm=70)
    edges = pm.polyListComponentConversion(sel_face, te=True)
    edges = pm.filterExpand(edges, sm=32)
    print edges
    smoothEdges = []
    for e in edges:
        if pm.MeshEdge(e).isSmooth():
            smoothEdges.append(e)

    if smoothEdges:
        print smoothEdges
        growFace = pm.polyListComponentConversion(smoothEdges, tf=True)
        growVfs = pm.polyListComponentConversion(growFace, tvf=True)
        growVfs = pm.filterExpand(growVfs, sm=70)

        interVfs = [i for i in vfs if i in growVfs]

        pm.polyNormalPerVertex(interVfs, xyz=normal)
        pm.polySoftEdge(smoothEdges, a=180)
        # pm.select(smoothEdges)
    else:
        print "b"
        interVfs = pm.polyListComponentConversion(sel_face, tvf=True)
        pm.polyNormalPerVertex(interVfs, xyz=normal)


def splitEdge(sel_face, *args):
    edges = pm.polyListComponentConversion(sel_face, te=True)
    edges = pm.filterExpand(edges, sm=32)
    smoothEdges = []
    hardEdges = []
    for e in edges:
        if pm.MeshEdge(e).isSmooth():
            smoothEdges.append(e)
        else:
            hardEdges.append(e)
    return smoothEdges, hardEdges

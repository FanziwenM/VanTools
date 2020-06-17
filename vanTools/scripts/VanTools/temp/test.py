import pymel.core as pm
import collections


def main():
    selList = pm.ls(sl=True, fl=True)

    vtxDict = collections.defaultdict(list)

    if isinstance(selList[0], pm.MeshFace):
        for f in selList:
            fArea = f.getArea()
            fNormal = f.getNormal()
            vtx = pm.polyListComponentConversion(f, tv=True)
            vtx = pm.filterExpand(vtx, sm=31)
            for v in vtx:
                vtxDict[v].append([fNormal, fArea])

        print(vtxDict)
        for k,v in vtxDict.items():
            if len(v)<=1:
                pm.polyNormalPerVertex(k, xyz=v[0][0])
            else:
                a = 0
                b = 0
                for i in v:
                    a += i[0]*i[1]
                    b += i[1]
                normal = a/b
                pm.polyNormalPerVertex(k, xyz=normal)

    else:
        pm.warning("Please Select Face")

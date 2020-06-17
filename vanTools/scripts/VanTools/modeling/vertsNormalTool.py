# Author: fanziwen (120416678@qq.com)
# Created: 09/26/2019
# Updated: 10/12/2019
# Last change:
#    - add new function: set vertex normal to align to face
#    - add flatten function
#    - add Smart Unlock Normal
#    - if selected face or edge can convert to vertices then get/set normal
import pymel.core as pm


class VertsNormalUI():

    def __init__(self, *args, **kwargs):
        '''
        Create a initialize tools windows
        '''
        winWidth = 241
        # main window
        with pm.window(
            title="VanNormalTools", sizeable=False,
            toolbox=True, w=winWidth
        ) as self.win:
            # Main Layout
            # with pm.formLayout() as mainForm:
            with pm.columnLayout() as mainColumn:
                # General Layout, Most commonly used controls
                with pm.frameLayout(label="General:") as _:
                    pass
                with pm.formLayout() as generalForm:
                    with pm.frameLayout(label=" ", h=5) as tempFrame:
                        pass
                    # the dispaly normal button
                    dispalyBtn = pm.iconTextButton(
                        st='iconAndTextVertical',
                        i1='vanToolsIcons/vertsNormal.png',
                        label='Dispaly Toggle', h=50,
                        c=self.toggle
                    )
                    # the normal size controls,
                    # including text and float field
                    # which use to set the normal size
                    with pm.columnLayout(ca=2, h=50, rs=5) as subColumn:
                        pm.text("Normal Szie:")
                        self.normalSizeFd = pm.floatField(
                            w=125, v=0.4, ec=self.setNormalSize)
                    # The two most commonly used Normal control buttons
                    with pm.rowLayout(nc=2) as subRow:
                        _ = pm.iconTextButton(
                            style="iconAndTextHorizontal",
                            label="Lock Normal",
                            image="polyNormalLock.png", h=40,
                            c=self.lockNormal
                            )

                        _ = pm.iconTextButton(
                            style="iconAndTextHorizontal",
                            label="Unlock Normal",
                            image="polyNormalUnlock.png", h=40,
                            c=self.unlockNormal
                            )
                    with pm.frameLayout(label=" ", h=5) as tempFrame2:
                        pass
                    smUnLockBt = pm.iconTextButton(
                        style="iconAndTextHorizontal",
                        label="Smart Unlock Normal",
                        image="vanToolsIcons/unlockNormal.png", h=40,
                        c=self.smartUnlockNormal
                        )
                    setNormalAlign2FBt = pm.iconTextButton(
                        style="iconAndTextHorizontal",
                        label="Set Vertex Normal Align Face",
                        image="vanToolsIcons/setNormalAlignFace.png", h=40,
                        c=self.normalAlignFace
                        )

                # General Layout setting
                pm.formLayout(
                    # bgc=(0.5,0.5,1),
                    generalForm, e=True, w=winWidth-6, h=200,
                    af=[
                        (dispalyBtn, "left", 5),    (subColumn, "right", 5),
                        (tempFrame, "left", 1),     (tempFrame, "right", 1),
                        (tempFrame2, "left", 1),    (tempFrame2, "right", 1),
                        (subRow, "left", 5),        (subRow, "right", 5),
                        (smUnLockBt, "left", 30),
                        (setNormalAlign2FBt, "left", 30),
                    ],
                    ac=[
                        (subColumn, "left", 5, dispalyBtn),
                        (tempFrame, "top", 5, dispalyBtn),
                        (subRow, "top", 5, tempFrame),
                        (tempFrame2, "top", 1, subRow),
                        (smUnLockBt, "top", 5, tempFrame2),
                        (setNormalAlign2FBt, "top", 2, smUnLockBt),
                    ])
# ----------------------General Layout Setting End-------------------------#

                # Quick Set Layout
                with pm.frameLayout(label='Quick Set:') as _:
                    pass
                with pm.formLayout() as quickSetForm:
                    with pm.rowLayout(nc=3) as row1:
                        pm.button("+X", w=77, h=30, bgc=(0.28, 0.66, 0.71),
                                  c=self.qkSetX)
                        pm.button("+Y", w=77, h=30, bgc=(0.28, 0.66, 0.71),
                                  c=self.qkSetY)
                        pm.button("+Z", w=77, h=30, bgc=(0.28, 0.66, 0.71),
                                  c=self.qkSetZ)
                    with pm.rowLayout(nc=3) as row2:
                        pm.button("-X", w=77, h=30, bgc=(0.28, 0.66, 0.71),
                                  c=self.qkSetNegX)
                        pm.button("-Y", w=77, h=30, bgc=(0.28, 0.66, 0.71),
                                  c=self.qkSetNegY)
                        pm.button("-Z", w=77, h=30, bgc=(0.28, 0.66, 0.71),
                                  c=self.qkSetNegZ)
                    with pm.rowLayout(nc=3) as row3:
                        pm.button("Flatten X", w=77, h=30,
                                  c=self.flattenX)
                        pm.button("Flatten Y", w=77, h=30,
                                  c=self.flattenY)
                        pm.button("Flatten Z", w=77, h=30,
                                  c=self.flattenZ)
                # Quick Set Setting
                pm.formLayout(
                    quickSetForm, e=True, w=winWidth-6,
                    af=[
                        (row1, "left", 1),        (row1, "right", 1),
                        (row2, "left", 1),        (row2, "right", 1),
                        (row3, "left", 1),        (row3, "right", 1),
                        (row3, "bottom", 1),
                    ],
                    ac=[
                        (row2, "top", 1, row1),
                        (row3, "top", 1, row2),
                    ])
# --------------------------- Quick Set Setting end ------------------------ #

                # Manual Set Layout
                with pm.frameLayout(label="Manual Set: ") as _:
                    pass
                with pm.columnLayout(adj=True) as manualColumn:
                    self.manualGetBtn = pm.button(
                        label="Get Normal", c=self.getVertsNormal)
                    self.normalField = pm.floatFieldGrp(
                        nf=3, cw3=(73, 73, 73), precision=2)
                    self.manualSetBtn = pm.button(
                        label="Set Normal", h=40,
                        bgc=(0.28, 0.66, 0.71),
                        c=self.setVertsNormal
                    )
                # Layout setting
                pm.columnLayout(
                    manualColumn, e=True, w=winWidth-6,  # bgc=(0,0.5,0),
                    rs=5, co=("both", 5),
                )
# ---------------------------Manual Set Layout End----------------------------#

                # Transform Normal Layout
                with pm.frameLayout(label="Transfer Normal:") as _:
                    pass
                with pm.formLayout() as transLayout:
                    self.getObjBtn = pm.button(
                        label="GetMesh", h=30, c=self.getMesh)
                    self.meshName = pm.textField(
                        placeholderText="Null", editable=False, h=25)
                    self.transNormalBtn = pm.button(
                        "Transfer Normal", h=40, bgc=(0.28, 0.66, 0.71),
                        c=self.setNormal)
                # Layout Setting
                pm.formLayout(
                    transLayout, e=True,  # bgc=(0.5,0.5,0),
                    af=[
                        (self.getObjBtn, "top",
                         5),             (self.meshName, "top", 8),
                        (self.getObjBtn, "left",
                         5),            (self.meshName, "right", 5),
                        (self.transNormalBtn, "left",
                         5),        (self.transNormalBtn, "right", 5),
                        (self.transNormalBtn, "bottom", 5),
                    ],
                    ac=[
                        (self.meshName, "left", 5, self.getObjBtn),
                        (self.transNormalBtn, "top", 5, self.getObjBtn),
                    ]
                )
            # Main Layout
            pm.columnLayout(
                mainColumn, e=True,
                adj=True, rs=3,
            )

# --------------------- Main Layout end -----------------------------------#
        pm.showWindow(self.win)

    def toggle(self, *args):
        '''
        toggle the vertexes normal display
        '''
        if pm.ls(sl=True):
            newSize = pm.floatField(self.normalSizeFd, q=True, v=True)
            tg = pm.polyOptions(q=True, dn=True)[0]
            pm.polyOptions(dn=not tg, pt=True, sn=newSize)
        else:
            pm.warning("Not Obj Selected!")

    def setNormalSize(self, *args):
        '''
        set the normal size
        '''
        newSize = pm.floatField(self.normalSizeFd, q=True, v=True)
        print(newSize)
        pm.polyOptions(sn=newSize)

    def getVertsNormal(self, *args):
        '''
        get vertexes Normal,
        the value will be saved in floatFieldGrp(self.normalField)
        update:
            - 10/12/2019: add Get face normal
        '''
        selList = pm.ls(sl=True)
        if selList:
            if isinstance(selList[0], pm.MeshVertex) or isinstance(selList[0], pm.MeshVertexFace):
                selVerts = selList
                normal = pm.polyNormalPerVertex(
                    selVerts[0], q=True, xyz=True)  # selVerts[0].getNormal()
                pm.floatFieldGrp(self.normalField, e=True,
                                 v1=normal[0], v2=normal[1], v3=normal[2])

            elif isinstance(selList[0], pm.MeshFace):
                selFace = selList
                normal = self.getFaceNormal(selFace[0])
                pm.floatFieldGrp(self.normalField, e=True,
                                 v1=normal[0], v2=normal[1], v3=normal[2])
            else:
                pm.warning("Please select Vertex or Face!")

        else:
            pm.warning("Nothing selected!")

    def setVertsNormal(self, *args):
        '''
        if the 'floatFieldGrp(self.normalField)' has normal value,
        pick the value set to selected vertexes normal
        update:
            #10/12/2019:
            if selected type is MeshFace also can set Normal(Face convert to Vertices)
        '''
        selList = pm.ls(sl=True)
        if selList:
            normal = pm.floatFieldGrp(self.normalField, q=True, v=True)
            if isinstance(selList[0], pm.MeshVertex)or isinstance(selList[0], pm.MeshVertexFace):
                for s in selList:
                    pm.polyNormalPerVertex(xyz=normal)
            else:
                vtxList = pm.polyListComponentConversion(selList, tv=True)
                vtxList = pm.filterExpand(vtxList, sm=31)
                pm.polyNormalPerVertex(vtxList, xyz=normal)
        else:
            pm.warning("Nothing selected!")

    def getMesh(self, *args):
        '''
        get the Name from the selected Object,
        and save the name in the 'pm.textField(self.meshName)'
        '''
        selList = pm.ls(sl=True)
        if selList:
            self.meshName.setText(selList[0])
        else:
            pm.warning("Not Object selected!")

    def setNormal(self, *args):
        '''
        if the ' pm.textField(self.meshName) ' is define,
        setting selected mesh normal from the defined name
        '''
        sourceName = self.meshName.getText()

        if sourceName:
            print(sourceName)
            selList = pm.ls(sl=True)
            for s in selList:
                '''
        transferAttributes()
            - sampleSpace : spa              (int)           [create,edit]
                Selects which space the attribute transfer is performed in.
                0 is world space,
                1 is model space,
                4 is component-based,
                5 is topology-based.
                The default is world space.
                '''
                pm.transferAttributes(sourceName, s, transferNormals=1)
                pm.delete(s, ch=True)
        else:
            pm.warning("Please get Normal first")

    def flatten(self, axis, *args):
        '''
        clear the value which specific axis
        '''
        selList = pm.ls(sl=True, fl=True)
        if isinstance(selList[0], pm.MeshVertex) or isinstance(selList[0], pm.MeshVertexFace):
            for s in selList:
                n = pm.polyNormalPerVertex(s, q=True, xyz=True)
                if axis == "x":
                    pm.polyNormalPerVertex(s, xyz=[0, n[1], n[2]])
                if axis == "y":
                    pm.polyNormalPerVertex(s, xyz=[n[0], 0, n[2]])
                if axis == "z":
                    pm.polyNormalPerVertex(s, xyz=[n[0], n[1], 0])
        else:
            selList = pm.polyListComponentConversion(selList, tv=True)
            selList = pm.filterExpand(selList, sm=31)
            print(selList)
            for s in selList:
                n = pm.polyNormalPerVertex(s, q=True, xyz=True)
                if axis == "x":
                    pm.polyNormalPerVertex(s, xyz=[0, n[1], n[2]])
                if axis == "y":
                    pm.polyNormalPerVertex(s, xyz=[n[0], 0, n[2]])
                if axis == "z":
                    pm.polyNormalPerVertex(s, xyz=[n[0], n[1], 0])

    def flattenX(self, *args):
        self.flatten("x")

    def flattenY(self, *args):
        self.flatten("y")

    def flattenZ(self, *args):
        self.flatten("z")

    def qkSetNormal(self, axis, *args):
        '''
        The function be used to the series of QuickSet button
        '''
        selList = pm.ls(sl=True, fl=True)
        axisDic = {
            "+x": [1, 0, 0], "-x": [-1, 0, 0],
            "+y": [0, 1, 0], "-y": [0, -1, 0],
            "+z": [0, 0, 1], "-z": [0, 0, -1],
        }
        if selList:
            try:
                pm.polyNormalPerVertex(xyz=axisDic[axis])
            except Exception:
                vtxList = pm.polyListComponentConversion(selList, tv=True)
                pm.polyNormalPerVertex(vtxList, xyz=axisDic[axis])
        else:
            pm.warning("Nothing selected!")

    def qkSetX(self, *args):
        self.qkSetNormal("+x")

    def qkSetY(self, *args):
        self.qkSetNormal("+y")

    def qkSetZ(self, *args):
        self.qkSetNormal("+z")

    def qkSetNegX(self, *args):
        self.qkSetNormal("-x")

    def qkSetNegY(self, *args):
        self.qkSetNormal("-y")

    def qkSetNegZ(self, *args):
        self.qkSetNormal("-z")

    def smartUnlockNormal(self, *args):
        '''
        Smart unlock normal with smooth/hard edgs
        '''
        from VanTools.modeling.smartUnlockNormal import VanMesh

        for s in pm.ls(sl=True):
            a = VanMesh(s)
            a.smartUnlockNormal()

    def getFaceNormal(self, face, *args):
        '''
        return face normal;
        return type (float, float, float)
        '''
        import re
        fNstr = pm.polyInfo(face, fn=True)[0]
        # print(fNstr)
        a = re.findall("([+|-]?[0-9]+.[0-9]+)", fNstr.split(":")[1])
        # a = fNstr.split(":")[1]
        # a = a.split("\n")[0]
        # a = a.split(" ")
        # a.pop(0)
        return map(float, a)

    def unlockNormal(self, *args):
        selList = pm.ls(sl=True, fl=True)
        if selList:
            if isinstance(selList[0], pm.MeshVertex)or isinstance(selList[0], pm.MeshVertexFace):
                for s in selList:
                    pm.polyNormalPerVertex(ufn=True)
            else:
                vtxList = pm.polyListComponentConversion(selList, tv=True)
                pm.polyNormalPerVertex(vtxList, ufn=True)

        else:
            pm.warning("Nothing selected!")

    def lockNormal(self, *args):
        selList = pm.ls(sl=True, fl=True)
        if selList:
            if isinstance(selList[0], pm.MeshVertex)or isinstance(selList[0], pm.MeshVertexFace):
                for s in selList:
                    pm.polyNormalPerVertex(fn=True)
            else:
                vtxList = pm.polyListComponentConversion(selList, tv=True)
                pm.polyNormalPerVertex(vtxList, fn=True)

        else:
            pm.warning("Nothing selected!")

    def normalAlignFace(self, *args):
        import collections
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
        else:
            pm.warning("Please Select Face")

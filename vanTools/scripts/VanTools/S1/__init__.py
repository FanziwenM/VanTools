import pymel.core as pm
# from functools import partial


def main():
    ww = 150
    hh = 200

    try:
        pm.deleteUI("s1win134")
    except Exception:
        pass

    with pm.window(
        "s1win134", t="S1 ToolKit", toolbox=True, sizeable=False
    ) as s1Win:
        with pm.columnLayout() as _:
            with pm.frameLayout(
                label="Character Creator:", w=ww,
                bgc=(0.30, 0.30, 0.30)
            ) as _:

                pm.button(
                    "Import Material",
                    c=importMatCmd,
                    bgc=(0.345, 0.647, 0.8)
                )
                pm.iconTextButton(
                    "charCreatorBtn",
                    style='iconAndTextVertical',
                    image1="cube.png", label="Character Creator", w=ww,
                    ann="Please Import Material firest",
                    enable=True,
                    command=charCreatorCmd
                )
            with pm.frameLayout(
                label="AO Tool:", w=ww,
                bgc=(0.30, 0.30, 0.30)
            ) as _:

                pm.iconTextButton(
                    "occChar",
                    style='iconAndTextVertical',
                    image1="cube.png", label="AO for Character", w=ww,
                    ann="Please Import Material firest",
                    enable=True,
                    command=occCharCmd
                )
        pm.window(
            s1Win, e=True,
            w=ww, h=hh
        )

    checkMatLoaded()
    pm.showWindow(s1Win)


def importMatCmd(*args):
    from VanTools.S1 import createMat
    reload(createMat)
    createMat.main()
    pm.iconTextButton("charCreatorBtn", e=True, enable=True)


def charCreatorCmd(*args):
    from VanTools.S1 import charCreator
    reload(charCreator)
    charCreator.main()
    pm.deleteUI("s1win134")


def checkMatLoaded(*args):
    shaderGrpList = ["faceSG", "hairSG", "eyesSG"]
    for sg in shaderGrpList:
        if not pm.objExists("%s" % sg):
            pm.iconTextButton("charCreatorBtn", e=True, enable=False)


def occCharCmd(*args):
    from VanTools.S1 import occTool
    reload(occTool)
    occTool.main()

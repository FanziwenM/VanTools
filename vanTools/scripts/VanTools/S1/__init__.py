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
                    bgc=(0.28, 0.66, 0.71)
                )
                pm.iconTextButton(
                    "charCreatorBtn",
                    style='iconAndTextVertical',
                    image1="cube.png", label="Character Creator",
                    ann="Please Import Material firest",
                    enable=True,
                    command=charCreatorCmd
                )
            with pm.frameLayout(label="AO Tool:", w=ww, bgc=(0.30, 0.30, 0.30)) as _:
                with pm.rowLayout(columnAttach=[(1, "both", 2)]) as _:
                    pm.checkBox("charOccCheckBox", label="Use Cage", w=ww)
                pm.iconTextButton(
                    "occChar",
                    style='iconAndTextVertical',
                    image1="vanToolsIcons/occForChar.png", label="AO for Character", w=ww,
                    ann="Please Import Material firest",
                    enable=True,
                    command=occCharCmd
                )
                with pm.columnLayout(
                    numberOfChildren=2,
                    columnAttach=("both", 4)
                ) as _:
                    pm.button("aoToggle", label="AO Toggle", c=lambda args: aoToggleCmd(), w=ww-10)
                    selHilight = pm.modelEditor("modelPanel4", q=True, selectionHiliteDisplay=True)
                    pm.checkBox(
                        "selHighlightToggle",
                        label=" Selection Highlight",
                        value=selHilight,
                        w=ww-10,
                        changeCommand=lambda args: selToogleCmd()
                    )
                    # setting

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


def aoToggleCmd(*args):
    '''
    Toggles display of vertex colors
    '''
    selList = pm.ls(sl=True)
    if selList:
        toggle = pm.polyOptions(selList, q=True, colorShadedDisplay=True)
        if any(toggle):
            pm.polyOptions(selList, colorShadedDisplay=False)
        else:
            pm.polyOptions(selList, colorShadedDisplay=True)
    else:
        pm.warning("Nothing Selected!")


def selToogleCmd(*args):

    selHilight = pm.checkBox("selHighlightToggle", q=True, v=True)
    # activeView = pm.getPanel(withFocus=True)
    if selHilight:
        pm.modelEditor("modelPanel4", e=True, selectionHiliteDisplay=True)
    else:
        pm.modelEditor("modelPanel4", e=True, selectionHiliteDisplay=False)

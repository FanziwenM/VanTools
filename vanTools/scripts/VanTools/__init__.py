import os
import json
import pymel.core as pm
import maya.mel as mel


def main():

    # mel.eval('shelfTabLayout -e -selectTab "Van" ShelfLayout')

    # Set the execution path
    vanToolsPath = os.path.abspath(__file__)
    os.chdir(os.path.dirname(vanToolsPath))

    # load config file
    with open("config.json", "r") as f:
        data = json.load(f)

    version = data["Version"]
    pathFile = data["PathFile"]
    remoteConfig = data["RemoteConfig"]
    prefFile = data["MayaPref"]

    # Get shelf button list
    shelfVan = pm.shelfLayout("Van", q=True, ca=True)
    print('Initializing'.center(50, '-'))
    print("VanTools Version:{}".format(version))

    # Load Remote config file
    try:
        with open(remoteConfig, "r") as f:
            dataRemote = json.load(f)
        newVersion = dataRemote["Version"]
        print("Remote Version:{}".format(newVersion))
    except Exception:
        print("No Found Remote Version!")
        newVersion = data["Version"]

    # Check if the HoudiniEngine is loaded
    if pm.pluginInfo("houdiniEngine", q=True, loaded=True):
        print("HoudiniEngine has been Loaded")
    else:
        try:
            pm.loadPlugin("houdiniEngine.mll")
            print("HoudiniEngine Load successfully")
        except Exception as e:
            pm.warning(e)

    checkFile(pathFile, prefFile)

    checkIcons(shelfVan, version, newVersion)

    print('Done'.center(50, '-'))

# ----------------------------------------------------------------- #


def checkFile(path_file, pref_file):

    if not os.path.exists(path_file):
        try:
            os.makedirs(os.path.dirname(path_file))
        except Exception:
            pass
        with open(path_file, "w") as f:
            json.dump({"tempPath": "D:\\"}, f, indent=4, sort_keys=True)
        print("Check files Done")

    if not os.path.exists(pref_file):
        try:
            os.makedirs(os.path.dirname(pref_file))
        except Exception:
            pass
        with open(pref_file, "w") as f:
            json.dump(
                {
                    "centerExport": False,
                    "sampleSpace": "ss0",
                }, f, indent=4, sort_keys=True
            )
        print("Check files Done")


def checkIcons(shelfVan, version, newVersion):

    # Check unit
    unit = pm.currentUnit(q=True)
    print(unit)
    if unit != "cm":
        mel.eval(
            'shelfButton -e -image \
                "vanToolsIcons/unitM.png" {}'.format(shelfVan[3]))
    else:
        mel.eval(
            'shelfButton -e -image \
                "vanToolsIcons/unitCm.png" {}'.format(shelfVan[3])
        )
    # ------------------------------------------

    # Check Version
    mel.eval(
        'shelfButton -e -imageOverlayLabel \
            "{}" {};'.format(version, shelfVan[0]))
    if version != newVersion:
        mel.eval(
            'shelfButton -e -image \
                "vanToolsIcons/newVersion.png" {}'.format(shelfVan[0])
        )
    else:
        mel.eval(
            'shelfButton -e -image \
                "vanToolsIcons/versionInfo.png" {}'.format(shelfVan[0])
        )
    # -------------------------------------------

    # Disable Quick export
    mel.eval('shelfButton  -e -enable false {}'.format(shelfVan[2]))

    # Disable Houdini Asset
    if not pm.pluginInfo("houdiniEngine", q=True, loaded=True):
        mel.eval('shelfButton  -e -enable false {}'.format(shelfVan[24]))
    else:
        mel.eval('shelfButton  -e -enable true {}'.format(shelfVan[24]))

    # -------------------------------------------

    print("Check Icons Done")


main()

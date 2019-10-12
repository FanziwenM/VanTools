import json,os
import maya.mel as mel



def checkFile(file):
    global data

    if os.path.exists(file):
        with open(file,"r") as f:
            data = json.loads(f.read())

    else:
        try:
            os.makedirs(os.path.dirname(file))
        except:
            pass
        with open(file,"w") as f: 
            json.dump({"tempPath":"D:\\"}, f, indent=4, sort_keys=True)

def searchPath(maya_name,path_file):
    global data
    with open(path_file,"r") as f:
        data = json.loads(f.read())

    if maya_name in data:
        exportPath = data[maya_name]
    else:
        exportPath = data["tempPath"]

    return exportPath



def switchImage(button_index, image1, image2):
    # use mel to change the image
    melCommond = """
$image = `shelfButton -q -image shelfButton{a}`;
if ($image == "{b}")
shelfButton -e -image "{c}" shelfButton{a};
else
shelfButton -e -image "{b}" shelfButton{a};
""".format(a = button_index, b = image1, c = image2)
    mel.eval(melCommond)


def disableButton():
    print("shelfButton  -e -enable false shelfButton1")

def updateLabel():
    mel.eval('"shelfButton -e -imageOverlayLabel "1.2.2" shelfButton1;"')
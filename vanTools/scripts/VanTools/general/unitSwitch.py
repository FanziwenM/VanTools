#Author: Fanziwen (120416678@qq.com)
#Created: 09/10/2019


import pymel.core as pm
import maya.mel as mel


def main():
    unit = pm.currentUnit(q=True)
    shelfVan = pm.shelfLayout("Van",q=True,ca=True)

    if unit == "m":
        unit = pm.currentUnit(linear="centimeter")
        mel.eval('shelfButton -e -image "vanToolsIcons/unitCm.png" {}'.format(shelfVan[3]))
        message = "Centimeter"
    else:
        unit = pm.currentUnit(linear="meter")
        mel.eval('shelfButton -e -image "vanToolsIcons/unitM.png" {}'.format(shelfVan[3]))
        message = "Meter"

    pm.inViewMessage(amg='Unit: <font color="#48AAB5">{}</font>'.format(message), pos='topCenter', fade=True )
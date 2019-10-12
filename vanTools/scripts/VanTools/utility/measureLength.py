#Author: Fanziwen (120416678@qq.com)
#Created: 09/20/2019
#Updated: 09/24/2019
#Last Change: add a unit in the suffix

import pymel.core as pm

def main():
    selectionList = pm.ls(sl=True, fl=True )
    unit = pm.currentUnit(q=True)
    sumLength = 0
    for s in selectionList:
        sumLength += s.getLength()

    print(sumLength)

    pm.inViewMessage( amg='Total Length: <font color="#48AAB5">{:.2f}</font> {}'.format(sumLength,unit), pos='topCenter', fade=True )
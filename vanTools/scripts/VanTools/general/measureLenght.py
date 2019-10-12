import pymel.core as pm

selectionList = pm.ls(sl=True, fl=True )
unit = pm.currentUnit(q=True)
sumLength = 0
for s in selectionList:
    sumLength += s.getLength()

print(sumLength)

pm.inViewMessage( amg='Total Length: <font color="#48AAB5">{:.2f}</font> {}'.format(sumLength,unit), pos='topCenter', fade=True )
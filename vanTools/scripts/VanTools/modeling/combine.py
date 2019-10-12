#Author: Fanziwen (120416678@qq.com)
#Created: 08/11/2019

import pymel.core as pm

def main():
	selectionList = pm.ls(sl=True)

	if selectionList:
		pm.mel.deleteUnusedDeformers()
		newName = selectionList[-1]
		parents = newName.getParent()
		pm.polyUnite(selectionList, n="combine")
		pm.parent("combine",parents)
		pm.delete(ch=True)
		pm.rename("combine",newName)
		pm.xform(cp=True)

	else:
		pm.confirmDialog(title="error",message="No objects be selected")
		return



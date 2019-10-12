#Author: Fanziwen (120416678@qq.com)
#Created: 08/11/2019

import pymel.core as pm

def main():
	selectionList = pm.ls(sl=True)
	for s in selectionList:
		mesh = s.getShape()
		originalName = str(s)
		parents = s.getParent()
		separated = pm.polySeparate(s, ch=0)
		pm.parent(separated,parents)
		pm.delete(originalName)

		separtedIndx = 0
		for parts in separated:
			pm.parent(parts,parents)
			pm.delete(ch=True)
			if  separtedIndx==0:
				pm.rename(parts, originalName)
				pm.xform(cp=True)

			else:
				originalName2 = originalName + "_" + str(separtedIndx)
				pm.rename(parts, originalName2 )
				pm.xform(cp=True)

			separtedIndx +=1



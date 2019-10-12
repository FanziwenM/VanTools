import pymel.core as pm


mainpos=pm.window('MayaWindow', query=True, topLeftCorner=True)

wh=pm.window('MayaWindow', query=True, wh=True)

pos = [mainpos[0] + wh[1]/2, mainpos[1] + wh[0]/2]


a = pm.window(title = "aaa")

wh2 = pm.window(a, query=True, wh=True)

pos = [pos[0]-wh2[1]/2, pos[1] - wh2[0]/2]

pm.window(a, e=True, topLeftCorner = pos)

pm.showWindow(a)
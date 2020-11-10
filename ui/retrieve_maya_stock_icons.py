import maya.cmds as cmds

for item in cmds.resourceManager(nameFilter="*.tiff"):
    print (item)

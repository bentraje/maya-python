### General
* Maya comes in three main Python implemantation
  * maya.cmds
  * pymel
  * OpenMaya
* Some weird instance where you need to slice the list.
* A script has a purpose, procedure and presumption
* Variables in Python: No need to add $
* Unlike in C4D where you have to put a docObject command, in Maya, you only have to put quotation marks “” and this means it is already #. search for that specific object.
* Unlike in joints, if you are modifiying the objects you have to specifiy the shape node which is object[0] node.
* Every command has a parenthesis such as polyCube(). You can also define a custom command consist of several commands such as procedure (local or global in MEL)
* Unlike MEL, command value in Python is not enclosed in a quotation marks “”
* Python requires that the declaration of a global variable remains separate from any commands that set the value of the variable.
* Python implements them slightly differently than most other languages in which they always iterate over a list of some kind. This means that if we want to do something X times, we have to have a list of X items. For this, we’ll want the built-in range() function
* Using global variables is one way to allow the different parts of your script communicate with eachother, but there’s a better way. Instead of using globals, you can organize your script using custom class.
* Creating a class for your script will not only allow you to easily access UI elements from various functions, but it will also make it easy to neatly contain other kinds of data, useful in more advanced scripts.
* Non key term then the key term. mc.parent(rnm_grp, w=true)
* RE: constraint. In python, the affected object are shown first while in MEL it is last.
* The str and int type will not concatenate by simply using “+”. You need a %. (thisNum = 5) Print “%d is the value of thisNum” % thisNum %f for the float. + that
* In 3DBuzz’s “Developing Modular Rigging Systems with Python”, the process of creating a mirror behaviour while moving controls on either of two sides of a mirror plane is described in detail. In case you need that extra kick in the right direction
* building maya interfaces with python
https://www.highend3d.com/maya/script/automated-animator-friendly-rigging-for-maya
http://chrislesage.com/python/maya-python-reset-selected-controls/
https://www.riggingdojo.com/quadruped-friendly-rigging/
https://ondemand.riggingdojo.com/store/j6JcX8T4
https://github.com/cgwire/awesome-cg-vfx-pipeline
http://www.chadvernon.com/blog/unit-testing-in-maya/
https://pyblish.com/
list all skinclusters. 
Create Proxy Skeleton http://kylemr.blogspot.com/2012/07/stick-fork-in-it.html 
Adjust Positioning Locators Built Skeleton Build Rig Control Curve Creator Character Rigger: -creates animation control rigs -creates animation pipeline toolsets -skin weights character models -set up character assets in game 
Pose and animation libraries. In production it is paramount for the rigs to be compatible with standard pose and animation library scripts like Kurt Rathjen’s Studio Library, Lionel Gallat’s PoseLib, or the very user friendly Sal Pose Manager by Salwan Badra for 3dsmax. 
Duplicate each target for a separate mesh of a blendShape (https://forums.cgsociety.org/t/get-the-name-of-each-blend-shape-mel/1544833/2)
Python http://discourse.techart.online/t/maya-retrieve-blendshape-name/9668/4
https://forums.cgsociety.org/t/transfer-skin-between-2-joints/2047527/7 
https://forums.cgsociety.org/t/mel-maya-ui-building/664014
http://www.manoanim.com/autodesk-maya-tutorials/maya-python-tutorial-101-script-an-ik-handle/


```python
from maya import cmds
geometry = cmds.ls(geometry=True)
transforms = cmds.listRelatives(geometry, p=True, path=True)
cmds.select(transforms, r=True)

# Store current selection
obj_list = cmds.ls(sl=True)

# Select object by name
obj = ['pSphere1']
obj_list = ['pSphere1', 'pCube1', 'pSphere2']

# Select all objects by type
all_meshes = cmds.ls(type="mesh")
all_joint = cmds.ls(type="joint")

# Select by Volume/Container Geo
# http://www.ericspevacek.com/blog/maya-python-select-by-volume/
```

```python
# Random 
Detect if the transform is from a mesh or a ligth in Maya.
cmds.objectType(cmds.listRelatives( 'directionalLight1'))

mc.select (toggle=true) is like having a shift+LMB selection

Toggle between World/Local Pivot. See python script (https://forums.autodesk.com/t5/maya-lt-forum/world-object-swap-axis-orientation-hotkey/td-p/6603226)

```

```python
# Rendering in the Commandline
Add a system variable to the Maya/Bin directory
Render.exe

render -r mr -s 1 -e 5 -b 1 -rd images/creeper scenes/creeper3.mb
render -help -r sw

mr means mental ray 
-b 1 means render everyframe 
-rd means render directory
```

```python 
# Materials
# Store all file names
allFiles = [cmds.getAttr("%s.fileTextureName"%file) for file in cmds.ls(type="file")]

# Store all file names with jpg extension
fileFilter = ".png"
typedFiles = [cmds.getAttr("%s.fileTextureName"%file) for file in cmds.ls(type="file") if fileFilter in cmds.getAttr("%s.fileTextureName"%file)]

# Select objects from a shading group
cmds.select(cmds.sets("initialShadingGroup", q=True))

# Select objects from a material 
materialName = "lambert1"
shadingGroup = cmds.listConnections(materialName, type="shadingEngine")
print shadingGroup
componentsWithMaterial = cmds.sets(shadingGroup, q=True)
cmds.select(componentsWithMaterial)

# List of all materials 
material_list = cmds.ls(type='shadingEngine')

# This is a UI Command. You can have a look at “hyperShadePanel.mel” to see what going on exactly. Otherwise you can just wrap the MEL command into Python

mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')

// mel
MLdeleteUnused;

python
import maya.mel as mel
mel.eval(‘MLdeleteUnused;’)


#You can use the same hyperShade command that the “Select Materials From Objects” uses. This example also filters out shaders that are not surface shaders, so it won’t return displacement shaders for example

pm.hyperShade(shaderNetworksSelectMaterialNodes=True)
for shd in pm.selected(materials=True):
    if [c for c in shd.classification() if 'shader/surface' in c]:
        print shd

import maya.cmds as mc
theNodes = mc.ls(sl = True, dag = True, s = True)
shadeEng = mc.listConnections(theNodes , type = “shadingEngine”)
materials = mc.ls(mc.listConnections(shadeEng ), materials = True)


# unfortunately, shaders and objects are not connected so you have to go via the ShadingGroup set.

# Get materials from a selected object
shaders = cmds.listConnections(cmds.listHistory('pCube1',f=1),type='lambert')

# Get material from selection
# get shapes of selection:
shapesInSel =  mc.ls(dag=1,o=1,s=1,sl=1)
# get shading groups from shapes:
shadingGrps = mc.listConnections(shapesInSel,type='shadingEngine')
# get the shaders:
shaders = mc.ls(mc.listConnections(shadingGrps),materials=1)


shading_group= cmds.sets(renderable=True,noSurfaceShader=True,empty=True)
```

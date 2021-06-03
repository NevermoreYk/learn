from pymel.core import *
import maya.cmds as cmds
import mtoa.utils as arnold


#路径换成你常用的hdr路径
hdr_Path = 'E:\\blaubeuren_hillside_4k.exr'



#下面的不用管
hdr_file = cmds.shadingNode("file",asTexture=True, n = "Hdr")
cmds.setAttr('%s.fileTextureName'%hdr_file,'%s'%hdr_Path,type='string')
lig = arnold.createLocator("aiSkyDomeLight",asLight=True)
connectAttr('%s.outColor'%hdr_file,'%s.color'%lig[1])
cmds.setAttr('%s.camera'%lig[1],0)

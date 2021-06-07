from pymel.core import *
import os
import maya.cmds as mc
import json

#定义方法根据选中的节点获取该节点的输入节点
def getNode(inputNode,textures_list):
    node_list =listConnections(inputNode,s=1,d=0)
    for node in node_list:
        
        if nodeType(node)=='file':
            textures_list.append(node)
        else:
            getNode(node,textures_list)
    return textures_list
    
#####资产目录############################
asset_path ='E:/stage/'

#根据选择的模型选中对应的Shape节点
selected = ls(sl=1)
shapes = ls(selected,dag = 1, s = 1)

if shapes == []:
    pass
else:
    for shape in shapes:
        #先选中当前Shape节点
        select(shape)
        #按下向上键选中模型Transfrom节点
        pickWalk(d='up')
        model_name = ls(sl=1)[0]
        #导出obj模型
        mc.file( os.path.join(asset_path,'%s.obj'%model_name),force=1, options= "groups=1;ptgroups=1;materials=0;smoothing=1;normals=1" ,typ="OBJexport" ,pr=1, es=1)
        sgs = listConnections(shape,type = 'shadingEngine')
        allInputNodes=[]
        for sg in sgs:
            allInputNodes.append(listConnections(sg,s=1,d=0,scn=1)[0])
        
        materials = {}
        for inputNode in allInputNodes:
            node_list =listConnections(inputNode,s=1,d=0)

            ########递归找到当前节点网络中连接的所有贴图########
            textures_list=[]
            textures_list=getNode(inputNode,textures_list)
            #################################################
            
            textures_dir={}
            for texture in textures_list:
                textures_path = getAttr(texture + '.fileTextureName')
                file_type = textures_path.split('.')[-2].split('_')[-1]
                textures_dir[file_type]=textures_path
                print(textures_path)
            materials[str(inputNode)]=textures_dir
        print(materials)
        #写入json文件
        with open(os.path.join(asset_path,'%s.json'%model_name),"w") as dump_f:
           json.dump(materials,dump_f)
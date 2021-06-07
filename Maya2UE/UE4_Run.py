import json
import os
import unreal
import sys

###定义模型导入参数
def buildStaticMeshImportOptions():
    options = unreal.FbxImportUI()
    # unreal.FbxImportUI
    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_textures', False)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('import_as_skeletal', False)  # Static Mesh
    # unreal.FbxMeshImportData
    options.static_mesh_import_data.set_editor_property('import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property('import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.static_mesh_import_data.set_editor_property('import_uniform_scale', 1.0)
    # unreal.FbxStaticMeshImportData
    options.static_mesh_import_data.set_editor_property('combine_meshes', True)
    options.static_mesh_import_data.set_editor_property('generate_lightmap_u_vs', True)
    options.static_mesh_import_data.set_editor_property('auto_generate_collision', True)
    return options

###定义模型导入参数
def buildImportTask(filename='', destination_path='', options=None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('destination_path', destination_path)
    task.set_editor_property('filename', filename)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    task.set_editor_property('options', options)
    return task


AssetTools = unreal.AssetToolsHelpers.get_asset_tools()
MaterialEditingLibrary = unreal.MaterialEditingLibrary
EditorAssetLibrary = unreal.EditorAssetLibrary
options = buildStaticMeshImportOptions()

#资产目录
asset_path ='E:/stage/'
#获取目录中所有文件
file_list = os.listdir(asset_path)



#从场景中获取根材质
base_shader = EditorAssetLibrary.find_asset_data('/Game/MSPresets/MS_DefaultMaterial/MS_DefaultMaterial').get_asset()

#从根材质中获取所有贴图参数名称
texture_list = MaterialEditingLibrary.get_texture_parameter_names(base_shader)

#从资产目录中的"texture_name_lib.json"取得贴图名称对应关系
texture_name_lib = {}
with open(os.path.join(asset_path,'texture_name_lib.json'),'r') as load_lib:
    texture_name_lib=json.load(load_lib)

for filepath in file_list:
    if filepath.endswith('.json'):
        file_name = filepath.replace('.json','')
        static_mesh_task = buildImportTask(os.path.join(asset_path,'%s.obj'%file_name), '/Game/Assets',options)
        AssetTools.import_asset_tasks([static_mesh_task])
        static_mesh = EditorAssetLibrary.find_asset_data('/Game/Assets/%s'%file_name).get_asset()
        with open(os.path.join(asset_path,filepath),'r') as load_f:
            load_dict = json.load(load_f)

            #key为材质名称，value为所有的贴图
            for key,value in load_dict.items():
                #根据材质名称创建实例材质
                instanceMat= AssetTools.create_asset(key, "/Game/Assets", unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
                #指定根材质
                MaterialEditingLibrary.set_material_instance_parent(instanceMat, base_shader)
                #为模型设置材质
                static_mesh.set_material(0,instanceMat)
                for subkey,subvalue in value.items():
                    if subkey in texture_name_lib:
                        if texture_name_lib[subkey] in texture_list:
                            file_name = subvalue.split('\\')[-1]
                            texture =''.join(file_name.split('.')[:-1])

                            texture_import_task = buildImportTask(subvalue, '/Game/Assets/Textures')
                            AssetTools.import_asset_tasks([texture_import_task])
                            texture_asset = EditorAssetLibrary.find_asset_data('/Game/Assets/Textures/%s'%texture).get_asset()
                            MaterialEditingLibrary.set_material_instance_texture_parameter_value(instanceMat,texture_name_lib[subkey],texture_asset)

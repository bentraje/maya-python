import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
import json


'''
Sample Dictionary Structure

    "epiglottis": {
        "mat_type": "Standard", 
        "mat_param": {
            "bumpMap": "None", 
            "diffuseMapAmount": "100.0", 
            "ior": "1.5", 
            "bumpMapAmount": "30.0000019073"
        }

'''


tex_path = "D:\\_Specwork\\10_October\\03_rig_female_anatomy_sebastian\\full_female_anatomy_rigged_3ds_max_vray\\"
param_path = "D:/female_vray_materials.json"

def create_file_place2d_node(tex_name, suffix=""):
    tex_path = tex_path
    #tex_name = '\kidneys_tube_CM.bmp'
    tex_file = tex_path + tex_name

    file_node_name = tex_name.split('.')[0]
    place2d_node_name = tex_name.split('.')[0]  + '_2dtexture'

    file_node = cmds.shadingNode('file', asTexture=True, name=file_node_name)
    place2d_node = cmds.shadingNode('place2dTexture', asUtility=True, name =place2d_node_name)

    cmds.setAttr(file_node + '.fileTextureName', tex_file, type="string")

    cmds.connectAttr(place2d_node + '.coverage', file_node + '.coverage')
    cmds.connectAttr(place2d_node + '.outUV', file_node + '.uvCoord')
    cmds.connectAttr(place2d_node + '.outUvFilterSize', file_node + '.uvFilterSize')
    cmds.connectAttr(place2d_node + '.vertexCameraOne', file_node + '.vertexCameraOne')
    cmds.connectAttr(place2d_node + '.vertexUvOne', file_node + '.vertexUvOne')
    cmds.connectAttr(place2d_node + '.vertexUvTwo', file_node + '.vertexUvTwo')
    cmds.connectAttr(place2d_node + '.vertexUvThree', file_node + '.vertexUvThree')
    cmds.connectAttr(place2d_node + '.mirrorU', file_node + '.mirrorU')
    cmds.connectAttr(place2d_node + '.mirrorV', file_node + '.mirrorV')
    cmds.connectAttr(place2d_node + '.noiseUV', file_node + '.noiseUV')
    cmds.connectAttr(place2d_node + '.offset', file_node + '.offset')
    cmds.connectAttr(place2d_node + '.repeatUV', file_node + '.repeatUV')
    cmds.connectAttr(place2d_node + '.rotateFrame', file_node + '.rotateFrame')
    cmds.connectAttr(place2d_node + '.rotateUV', file_node + '.rotateUV')
    cmds.connectAttr(place2d_node + '.stagger', file_node + '.stagger')
    cmds.connectAttr(place2d_node + '.translateFrame', file_node + '.translateFrame')
    cmds.connectAttr(place2d_node + '.wrapU', file_node + '.wrapU')
    cmds.connectAttr(place2d_node + '.wrapV', file_node + '.wrapV')
    
    return file_node
        

mat_extra = {

    "cricoid cartilage": "cricoidFBXASC032cartilage",
    "eye3": "eyelash",
    "glans_ penis_to": "glans_FBXASC032penis_top",
    "hepatic left": "hepaticFBXASC032left",
    "hyoid_bone": "hyoid_bone_ncl1_2",
    "liver ligament": "liverFBXASC032ligament",
    "transverse muscle": "transverseFBXASC032muscle",
    "vascular_system_03": "vascular_blue",
    "vascular_system_02": "vascular_red",

    "calcaneum ": "calcaneumFBXASC032",
    " gallbladder": "FBXASC032gallbladder",
    "ilium": "ilium_ncl1_2",
    "lymphatic_system": "lymphatic_system_ncl1_2",
    "pancreas duct": "pancreasFBXASC032duct",
    "spleen ligament": "spleenFBXASC032ligament",
    "stomach pharynx": "stomachFBXASC032pharynx",
    "thyroid cartilage": "thyroidFBXASC032cartilage",

}


# RETRIEVE VRAY DATA

with open(param_path, "r") as read_file:
    data = json.load(read_file)

    for mat_name, mat_values in data.items():        
               
        
        #if mat_name != 'cartilage_tissue':
        #   continue
           
        #if mat_name == 'cartilage_tissue':
        #   print mat_name

        if cmds.objExists(mat_name) != 1:
            #print mat_name
            dict_mat = mat_extra.get(mat_name, None)    
            if dict_mat == None: 
                dict_mat = 'nandemonai' # What is this?
                      
            if cmds.objExists(dict_mat): # objExists does not accept None. That's why there is a nandemonai. LOL
                mat_name = mat_extra[mat_name]
            else:
                print  "{} does not exist in Maya file".format(mat_name)
                continue      
        
        if maya.cmds.nodeType(mat_name)== 'transform' or maya.cmds.nodeType(mat_name)== 'displayLayer':
            dict_mat = mat_extra.get(mat_name, None)
            print dict_mat
            if dict_mat == None: 
                dict_mat = 'nandemonai'  
  
            if cmds.objExists(mat_name + '_ncl1_1'): # localized adjustment 
                mat_name = mat_name + '_ncl1_1'

            #if cmds.objExists(' gallbladder'): # localized for female
            #    mat_name = 'FBXASC032gallbladder'
                
            elif cmds.objExists(dict_mat):
                mat_name = mat_extra[mat_name]
                
            else:  
                print "{} exist but not as a material".format(mat_name)
                continue
        
        try:
            if maya.cmds.nodeType(mat_name + '_ai') == 'aiStandardSurface':
                print "Skipping {}. Its already an arnold shader".format(mat_name)
                continue 
        except:      
            print "Processing {}".format(mat_name)   
            
       
        for key, value in mat_values.items():
            
            if mat_values['mat_type'] == "VRayFastSSS2":
                
                sss_map = mat_values['mat_param'].get('texmap_sss_color')
                base_color = eval(mat_values['mat_param'].get('sub_surface_color').strip("Color") )
                bump_map = mat_values['mat_param'].get('texmap_bump')
                opacity_map = None
                              
                ior = float (mat_values['mat_param']['IOR'])
                spec = float (mat_values['mat_param']['specular_glossiness'])                
                if spec is None:
                    spec = 0.50  
                
            elif mat_values['mat_type'] == "VRayMtl":
                
                base_map = mat_values['mat_param'].get('texmap_diffuse')
                base_color = eval (mat_values['mat_param'].get('diffuse') ) # convert to tuple
                specular_color = eval (mat_values['mat_param'].get('specular') ) # convert to tuple
                sss_map = None
                bump_map = mat_values['mat_param'].get('texmap_bump')
                opacity_map = None
                
                ior = float (mat_values['mat_param']['reflection_ior'])
                spec = float (mat_values['mat_param']['reflection_glossiness'])
                if spec is None:
                    spec = 0.50  

            
            elif mat_values['mat_type'] == "Standard":
                
                base_map = mat_values['mat_param'].get('diffuseMap')
                base_color = eval ( mat_values['mat_param'].get('diffuse') ) # convert to tuple
                specular_color = eval (mat_values['mat_param'].get('specular') ) # convert to tuple
                sss_map = None
                bump_map = mat_values['mat_param'].get('bumpMap')
                opacity_map = mat_values['mat_param'].get('opacityMap')            
                
                ior = float (mat_values['mat_param']['ior'])
                spec = mat_values['mat_param'].get('reflection_glossiness')
                if spec is None:
                    spec = 0.50  
                else: 
                    spec = float(spec)          

            else:
                print "Type:{} configuration not found".format(mat_values['mat_type'])
                continue

            # Query Existing Shading Engine 
            
            try: 
                shading_engine = cmds.listConnections(mat_name + '.outColor', type='shadingEngine')
            except Exception as e:
                print (e)
                           
            # Create Shader
                
            ai_shader = cmds.shadingNode("aiStandardSurface", asShader=True, name = mat_name + '_ai')                                
                       
            # Modify parameters
            
            cmds.setAttr(ai_shader + '.baseColor', base_color[0], base_color[1], base_color[2], type ="double3")
            cmds.setAttr(ai_shader + '.subsurfaceColor', base_color[0], base_color[1], base_color[2], type ="double3")
            cmds.setAttr(ai_shader + '.specularColor', specular_color[0], specular_color[1], specular_color[2], type ="double3")
            cmds.setAttr(ai_shader + '.specularRoughness', 1 -  spec)
            cmds.setAttr(ai_shader + '.specularIOR', ior)

            if mat_values['mat_type'] == "VRayFastSSS2":
                cmds.setAttr(ai_shader + '.subsurface', 0.7)
            
            # Maps

            if base_map and base_map != "None": # Dirty for revision
                base_file = create_file_place2d_node(base_map, suffix="_base")
                cmds.setAttr(base_file + '.colorSpace', 'sRGB', type='string')
                cmds.connectAttr(base_file + '.outColor', ai_shader + '.baseColor', force=True)
                cmds.setAttr(ai_shader + '.base', 1)
                
                cmds.setAttr(base_file + ".aiAutoTx", 0)
            
            if sss_map and sss_map != "None":
                sss_color_file = create_file_place2d_node(sss_map, suffix="_sss")
                cmds.setAttr(sss_color_file + '.colorSpace', 'sRGB', type='string')
                
                cmds.connectAttr(sss_color_file + '.outColor', ai_shader + '.baseColor', force=True)
                cmds.setAttr(ai_shader + '.base', 0.7)                
                
                cmds.connectAttr(sss_color_file + '.outColor', ai_shader + '.subsurfaceColor', force=True)
                cmds.setAttr(ai_shader + '.subsurface', 0.3)
                cmds.setAttr(ai_shader + '.subsurfaceScale', 1)
                cmds.setAttr(ai_shader + '.subsurfaceType', 1) # randomwalk
                cmds.setAttr(ai_shader + ".subsurfaceRadius",  1, 0.35, 0.20 , type ="double3")
                
                cmds.setAttr(sss_color_file + ".aiAutoTx", 0)
                
            if bump_map and bump_map != "None":
                bump_file = create_file_place2d_node(bump_map, suffix="_bump")              
                cmds.setAttr(bump_file + '.colorSpace', 'Raw', type='string')

                bump_node = cmds.shadingNode("aiBump2d", asUtility=True, name= mat_name + '_bump2D')
                cmds.connectAttr(bump_file + '.outAlpha', bump_node + '.bumpMap', force=True)
                cmds.setAttr(bump_node + '.bumpHeight', 1)

                cmds.connectAttr(bump_node + '.outValue', ai_shader + '.normalCamera', force=True)
                
                cmds.setAttr(bump_file + ".aiAutoTx", 0)

            if opacity_map and opacity_map != "None":
                opacity_file = create_file_place2d_node(opacity_map, suffix="_opacity")              
                cmds.setAttr(opacity_file + '.colorSpace', 'Raw', type='string')
                cmds.connectAttr(opacity_file + '.outColor', ai_shader + '.opacity', force=True) 
                
                cmds.setAttr(opacity_file + ".aiAutoTx", 0)            
            
            # Connect Shading Engine
            
            cmds.connectAttr(ai_shader + '.outColor', shading_engine[0] + '.surfaceShader', force=True)
            base_map = "None"
            sss_map = "None"
            bump_map = "None"
            opacity_map = "None"

            break # So dirty. In place only because it loops twice. Should be once. 
                
mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')

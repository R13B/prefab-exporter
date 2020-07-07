# ##### BEGIN LICENSE BLOCK #####
#
# This program is licensed under The MIT License:
# see LICENSE for the full license text
#
# ##### END LICENSE BLOCK #####

import os
import time
import math
import bpy
import mathutils

######################################################
# EXPORT MAIN FILES
######################################################


def export_prefab(file, shape_name, shape_exten, collision_type, decal_type, data_source):
    items = []

    items.append('//--- OBJECT WRITE BEGIN ---')
    items.append('$ThisPrefab = new SimGroup() {')
    items.append('  canSave = "1";')
    items.append('  canSaveDynamicFields = "1";\n')

    for ob in data_source:

        # O X é Y, pois o Torque3d é invetido
        rot_x = ob.rotation_axis_angle[2]
        rot_y = ob.rotation_axis_angle[1]
        rot_z = ob.rotation_axis_angle[3]

        # Calculo o radiano (sendo que 360 é igual 6..., ou seja
        #divido por ele mesmo e depois multiplico para obter o grau exato
        # é usado o pi
        rot_w_angle = (360/6.283185)*ob.rotation_axis_angle[0]

        # Como o torque calcular o grau 360 em 240 e depois 120
        rot_a = 0
        if rot_w_angle <= 240:
           rot_a = rot_w_angle
        elif rot_w_angle > 240:
           rot_a = rot_w_angle - 240

        shape_exten_name = "Not Set"
        if shape_exten == "0":
            shape_exten_name = ".DAE"
        elif shape_exten == "1":
            shape_exten_name = ".dts"
        elif shape_exten == "2":
            shape_exten_name = ""

        collision_type_name = "Not Set"
        if collision_type == "0":
            collision_type_name = "Collision Mesh"
        elif collision_type == "1":
            collision_type_name = "Visible Mesh"
        elif collision_type == "2":
            collision_type_name = "Visible Mesh Final"
        elif collision_type == "3":
            collision_type_name = "Bounds"
        elif collision_type == "4":
            collision_type_name = "None"

        decal_type_name = "Not Set"
        if decal_type == "0":
            decal_type_name = "Collision Mesh"
        elif decal_type == "1":
            decal_type_name = "Visible Mesh"
        elif decal_type == "2":
            decal_type_name = "Visible Mesh Final"
        elif decal_type == "3":
            decal_type_name = "Bounds"
        elif decal_type == "4":
            decal_type_name = "None"

        items.append(
            '  new TSStatic() {\n' +
            '    shapeName = "' + shape_name + ob.name + shape_exten_name + '";\n' +
            '    playAmbient = "1";\n' +
            '    meshCulling = "0";\n' +
            '    originSort = "0";\n' +
            '    collisionType = "' + collision_type_name + '";\n' +
            '    decalType = "' + decal_type_name + '";\n' +
            '    allowPlayerStep = "0";\n' +
            '    alphaFadeEnable = "0";\n' +
            '    alphaFadeStart = "100";\n' +
            '    alphaFadeEnd = "150";\n' +
            '    alphaFadeInverse = "0";\n' +
            '    renderNormals = "0";\n' +
            '    forceDetail = "-1";\n' +
            '    position = "' + str(ob.location[0]) + ' ' + str(ob.location[1]) + ' ' + str(ob.location[2]) + '";\n' +
            '    rotation = "' + str(rot_x) + ' ' + str(rot_y) + ' ' + str(rot_z) + ' ' + str(rot_a) + '";\n' +
            '    scale = "' + str(ob.scale[1]) + ' ' + str(ob.scale[0]) + ' ' + str(ob.scale[2]) + '";\n' +
            '    canSave = "1";\n' +
            '    canSaveDynamicFields = "1";\n' +
            '  };\n'
        )

    items.append('};')
    items.append('//--- OBJECT WRITE END ---')

    # write to file
    file.write("\n".join(items))
    file.close()
    return


######################################################
# EXPORT
######################################################
def save_prefab(filepath,
                shape_name,
                shape_exten,
                collision_type,
                decal_type,
                selection_only,
                context):

    print("exporting prefab: %r..." % (filepath))

    time1 = time.clock()

    # get data source
    data_source = bpy.data.objects
    if selection_only:
        data_source = bpy.context.selected_objects

    # write prefab
    file = open(filepath, 'w')
    export_prefab(file, shape_name, shape_exten, collision_type, decal_type, data_source)

    # prefab export complete
    print(" done in %.4f sec." % (time.clock() - time1))


def save(operator,
         context,
         filepath="",
         shape_name="none",
         shape_exten="0",
         collision_type="0",
         decal_type="1",
         selection_only=False
         ):

    # check item length
    if len(shape_name) == 0:
        shape_name = "No shape path set/"

    # save prefab
    save_prefab(filepath,
                shape_name,
                shape_exten,
                collision_type,
                decal_type,
                selection_only,
                context,
                )

    return {'FINISHED'}

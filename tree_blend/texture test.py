### libraries
from os import path, makedirs
import os.path
import bpy
from math import sqrt, radians, pi, cos, sin, acos, fabs, ceil
from random import random, randint, uniform, Random, gauss
from datetime import datetime
from time import sleep
from string import ascii_lowercase
from mathutils import Vector

#set the scene
def reset_scene():
	bpy.ops.object.select_all(action = 'DESELECT')
	bpy.ops.object.select_pattern(pattern = "*")
	n = len(bpy.context.selected_objects)
	bpy.ops.object.delete()
	for material in bpy.data.materials:
		if not material.users:
			bpy.data.materials.remove(material)
	for texture in bpy.data.textures:
		if not texture.users:
			bpy.data.textures.remove(texture)


reset_scene()
scene = bpy.data.scenes["Scene"]

#add tree
obj = bpy.ops.curve.tree_add(bevel=True,showLeaves=True,scale=11,baseSize=0.1,baseSplits=2, segSplits=(0.24,0.24,0,0),splitAngle=(6.475,6.475,6.475,6.475),attractUp=0.28,levels=4, length=(1.027,0.327,0.627,0.477),branches=(50,30,10,10),			leaves=50,leafScale=0.1,leafScaleX=1.65, ratioPower = 1.02)

tree = bpy.data.objects['tree']
leafs = bpy.data.objects['leaves']

#add camera and light
obj_position = bpy.data.objects['tree'].location
camera_position = (15, 15, 0)
bpy.ops.object.camera_add(location = camera_position)
the_camera = bpy.data.objects["Camera"]
camera_location = the_camera.matrix_world.to_translation()
camera_direction = obj_position - camera_location
camera_rotation = camera_direction.to_track_quat('-Z', 'Y')
the_camera.rotation_euler = camera_rotation.to_euler()
the_camera.delta_location += Vector((0,0,8))
bpy.context.scene.render.resolution_y = 2000
bpy.context.scene.render.resolution_x = 1000
lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')
lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
scene.objects.link(lamp_object)
lamp_object.location = (5,5,10)
lamp_object.select = True
scene.objects.active = lamp_object


#add in the bark texture to the tree
bark_file = "/home/labcomp/Desktop/Blender/Textures/treebark16.jpg"
mat = bpy.data.materials.new("material")
mat_texture = mat.texture_slots.add()
img = bpy.data.images.load(bark_file)
tex = bpy.data.textures.new("bark_tex", type = "IMAGE")
tex.image = img
mat_texture.texture = tex
mat_texture.texture_coords = "UV"
mat_texture.mapping = "TUBE"
tree.data.materials.append(mat)

leaf_file = "/home/labcomp/Desktop/Blender/Textures/leaf16.jpg"
mat = bpy.data.materials.new("material")
mat_texture = mat.texture_slots.add()
img = bpy.data.images.load(leaf_file)
tex = bpy.data.textures.new("leaf_tex", type = "IMAGE")
tex.image = img
mat_texture.texture = tex
mat_texture.texture_coords = "UV"
mat_texture.mapping = "FLAT"
leafs.data.materials.append(mat)

print("done")

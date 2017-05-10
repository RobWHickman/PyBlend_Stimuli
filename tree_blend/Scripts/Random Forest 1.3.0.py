# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:10:33 2017
@author: robert
"""

"""
Generate trees which vary by set parameters using the Sapling add-on for Blender
--------------------------------------------------------------------------------
Firstly, imports libraries. Then sets values or T/F for switches to control the output. To produce grids use T/T/F
for the randomness of the tree. The two axes of variation are controlled at the bottom with var1_mu and var2_mu.
Generally set all production randomness to True and then use >10 iterations and a grid of at least 6 (36 'bins').
This should take ~20 minutes to run.
The main body is composed of five functions:
	- reset_scene():
		deletes everything in the scene and removes all textures. will be run at the start of each iteration
	- tree_add():
		adds the tree (or a cube). Generally you want controlled randomness (where most randomness is aesthetic
		except for the two branchy/leafy values specified at the bottom). Can also produce a 'fully' random tree
		where every parameter is free to vary, or a 'debug' tree which should produce the same tree each time
	- production_add():
		adds a new camera and lamp. these can be in a set position of be randomly placed around the tree which
		is the centre of the scene. Only argument is camera_radius which sets how far away from the tree the
		camera should be set
	- environment_add():
		colours the tree/leafs/grass/sky based on wether these should be set or random
	- render_scene():
		renders the scene and saves it based on either the system time or the leafy/branchy-ness.
These are then fed through two sets of loops:
	- one for the number of iterations- basically how many trees for each conditino to create
	- the second for the grid_position (the amount of leafy and branchy-ness) if a grid is set via controlled_randomness
They are outputted to a folder defined by Output_directory in a new folder based upon the system time.
Latest version: 1.3.0 (April 26th, 2017)
"""

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

#set the random number generator to override the global seed
#IF YOU DO NOT DO THIS YOU WILL NOT GENERATE RANDOM NUMBERS
randomgen = Random()

#How should the file be run?
#how many trees to make
Iterations = 100
#what format the filename should be in- systime of generation, or parameters of the tree
SysTime_save = False
#if generating a grid of trees, how many rows/columns?
Grid_size = 6
#what is the main folder directory for generated images
Output_directory = "/home/labcomp/Desktop/Blender/imagebin"

#to clear the scene of objects, camera etc.
def reset_scene():
	#delete all objects
	bpy.ops.object.select_all(action = 'DESELECT')
	bpy.ops.object.select_pattern(pattern = "*")
	n = len(bpy.context.selected_objects)
	bpy.ops.object.delete()
	#also get rid of materials and textures because why not
	for material in bpy.data.materials:
		if not material.users:
			bpy.data.materials.remove(material)
	for texture in bpy.data.textures:
		if not texture.users:
			bpy.data.textures.remove(texture)

#adds a tree (or cube) 
def tree_add(x, y, var1_mu, var1_sig, var2_mu, var2_sig, iteration,
	Tree_not_cube = True, Controlled_randomness = True, Basic_debugging_tree = False):
	#How random a tree should we make?
	#make a tree/cube
	if Tree_not_cube:
		#make a truly random tree or a one that varies in controlled ways
		if Controlled_randomness:
			#make a standard debug tree or use it to paramaterise out features?
			if Basic_debugging_tree: #basic set tree
				obj = bpy.ops.curve.tree_add(bevel=True,showLeaves=True,scale=11,baseSize=0.1,baseSplits=3,
					segSplits=(0.24,0.24,0,0),splitAngle=(6.475,6.475,6.475,6.475),attractUp=0.28,levels=4,
					length=(1.027,0.327,0.627,0.477),branches=(56,36,16,16),leaves=20,leafScale=0.045,leafScaleX=1.65)
			else: #to form grids of trees
				obj = bpy.ops.curve.tree_add(bevel=True,
							showLeaves=True,
							seed = iteration,
							scale=randomgen.randint(10,14),
							baseSize=0.1,
							baseSplits=3,
							segSplits=(0.24,0.24,0,0),
							splitAngle=(randomgen.gauss(0, 20),randomgen.gauss(0, 20),randomgen.gauss(0, 20),randomgen.gauss(0, 20)),
							attractUp=randomgen.gauss(0.35,0.2),
							levels=4,
							length=(1.027,0.327,0.627,0.477),
							leafScale=0.08,
							leafScaleX=randomgen.lognormvariate(0.5, 0),
							rotate=(randomgen.randint(0,180),randomgen.randint(0,180),randomgen.randint(0,180),randomgen.randint(0,180)),
					branches=(var1_mu+(x*var1_sig),var1_mu+(x*var1_sig),7,15),
					leaves = var2_mu+(y*var2_sig))
		else:
			obj = bpy.ops.curve.tree_add(#always set these to True
							bevel = True, showLeaves = True,
							#general size parameters
							scale = scale_num, baseSize = baseSize_num, baseSplits = baseSplits_num,
							segSplits = (segSplit_num, segSplit_num, 0, 0), attractUp = attractUp_num,
							splitAngle = (splitAngle_num,splitAngle_num,splitAngle_num,splitAngle_num),
							#parameters for the 'branchiness'
							levels = levels_num,
							length = (1+branchLength_num, 0.3+branchLength_num, 0.6+branchLength_num, 0.45+branchLength_num),
							branches = (50+branchNum_num, 30+branchNum_num, 10+branchNum_num, 10+branchNum_num),
							#parameters for the leaves
							leaves = leaves_num, leafScale = leafScale_num, leafScaleX = leafScaleX_num)
	else: #adds a cube
		bpy.ops.mesh.primitive_cube_add(radius=1, location = (0,0,0)) 

def production_add(camera_radius, Camera_random = False, LightSource_random = False, Tree_not_cube = True):
	if Tree_not_cube:
		obj_position = bpy.data.objects['tree'].location
	else:
		obj_position = bpy.data.objects["Cube"].location
	#find either the random or pre-set camera position
	if Camera_random: 	#move the camera randomly or fix it
		alpha = 2 * pi * randomgen.random()
		beta = acos(2 * randomgen.random() - 1)
		#limit the z axis of the random camera position to stop it being above object
		while fabs(camera_radius * cos(beta)) / camera_radius > 0.3 and camera_radius * sin(beta) * cos(alpha) < 0:
			alpha = 2 * pi * randomgen.random()
			beta = acos(2 * randomgen.random() - 1)
		#find the x,y,z coordinates
		x = obj_position[0] + (r * sin(beta) * cos(alpha))
		y = obj_position[1] + (r * sin(beta) * sin(alpha))
		z = fabs(obj_position[2] + (r * cos(phi)))
		camera_position = (x,y,z)
	else:
		#set and x and y to be the same
		x_and_y = sqrt(0.5 * (camera_radius ** 2))
		camera_position = (x_and_y, x_and_y, 0)
	#add in the camera at this position
	bpy.ops.object.camera_add(location = camera_position)
	the_camera = bpy.data.objects["Camera"]
	camera_location = the_camera.matrix_world.to_translation()
	#rotate the camera to view the tree
	#points the camera at the centre of the tree
	camera_direction = obj_position - camera_location
	#point up a bit instead of at the base
	camera_rotation = camera_direction.to_track_quat('-Z', 'Y')
	the_camera.rotation_euler = camera_rotation.to_euler()
	#move the whole frame up to prevent cropping
	the_camera.delta_location += Vector((0,0,8))
	#set the camera resolution
	bpy.context.scene.render.resolution_y = 2000
	bpy.context.scene.render.resolution_x = 1000

	# Create new lamp datablock
	lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')
	# Create new object with our lamp datablock
	lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
	# Link lamp object to the scene so it'll appear in this scene
	scene.objects.link(lamp_object)
	# Place lamp to a specified location
	lamp_object.location = (randomgen.randint(3,10), randomgen.randint(3,10), randomgen.randint(3,10))
	# And finally select it make active
	lamp_object.select = True
	scene.objects.active = lamp_object

def environment_add(Colour_random = True, Transparent_background = True):
	#have a transparent background
	if Transparent_background:
		bpy.data.scenes["Scene"].render.alpha_mode = 'TRANSPARENT'
	#or add in a sky-coloured background
	else:
		bpy.data.scenes["Scene"].render.alpha_mode = 'SKY'	
		world = bpy.context.scene.world
		world.use_sky_blend = True
		world.horizon_color = (0.09375, 0.457, 0.5235)
		world.zenith_color = (0.09375, 0.457, 0.5235)

	#add a small green patch of grass below the tree
	bpy.ops.mesh.primitive_plane_add(radius=2)
	bpy.context.scene.objects.active = bpy.data.objects['Plane']
	activeObject = bpy.context.active_object
	grassy_field = bpy.data.materials.new(name="GrassyGrass")
	activeObject.data.materials.append(grassy_field)
	if Colour_random:
		bpy.context.object.active_material.diffuse_color = (randomgen.gauss(0.2, 0.1),randomgen.gauss(0.8, 0.2),0)
	else:
		bpy.context.object.active_material.diffuse_color = (0,1,0)

	#add colour to leaves
	bpy.context.scene.objects.active = bpy.data.objects['leaves']
	activeObject = bpy.context.active_object
	Leafmat = bpy.data.materials.new(name="LeafyLeaves")
	activeObject.data.materials.append(Leafmat)
	if Colour_random:
		leaf_green = (randomgen.random(), randomgen.random(), 0)
	else:
		leaf_green = (0,1,0)
	bpy.context.object.active_material.diffuse_color = leaf_green
	#and then the tree itself
	bpy.context.scene.objects.active = bpy.data.objects['tree']
	activeObject = bpy.context.active_object
	Branchmat = bpy.data.materials.new(name="BranchyBranches")
	activeObject.data.materials.append(Branchmat)
	if Colour_random:
		#randomised around "saddlewood brown"
		branch_brown = (randomgen.lognormvariate(-0.2,0.5),randomgen.gauss(0.27,0.07),randomgen.gauss(0.07, 0.02))
	else:
		branch_brown = (0.55, 0.27, 0.07)
	bpy.context.object.active_material.diffuse_color = branch_brown

def render_scene(output_folder, grid_pos, iteration):
	if SysTime_save:
		image_string = datetime.now().strftime("%d-%m:::%H:%M:%S")
	else:
		image_string = (grid_pos + "_" + ascii_lowercase[iteration])
	bpy.data.scenes['Scene'].render.filepath = os.path.join(output_folder, image_string)
	bpy.context.scene.camera = bpy.data.objects['Camera']
	bpy.ops.render.render(write_still=True)
	#do a little sleep to prevent overwriting
	sleep(1)

#explanation of and values for the tree parameters if creating truly random single trees
#leaves
leaves_num = randomgen.gauss(30, 10) #how many leaves
leafScale_num = randomgen.gauss(0.17, 0.1) #how big the leaves are
leafScaleX_num = randomgen.lognormvariate(0.5, 0) #how squircle vs. long the leaves are
#general size and splitting
scale_num = randomgen.randint(9,17) #how big the tree is
baseSize_num = randomgen.uniform(0.05,0.15) #how tall the trunk is before it starts to split
baseSplits_num = randomgen.randint(1,3) #how many primary splits of the trunk there are
segSplit_num = randomgen.gauss(0.1, 0.1) #how many extra splits per segment there are
splitAngle_num = randomgen.gauss(0, 20) #the angle these splits happen at
attractUp_num = randomgen.gauss(0.35, 0.2) #how much branches bend towards the 'sun'
#branches
levels_num = randomgen.randint(2,4) #the number of levels of branches (e.g. how many splits)
branchLength_num = randomgen.gauss(0, 0.05) #how long the branches are
branchNum_num = round(randomgen.gauss(0, 5)) #how many branches there are per level

#run it all
#make a new directory for the images
run_id = datetime.now().strftime("%d %B %H:%M")
run_directory = path.join(Output_directory, run_id)
if not path.exists(run_directory):
	makedirs(run_directory)
#iterate a number of times
for repeats in range(Iterations):
	scene = bpy.data.scenes["Scene"]
	#for grids run altering the two paramters each time
	if Controlled_randomness:
		for x_repeat in range(Grid_size):
			for y_repeat in range(Grid_size):
				#reset and grab the scene
				reset_scene()
				#make subdirectory bin for each paramater combination
				grid_string = ("b" + str(x_repeat + 1) + "l" + str(y_repeat+1))
				grid_subdirectory = path.join(run_directory, grid_string)
				#if not path.exists(grid_subdirectory):
					#makedirs(grid_subdirectory)
				#adds trees and cameras and environment
				tree = tree_add(x = x_repeat, y = y_repeat, var1_sig = 5, var1_mu = 15, var2_sig = 3, var2_mu = 1, iteration = repeats)
				production_add(camera_radius = 25)
				environment_add()
				#render it all
				render_scene(output_folder = path.join(run_directory), grid_pos = grid_string, iteration = repeats)
	else:
		#reset and grab the scene
		reset_scene()
		#adds trees and cameras and environment
		tree_add(x = 0, y = 0, var1_sig = 0, var1_mu = 0, var2_sig = 0, var2_mu = 0, iteration = repeats)
		production_add(camera_radius = 25)
		environment_add()
		#render it all
		render_scene(output_folder = run_directory, iteration = repeats)

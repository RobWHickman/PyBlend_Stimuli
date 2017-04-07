#written by Robert William Hickman using the Blender python API
#tested using Blender 2.76 and 2.77
#available at https://github.com/RobWHickman/Summerfield-Lab
#email at robwhickman@gmail.com
#distributed freely under MIT general license 1/4/2017

### libraries
import os
import os.path
import bpy
from math import sqrt, radians, pi, cos, sin, acos, fabs, ceil
from random import random, randint, uniform, Random, gauss
from datetime import datetime
from time import sleep
import mathutils

#set the random number generator to override the global seed
#IF YOU DO NOT DO THIS YOU WILL NOT GENERATE RANDOM NUMBERS
randomgen = Random()

#Universal parameters
#How random a tree should we make?
#make a tree/cube
Tree = True
#make a truly random tree or a basic prototype
Random_Forest = False
#makea standard debug tree or use it to paramaterise out features?
Debug = False

#What should the environment look like?
#colour the tree randomly
Colour_random = False
#move the camera randomly or fix it
Camera_random = False
#move the light source randomly or fix it
LightSource_random = False #**WIP**

#How should the file be run?
#how many trees to make
Iterations = 5
#what format the filename should be in- systime of generation, or parameters of the tree
SysTime_save = False

#where to save the output
image_folder = "/home/robert/Desktop/Summerfield Lab/Blender/imagebin"

#to clear the scene of objects, camera etc.
def reset_scene():
	for item in bpy.data.objects:
		#must be a better way to do this **WIP**
		item.select = item.name.startswith('C') | item.name.startswith('l') | item.name.startswith('t') | item.name.startswith('e') | item.name.startswith('P')
	bpy.ops.object.delete()
	#also get rid of materials and textures because why not
	for material in bpy.data.materials:
		if not material.users:
			bpy.data.materials.remove(material)
	for texture in bpy.data.textures:
		if not texture.users:
			bpy.data.textures.remove(texture)

#to generate the position of the camera randomly
#in a hemisphere around the centre of the scene [0,0,0] 
def hemisphere_position(sphere_centre, r, rand_angle1, rand_angle2):
	#use two random numbers to generate angles from which a sphere can be generated
	theta = rand_angle1
	phi = rand_angle2
	#use these two angles to generate x,y and z co-ordinates for the camera
	x = sphere_centre[0] + (r * sin(phi) * cos(theta))
	y = sphere_centre[1] + (r * sin(phi) * sin(theta))
	#z is always positive (never 'below' the tree)
	#z is also limited to 2/3rds of r when we set randnum2
	z = fabs(sphere_centre[2] + (r * cos(phi)))
	#return a set of coordinates which orbit the centre of the rendered object
	return(x,y,z)

#plot a tree based on leafiness and branchiness and render it to a folder
#x is var1, y is var2
def tree_plotter(save_folder, x, y, var1_mu, var1_sig, var2_mu, var2_sig):
	#generate the values for the tree parameters
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

	#add the tree
	if Tree:
		if Random_Forest:
			obj = bpy.ops.curve.tree_add(#always set these to True
										bevel = True,
										showLeaves = True,
										#general size parameters
										scale = scale_num,
										baseSize = baseSize_num,
										baseSplits = baseSplits_num,
										segSplits = (segSplit_num, segSplit_num, 0, 0),
										splitAngle = (splitAngle_num,splitAngle_num,splitAngle_num,splitAngle_num),
										attractUp = attractUp_num,
										#parameters for the 'branchiness'
										levels = levels_num,
										length = (1+branchLength_num, 0.3+branchLength_num, 0.6+branchLength_num, 0.45+branchLength_num),
										branches = (50+branchNum_num, 30+branchNum_num, 10+branchNum_num, 10+branchNum_num),
										#parameters for the leaves
										leaves = leaves_num,
										leafScale = leafScale_num,
										leafScaleX = leafScaleX_num)
			obj_centre = bpy.data.objects['tree'].location
		#or a basic one for debugging
		else:
			if Debug:
				obj = bpy.ops.curve.tree_add(bevel=True,showLeaves=True,
					scale=11,baseSize=0.1,baseSplits=3,segSplits=(0.24,0.24,0,0),
					splitAngle=(6.475,6.475,6.475,6.475),attractUp=0.28,
					levels=4,length=(1.027,0.327,0.627,0.477),branches=(56,36,16,16),
					leaves=20,leafScale=0.045,leafScaleX=1.65)
			else:
				obj = bpy.ops.curve.tree_add(bevel=True,showLeaves=True,
				scale=11,baseSize=0.1,baseSplits=3,segSplits=(0.24,0.24,0,0),
				splitAngle=(6.475,6.475,6.475,6.475),attractUp=0.28,
				levels=4,length=(1.027,0.327,0.627,0.477),
				leafScale=0.045,leafScaleX=1.65,
				branches = (50+var1_mu+(x*var1_sig), 30+var1_mu+(x*var1_sig), 10+var1_mu+(x*var1_sig), 10+var1_mu+(x*var1_sig),),
				leaves = var2_mu+(y*var2_sig))
			obj_centre = bpy.data.objects['tree'].location
	#or use the cube to check
	else:
		bpy.ops.mesh.primitive_cube_add(radius=1, location = (0,0,0)) #adds a cube
		obj_centre = bpy.data.objects["Cube"].location

	#set parameters for the camera
	#how far away to take pictures from
	camera_radius = 40
	#angles from which to generate co-ordinates on a sphere
	alpha = 2 * pi * randomgen.random()
	beta = acos(2 * randomgen.random() - 1)
	while fabs(camera_radius * cos(beta)) / camera_radius > 0.3 and camera_radius * sin(beta) * cos(alpha) < 0:
		alpha = 2 * pi * randomgen.random()
		beta = acos(2 * randomgen.random() - 1)

	#feed these into the hemipshere_position function to generate the camera position
	if Camera_random:
		camera_position = hemisphere_position((0,0,0), camera_radius, alpha, beta)
	else:
		camera_position = (20,34.64,0)

	#add in the camera at this point
	bpy.ops.object.camera_add(location = camera_position)
	the_camera = bpy.data.objects["Camera"]
	camera_location = the_camera.matrix_world.to_translation()

	#rotate the camera to view the tree
	#points the camera at the centre of the tree
	camera_direction = obj_centre - camera_location
	#point up a bit instead of at the base
	camera_rotation = camera_direction.to_track_quat('-Z', 'Y')
	the_camera.rotation_euler = camera_rotation.to_euler()
	#move the whole frame up a bit so trees don't get cut off as much
	the_camera.delta_location += mathutils.Vector((0, 0, 9))

	#add some colour
	#https://www.youtube.com/watch?v=zphAHMPtu4g
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

	#add a small green patch of grass below the tree
	bpy.ops.mesh.primitive_plane_add(radius=2)
	bpy.context.scene.objects.active = bpy.data.objects['Plane']
	activeObject = bpy.context.active_object
	grassy_field = bpy.data.materials.new(name="GrassyGrass")
	activeObject.data.materials.append(grassy_field)
	bpy.context.object.active_material.diffuse_color = (0,1,0)

	#render an image and save it to a specified folder
	#saves a .png image
	if SysTime_save:
		image_string = datetime.now().strftime("%d-%m:::%H:%M:%S")
	else:
		image_string = ("grid="+str(x)+":"+str(y))
	bpy.data.scenes['Scene'].render.filepath = os.path.join(save_folder, image_string)
	bpy.context.scene.camera = bpy.data.objects['Camera']
	bpy.ops.render.render(write_still=True)
	#do a little sleep to prevent overwriting
	sleep(1)

# #run the functions iterated x times
# for iteration in range(Iterations):
# 	#rest the scene
# 	reset_scene()
# 	#plot the tree
# 	tree_plotter(save_folder = image_folder)

#the the function iterated x*y times to create a grid
grid_size = 5
lower = ceil(0 - (grid_size / 2))
upper = grid_size + lower
for xaxis in range(lower, upper):
	for yaxis in range(lower, upper):
		#rest the scene
		reset_scene()
		#plot the tree
		tree_plotter(save_folder = image_folder, x=xaxis,y=yaxis,
			var1_mu = 0,
			var1_sig = 5,
			var2_mu = 21,
			var2_sig = 10)


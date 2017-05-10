
Work to generate random trees using the sapling add-on for Blender

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

To Run:
--------------------------------------------------------------------------------

1) Clone the repo somewhere on your PC using https://github.com/RobWHickman/Summerfield-Lab.git or the GUI
  1.2) Extract the downloaded file. You can prune away all except the tree_blend folder if you so wish but
  will need to update the filepaths in the Random Forest script
2) Install Blender from https://www.blender.org/download/
3) Run:

cd "/home/path/to/tree_blend/Scripts"
current_file = "Random Forest x.y.z"
blender -b -P ./current_file

Latest version: 1.3.2 (May 9th, 2017)

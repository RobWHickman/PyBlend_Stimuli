#modules
import bpy
import os
import math

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

reset_scene()

scene = bpy.data.scenes["Scene"]

#add a sphere
bpy.ops.mesh.primitive_uv_sphere_add(
	segments = 96, ring_count=48, size = 1.0,
	location = (0,0,0), rotation = (0,0,0))

#select the sphere
sphere = bpy.context.object

#smooth the sphere
bpy.ops.object.shade_smooth()

#link to the picture that will cover the sphere as a 'map'
folder = "/home/robert/Desktop/Summerfield Lab/My Code/Planet Code/Maps"
imgname = "map.bmp"

file = os.path.join(folder, imgname)

#add in the material and texture from the map image
mat = bpy.data.materials.new("material")
mat_texture = mat.texture_slots.add()
img = bpy.data.images.load(file)
tex = bpy.data.textures.new('planet_tex', type = 'IMAGE')
tex.image = img

#map the material
mat_texture.texture = tex
mat_texture.texture_coords = 'ORCO'
mat_texture.mapping = 'SPHERE'

#add a camera and point it at the sphere
bpy.ops.object.camera_add(location = (5.0, 5.0, 0))
the_camera = bpy.data.objects["Camera"]
camera_location = the_camera.matrix_world.to_translation()
camera_direction = sphere.location - camera_location
camera_rotation = camera_direction.to_track_quat('-Z', 'Y')
the_camera.rotation_euler = camera_rotation.to_euler()

# Create new lamp and set it on
lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')
lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
scene.objects.link(lamp_object)
lamp_object.location = (5.0, 5.0, 5.0)
lamp_object.select = True
scene.objects.active = lamp_object

#overlay the material on the sphere
sphere.data.materials.append(mat)

#set the animation
scene.frame_start = 1
scene.frame_end = 200

sphere.rotation_euler = (0, 0, 0)
sphere.keyframe_insert('rotation_euler', index=2 ,frame=1)

sphere.rotation_euler = (0, 0, math.radians(360))
sphere.keyframe_insert('rotation_euler', index=2 ,frame=100)

scene.render.use_stamp = 1
scene.render.stamp_background = (0,0,0,1)

#output folder
output_folder = "/home/robert/Desktop/Summerfield Lab/My Code/Planet Code/Animations"

#render
bpy.data.scenes['Scene'].render.filepath = os.path.join(output_folder, "planimation")
bpy.context.scene.camera = bpy.data.objects['Camera']
scene.render.image_settings.file_format = "AVI_JPEG"
bpy.ops.render.render(animation=True)


# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:02:33 2017

@author: robert
"""

import noise
import random
import PIL 
import os

#set output folder and map name
planet_folder = "/home/robert/Desktop/Summerfield Lab/My Code/Planet Code/Maps"
file_name = "map.bmp"
output_file  = os.path.join(planet_folder, file_name)

#set the seed
seed = random.random()

#set up the image of x,y pixels
#should be twice as wide as high for sphere
img = PIL.Image.new( 'RGB', (2000,1000), "black")
pixels = img.load()

#
frequency = 300.0

#
octs = 6

#m
multiplier = 1.5

#add
addition = 0.8

for y in range(img.size[0]):
    for x in range(img.size[1]):
        n = noise.snoise3(x/frequency, y/frequency, seed, octaves = octs) * multiplier + addition
        if n < 0.000000000000000000000000001:
            pixels[y,x] = (255, 255, 255) #snow
        elif n >= 0.000000000000000000000000001 and n < 0.15:
            pixels[y,x] = (128, 128, 128) #rock
        elif n >= 0.15 and n < 0.5:
            pixels[y,x] = (34,139,34) #forest
        elif n >= 0.5 and n < 0.7:
            pixels[y,x] = (32, 160, 0) #grass
        elif n >= 0.7 and n < 0.75:
            pixels[y,x] = (240, 240, 64) #sand
        elif n >= 0.75 and n < 0.8:
            pixels[y,x] = (0, 128, 255) #shore
        elif n >= 0.8 and n < 0.95:
            pixels[y,x] = (0, 0, 255) #shallows
        else:
            pixels[y,x] = (0, 0, 128) #deeps

#save the created map            
img.save(output_file)
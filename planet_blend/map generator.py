# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:02:33 2017

@author: robert
"""

import noise
import random
import PIL 
import os

randomgen = random.Random()

#how many maps to make?
repeats = 10

for repeat in range(repeats):

    #set output folder and map name
    planet_folder = "/home/robert/Desktop/Summerfield Lab/My Code/Planet Code/Maps"
    file_name = "map"
    file_num = repeat
    file_ext = ".bmp"
    output_file  = os.path.join(planet_folder, (file_name+ str(file_num)+ file_ext))

    #set the seed
    seed = randomgen.random()
    #seed = 0.22081992
    print(seed)

    #set up the image of x,y pixels
    #should be twice as wide as high for sphere
    img = PIL.Image.new( 'RGB', (2000,1000), "black")
    pixels = img.load()

    #how small the repeating units are (i.e. how small the islands are)
    #conserves land/water balance
    frequency = randomgen.gauss(270, 70)
    #add more layers of finer noise
    #after 6 is mostly redundant
    octs = 6
    #biases the results towards extremes (0,1) or middle (0.5)
    #1.5 seems a nice balance
    multiplier = randomgen.gauss(1.5, 0.3)
    #biases towards higher/lower (0/1)
    addition = randomgen.gauss(0.8, 0.2)

    #colour every pixel based on snoise3 height map
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
    
    flip_left = randomgen.random()
    if flip_left > 0.5:    
        img.rotate(180)
    
    #save the created map            
    img.save(output_file)
    #or show the img instead
    #img.show()
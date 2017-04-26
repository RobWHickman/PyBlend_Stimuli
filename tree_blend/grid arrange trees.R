library(png)
library(grid)
library(gridExtra)
library(ggplot2)
library(lattice)
library(raster)

var1 = "branches"
mu1 = 0
sig1 = 5
var2 = "leaves"
mu2 = 11
sig2 = 5

zip_file <- "25thapril1"
dir <- paste0("/home/robert/Desktop/Summerfield Lab/My Code/Tree Scripts/Generated Trees/Grid Zips/", zip_file)
setwd(dir)

val_grid <- expand.grid(x=-2:2, y=-2:2)
pngs <- lapply(sprintf("grid=%i:%i.png", val_grid$x, val_grid$y), readPNG)
arranged_pngs <- lapply(pngs, rasterGrob)




grid.draw(grobTree(rectGrob(gp=gpar(fill="#56B4BE", lwd=0)), 
	grid.arrange(grobs=arranged_pngs)))

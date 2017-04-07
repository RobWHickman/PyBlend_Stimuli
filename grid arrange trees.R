library(png)
library(grid)
library(gridExtra)
library(ggplot2)

setwd('/home/robert/Desktop/Summerfield Lab/Blender/imagebin/Rgrid')

val_grid <- expand.grid(x=-2:2, y=-2:2)
pngs <- lapply(sprintf("grid=%i:%i.png", val_grid$x, val_grid$y), readPNG)
arranged_pngs = lapply(pngs, rasterGrob)
gridded_trees <- grid.arrange(grobs=arranged_pngs)

#!/usr/bin/env python
# GIMP Plug-In.

# Create montage from layers.

from gimpfu import *

def prt(*x):
	""" Print to error console. """
	pdb.gimp_message(x)

def montage(image,w,h,order):
	prt(image)
	# Verify parameters.
	w=max(1,w)
	h=max(1,h)
	# Get biggest layer.
	layers=image.layers
	layer_sizes=[(x.width,x.height) for x in layers]
	biggest_layer=max(layer_sizes)
	prt(biggest_layer)
	# Use it for cell size.
	(cell_w,cell_h)=biggest_layer
	# Duplicate the image.
	new_image=pdb.gimp_image_duplicate(image)
	# Resize it.
	pdb.gimp_image_resize(new_image,w*cell_w,h*cell_h,0,0)
	# Move layers.
	layers=new_image.layers
	if order==1:
		layers.reverse()
	iterations=min(len(layers),w*h)
	for i in range(0,iterations):
		x=layers[i]
		pdb.gimp_layer_set_offsets(x,(i%w)*cell_w,(i//w)*cell_h)
	# Display.
	pdb.gimp_display_new(new_image)	
	prt("done")
	

register(
	"python_fu_montage", # Proc name
	"Montage.", # Blurb
	"Position layers in a grid.", # Help
	"Crapola", # Author
	"https://github.com/crapola", # Copyright
	"2020", # Date
	"Montage", # Label
	"*", # Image types
	[
		(PF_IMAGE, "image", "Image", None),
		(PF_INT, "cols", "Columns", 2),
		(PF_INT, "rows", "Rows", 2),
		(PF_OPTION, "order", "Order", 0, ("Top to bottom","Bottom to top"))
	], # Params
	[], # Results
	montage, # Function
	menu="<Image>/Filters" # Menu
)

main()
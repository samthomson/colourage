import Image, ImageDraw
import os
import sys
import math

from os import listdir
from os.path import isfile, join
import rethinkdb as r

def get_colors(infile, outfile = '', numcolors=1, swatchsize=20, resize=150):
 
    image = Image.open(infile)
    image = image.resize((resize, resize))
    result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
    result.putalpha(0)
    colors = result.getcolors(resize*resize)

    return colors[0][1]

 
if __name__ == '__main__':

	# seed image, which will be analysed and a colage made from
	s_seed_image = "seed.JPG"
	ia_step_sizes = [16, 32, 64, 128, 256]
	ia_step_sizes = [16]


	im_seed = Image.open(s_seed_image)
	im_lodead_seed = im_seed.load()
	t_size_of_seed = im_seed.size
	i_shortest_side = min(t_size_of_seed)

	# create renderings
	for cColage in range(len(ia_step_sizes)):
		print "\nCreate image for step size %i " % ia_step_sizes[cColage]
		# define the block ssize based on the shortest size of the image
		i_block_size = i_shortest_side / ia_step_sizes[cColage]
		ia_xy_steps = [(t_size_of_seed[0] / i_block_size), (t_size_of_seed[1] / i_block_size)]

		# make sure we have enough blocks to encompass the seed
		if ia_xy_steps[0] * i_block_size < t_size_of_seed[0]:
			ia_xy_steps[0] += 1

		if ia_xy_steps[1] * i_block_size < t_size_of_seed[1]:
			ia_xy_steps[1] += 1

		print "block size: %i, x: %i, y: %i" % (i_block_size, ia_xy_steps[0], ia_xy_steps[1])
		#print "seed size: x: %i, y: %i" % (t_size_of_seed[0], t_size_of_seed[1])

		# create structure to hold block averages
		miColourHolder = [[[0 for x in xrange(ia_xy_steps[0])] for x in xrange(ia_xy_steps[1])] for RGB in xrange(3)]

		for x in range(t_size_of_seed[0]):
			for y in range(t_size_of_seed[1]):
				#if(im_lodead_seed[x,y] is not None):
				i_x = math.floor(x/ia_step_sizes[cColage])
				i_y = math.floor(y/ia_step_sizes[cColage])

				miColourHolder[i_x,i_y, R] = im_lodead_seed[x,y][0]
				miColourHolder[i_x,i_y, G] = im_lodead_seed[x,y][1]
				miColourHolder[i_x,i_y, B] = im_lodead_seed[x,y][2]




		# resize target image to 1/step size of seed and make square
import Image, ImageDraw
import os
import sys
import math

from os import listdir
from os.path import isfile, join
import rethinkdb as r

def s_get_path(conn, i_r, i_g, i_b):

	i_offset = 20
 
	iresult = r.table('seed_colours').filter(
		(r.row["red"] >= i_r-i_offset) & (r.row["red"] <= i_r+i_offset) &
		(r.row["green"] >= i_g-i_offset) & (r.row["green"] <= i_g+i_offset) &
		(r.row["blue"] >= i_b-i_offset) & (r.row["blue"] <= i_b+i_offset)
		).limit(1).run(conn)
	for image in result:
		return image["file"]

	return ""


 
if __name__ == '__main__':

	# seed image, which will be analysed and a colage made from
	s_seed_image = "seed.JPG"
	ia_step_sizes = [16, 32, 64, 128, 256]
	ia_step_sizes = [128]


	im_seed = Image.open(s_seed_image)
	im_lodead_seed = im_seed.load()
	t_size_of_seed = im_seed.size
	i_shortest_side = min(t_size_of_seed)

	conn = r.connect(host = 'localhost', db = 'colourage')

	r.db("colourage")

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
		#miColourHolder = [[0 for x in xrange(ia_xy_steps[0])] for y in xrange(ia_xy_steps[1])]
		miColourHolder = {}
		for x in range (0,ia_xy_steps[0]):
			miColourHolder [x]={}
			for y in range (0,ia_xy_steps[1]):
				miColourHolder[x][y] = {0,0,0,0}


		for x in range(t_size_of_seed[0]):
			for y in range(t_size_of_seed[1]):
				#if(im_lodead_seed[x,y] is not None):
				# calculate the block to add this pixels colour to the average of
				i_x = round(math.floor(x/ia_step_sizes[cColage]))
				i_y = round(math.floor(y/ia_step_sizes[cColage]))

				t_rgb = im_lodead_seed[x,y]

				#cd codeprint "RGB (%i,%i) : %i,%i,%i " % (x, y, t_rgb[0], t_rgb[1], t_rgb[2])

				miColourHolder[i_x, i_y, 0] = t_rgb[0] + miColourHolder[i_x, i_y, 0]
				miColourHolder[i_x, i_y, 1] = t_rgb[1] + miColourHolder[i_x, i_y, 1]
				miColourHolder[i_x, i_y, 2] = t_rgb[2] + miColourHolder[i_x, i_y, 2]
				miColourHolder[i_x, i_y, 3] = miColourHolder[i_x, i_y, 3] + 1

		print "there are now %i blocks(%i,%i), and %i pixels" % (i_x * i_y, i_x, i_y, x * y)

		# calculate averages
		for x in range(ia_xy_steps[0]):
			for y in range(ia_xy_steps[1]):
				miColourHolder[x,y,0] = miColourHolder[x,y,0] / miColourHolder[x,y,3]
				miColourHolder[x,y,1] = miColourHolder[x,y,1] / miColourHolder[x,y,3]
				miColourHolder[x,y,2] = miColourHolder[x,y,2] / miColourHolder[x,y,3]


		# go through each block and find a matching picture
		for x in range(ia_xy_steps[0]):
			for y in range(ia_xy_steps[1]):
				# search for a picture in db which is closest to this colour range
				print s_get_path(conn, miColourHolder[x,y,0], miColourHolder[x,y,1], miColourHolder[x,y,2])




		# resize target image to 1/step size of seed and make square
import Image, ImageDraw
import os
import sys
import math
import numpy

from os import listdir
from os.path import isfile, join
import sqlite3

def s_get_path(cursor, i_r, i_g, i_b):

	cursor.execute('''SELECT file FROM files ORDER BY ((red-?)*(red-?))+((green-?)*(green-?))+((blue-?)*(blue-?)) ASC LIMIT 0,1''', (i_r, i_r, i_g, i_g, i_b, i_b))
	#$sQuery = "SELECT `file` FROM `colour_tags` ORDER BY ((r-:r)*(r-:r))+((g-:g)*(g-:g))+((b-:b)*(b-:b)) ASC LIMIT 0,500";
                    
	return cursor.fetchone()[0]

 
if __name__ == '__main__':

	# seed image, which will be analysed and a colage made from
	s_seed_image = "seed.JPG"
	ia_step_sizes = [16, 32, 64, 128, 256]
	ia_step_sizes = [128,256]


	im_seed = Image.open(s_seed_image)
	im_lodead_seed = im_seed.load()
	t_size_of_seed = im_seed.size
	i_shortest_side = min(t_size_of_seed)

	i_analysing_accuracy = 10

	im_new_colage = Image.new("RGB", t_size_of_seed)


	db = sqlite3.connect('database')
	cursor = db.cursor()


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
		miColourHolder = numpy.zeros((ia_xy_steps[0],ia_xy_steps[1],4))
		print "step container: %i, %i" % (ia_xy_steps[0], ia_xy_steps[1])


		for x in range(0, t_size_of_seed[0], i_analysing_accuracy):
			for y in range(0, t_size_of_seed[1], i_analysing_accuracy):
				#if(im_lodead_seed[x,y] is not None):
				# calculate the block to add this pixels colour to the average of
				#i_x = int(math.floor(x/ia_step_sizes[cColage]))
				#i_y = int(math.floor(y/ia_step_sizes[cColage]))
				i_x = int(math.floor(x/i_block_size))
				i_y = int(math.floor(y/i_block_size))

				#print "insert into %i,%i: will go up to %i, divided by: %i" % (i_x, i_y, t_size_of_seed[1], i_block_size)

				t_rgb = im_lodead_seed[x,y]

				#print "RGB (%i,%i) : %i,%i,%i " % (i_x, i_y, t_rgb[0], t_rgb[1], t_rgb[2])
				
				miColourHolder[i_x, i_y, 0] = t_rgb[0] + miColourHolder[i_x, i_y, 0]
				miColourHolder[i_x, i_y, 1] = t_rgb[1] + miColourHolder[i_x, i_y, 1]
				miColourHolder[i_x, i_y, 2] = t_rgb[2] + miColourHolder[i_x, i_y, 2]
				miColourHolder[i_x, i_y, 3] = miColourHolder[i_x, i_y, 3] + 1

		#print "there are now %i blocks(%i,%i), and %i pixels" % (i_x * i_y, i_x, i_y, x * y)

		# calculate averages
		print "calculate averages"
		for x in range(ia_xy_steps[0]):
			for y in range(ia_xy_steps[1]):
				if miColourHolder[x,y,3] > 0:
					miColourHolder[x,y,0] = miColourHolder[x,y,0] / miColourHolder[x,y,3]
					miColourHolder[x,y,1] = miColourHolder[x,y,1] / miColourHolder[x,y,3]
					miColourHolder[x,y,2] = miColourHolder[x,y,2] / miColourHolder[x,y,3]
				else:
					miColourHolder[x,y,0] = miColourHolder[x,y,0]
					miColourHolder[x,y,1] = miColourHolder[x,y,1]
					miColourHolder[x,y,2] = miColourHolder[x,y,2]

		print "make collage"


		#print "will now make blocks from looked up images, with dimensions: %i in grid of (%i,%i)" % (i_block_size, ia_xy_steps[0], ia_xy_steps[1])

		# go through each block and find a matching picture
		for x in xrange(0, ia_xy_steps[0]):
			for y in xrange(0, ia_xy_steps[1]):
				# search for a picture in db which is closest to this colour range
				s_best_matching_image_path = s_get_path(cursor, miColourHolder[x,y,0], miColourHolder[x,y,1], miColourHolder[x,y,2])
				
				im_temp = Image.open(s_best_matching_image_path)
				i_shortest_side_of_temp = min(im_temp.size)
				im_temp = im_temp.crop((0,0,i_shortest_side_of_temp,i_shortest_side_of_temp))

				im_temp.thumbnail((i_block_size, i_block_size))

				im_new_colage.paste(im_temp, (x * i_block_size, y * i_block_size))
				#print "pasting %i,%i" % (x,y)
			print "completed line %i of %i" % (x,y)

		
		im_new_colage.save("out/collage"+str(ia_step_sizes[cColage])+".jpg")


	# after images have been made
	db.close()
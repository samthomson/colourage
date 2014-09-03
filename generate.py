import Image, ImageDraw
import os
import sys
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


	files = get_files('seed')
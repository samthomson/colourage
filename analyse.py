import Image, ImageDraw
import os
import sys
from os import listdir
from os.path import isfile, join
import sqlite3
 
def get_colors(infile, outfile = '', numcolors=1, swatchsize=20, resize=150):
 
    image = Image.open(infile)
    image = image.resize((resize, resize))
    result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
    result.putalpha(0)
    colors = result.getcolors(resize*resize)

    return colors[0][1]

def get_files(s_base_dir):
	fileList = []

	for root, subFolders, files in os.walk(s_base_dir):
	    for file in files:
			f = os.path.join(root,file)
			fileList.append(f)

	return fileList

 
if __name__ == '__main__':

	files = get_files('seed')

	i_files = len(files)
	i_block_size = 100


	print "%i files" % i_files

	# store in db
	db = sqlite3.connect('database')
	cursor = db.cursor()


	#for i in range(10):
	for i in range(i_files):
		if(files[i].endswith(('.jpg', '.JPG', '.jpeg', '.JPEG'))):
			t_color_tuple = get_colors(files[i])
			print "file %i/%i: %s; red: %i, green: %i, blue: %i" % (i, i_files, files[i], t_color_tuple[0], t_color_tuple[1], t_color_tuple[2])
			# store in db
			cursor.execute('''INSERT OR IGNORE INTO files(file, red, green, blue) VALUES(?,?,?,?)''', (files[i], t_color_tuple[0], t_color_tuple[1], t_color_tuple[2]))
			# load image into ram
			im_temp = Image.open(files[i])
			# find shortest side, to resize to square
			i_shortest_side_of_temp = min(im_temp.size)
			# ensure it's a square
			im_temp = im_temp.crop((0,0,i_shortest_side_of_temp,i_shortest_side_of_temp))
			# make a thumbnail, as per block size
			im_temp.thumbnail((i_block_size, i_block_size))
			im_temp.save("thumb/"+files[i].replace("/","-"));

	db.commit()
	db.close()

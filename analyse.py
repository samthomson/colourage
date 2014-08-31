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


	print "%i files" % i_files


	# store in db
	r.connect( "localhost").repl()

	r.db("colourage")


	if i_files > 10:
		for i in range(10):
			t_color_tuple = get_colors(files[i])
			#print "file: %s; red: %i, green: %i, blue: %i" % (files[i], t_color_tuple[0], t_color_tuple[1], t_color_tuple[2])
			r.db("colourage").table("seed_colours").insert([{"file": files[i], "red": t_color_tuple[0], "green": t_color_tuple[1], "blue": t_color_tuple[2]}]).run()

import Image, ImageDraw
import os
import sys
from os import listdir
from os.path import isfile, join
 
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


	if i_files > 10:
		for i in range(10):
			t_color_tuple = get_colors(files[i])
			print "red: %i, green: %i, blue: %i" % (t_color_tuple[0], t_color_tuple[1], t_color_tuple[2])

    #get_colors('seed/sudan.jpg', 'outfile.png', numcolors = 1)
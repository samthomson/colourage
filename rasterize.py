import Image, ImageDraw
import os
import sys
import math



def t_loosen(s_mode, t_colour, f_band_size):
	# divulge colours values to bands
	ia_colours = [0,0,0]

	for i in range(3):

		i_new_colour = math.floor(t_colour[i] / f_band_size) * f_band_size + (f_band_size/2)

		ia_colours[i] = int(i_new_colour)

	#value

	if s_mode == '1':
		value = int(shade >= 127) # Black-and-white (1-bit)
	elif s_mode == 'L':
		value = shade # Grayscale (Luminosity)
	elif s_mode == 'RGB':
		value = (ia_colours[0], ia_colours[1], ia_colours[2])
	elif s_mode == 'RGBA':
		value = (ia_colours[0], ia_colours[1], ia_colours[2], 255)
	elif s_mode == 'P':
		raise NotImplementedError("TODO: Look up nearest color in palette")
	else:
		raise ValueError("Unexpected mode for PNG image: %s" % im.mode)

	return value



if __name__ == '__main__':

	s_seed_image = "sam.JPG"

	im_seed = Image.open(s_seed_image)
	im_lodead_seed = im_seed.load()
	t_size_of_seed = im_seed.size
	s_im_mode = im_seed.mode

	ia_col_bits = [5,10,15,20,25]

	for b in range(len(ia_col_bits)):
		for x in range(t_size_of_seed[0]):
			for y in range(t_size_of_seed[1]):
				im_lodead_seed[x,y] = t_loosen(s_im_mode, im_lodead_seed[x,y], ia_col_bits[b])
				#print t_loosen(s_im_mode, im_lodead_seed[x,y])

		im_seed.save("out/out_" + str(b) + ".jpg")

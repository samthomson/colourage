colourage
=========

python image analyser gets colours then builds collage by doing an image search based on those colours to build a collage

written in python, uses sqlite to store an index of seed pictures, which it then generates a collage from, based on a supplied collage seed.

So basically put all your source seed pictures into 'seed' folder. 

Then run the analyse.py script. It will loop through all pictures and store the average RGB values into an sqlite instance.

Once the index is complete run generate.py to build a collage from based on the seed image and indexed seed folder pictures.

You can edit the generate.py script to change the supplied seed (the picture you want a collage made for), and also the 'resolution'.

Turn:

![Original image](wave.jpg)

into:

![collage](docs/r_16wave.jpg)

![collage](docs/r_32wave.jpg)

![collage](docs/r_64wave.jpg)

![collage](docs/r_128wave.jpg)

![collage](docs/r_256wave.jpg)

# Maze solving

## Prerequisites

Under Ubuntu just install a couple of python packages

	sudo apt-get install python-numpy python-networkx python-matplotlib python-imaging 

## Maze solving

For solving a maze it has to be encoded in a set of files defining horizontal and
vertical walls of the maze. To solve execute

	python maze_solve.py examples/simple
	python maze_solve.py examples/vetica

The latter one has the folloing solution:

![](https://github.com/proebrock/mazesolve/blob/master/examples/vetica_result.png)

## Extracting a maze from an image file

Provide the image of the maze as a PNG and in an upright and distortion-free
form. Convert the image to a maze description with

	python maze_extract.py examples/vetica

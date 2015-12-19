# Maze solving

## Prerequisites

	sudo apt-get install python-numpy python-networkx python-matplotlib python-imaging 

## Maze solving

	python maze_solve.py examples/simple
	python maze_solve.py examples/vetica

## Extracting a maze from an image file

Provide the image of the maze as a PNG and in an upright and distortion-free
form. Convert the image to a maze description with

	python maze_extract.py examples/vetica

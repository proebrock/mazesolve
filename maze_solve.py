import numpy as np
import matplotlib.pyplot as plt
import networkx as nx



class Maze:

	def __init__(self):
		self.height = None
		self.width = None
		self.v_walls = None
		self.h_walls = None
	
	def check(self):
		# Check vertical walls
		assert(len(self.v_walls) == self.height)
		for row in self.v_walls:
			assert(len(row) == self.width + 1)
			assert(row[0] == '1')
			assert(row[self.width] == '1')
			for c in row:
				assert(c == '0' or c == '1')
		# Check horizontal walls
		assert(len(self.h_walls) == self.height + 1)
		for row in self.h_walls:
			assert(len(row) == self.width)
			for c in row:
				assert(c == '0' or c == '1')
		assert(self.h_walls[0] == self.width * '1')
		assert(self.h_walls[self.height] == self.width * '1')
	
	def set(self, height, width, v_walls, h_walls):
		self.height = height
		self.width = width
		self.v_walls = v_walls
		self.h_walls = h_walls
		self.check()

	def load_from_file(self, basename):
		# Load vertical walls
		self.v_walls = []
		f = open(basename + '.v_walls', 'r')
		for line in f:
			self.v_walls.append(line.strip())
		f.close()
		# Load horizontal walls
		self.h_walls = []
		f = open(basename + '.h_walls', 'r')
		for line in f:
			self.h_walls.append(line.strip())
		f.close()
		# Guess height and width
		self.height = len(self.v_walls)
		self.width = len(self.v_walls[0]) - 1
		self.check()
	
	def plot(self, color):
		for i in range(self.height):
			for j in range(self.width):
				if self.v_walls[i][j] == '1':
					plt.plot([j, j], [i, i + 1], '-', color=color)
				if self.h_walls[i][j] == '1':
					plt.plot([j, j+1], [i, i], '-', color=color)
			if self.v_walls[i][self.width]:
				plt.plot([self.width, self.width], [i, i + 1], '-', color=color)
		for j in range(self.width):
			if self.h_walls[self.height][j] == '1':
				plt.plot([j, j + 1], [self.height, self.height], '-', color=color)
		plt.axis('equal')
		plt.xlim([-1, self.width + 1])
		plt.ylim([self.height + 1, -1])

	def get_graph(self):
		G = nx.Graph()
		G.add_nodes_from(range(self.height * self.width))
		for i in range(self.height):
			for j in range(self.width):
				if (self.v_walls[i][j] == '0'): # No left wall
					G.add_edge(self.width * i + j, self.width * i + (j-1))
				if (self.h_walls[i][j] == '0'): # No top wall
					G.add_edge(self.width * i + j, self.width * (i-1) + j)
		return G

	def plot_path(self, path, color):
		x = [ p % self.width + 0.5 for p in path ]
		y = [ p / self.width + 0.5 for p in path ]
		for i in range(len(path)-1):
			plt.arrow(x[i], y[i], x[i+1]-x[i], y[i+1]-y[i], color=color, \
				length_includes_head=True, head_width=0.1)

	def solve(self):
		m.plot('b')
		G = m.get_graph()
		path = nx.shortest_path(G, 0, 31)
		print(path)
		m.plot_path(path, 'r')
		plt.show()



m = Maze()
m.load_from_file('simple')
m.solve()

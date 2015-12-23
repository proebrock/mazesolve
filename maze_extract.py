from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import sys



if not len(sys.argv) == 2:
	print('Usage: {0} <basename of png file>'.format(sys.argv[0]))
	sys.exit()
basename = sys.argv[1]
verbose = True

im = Image.open(basename + '.png')
(width, height) = im.size
bwimage = im.convert('L')
bwpix = bwimage.load()

# Calulate average luminosity of rows and columns
rowsums = np.zeros(height)
colsums = np.zeros(width)
for x in range(width):
	for y in range(height):
		rowsums[y] += bwpix[x,y]
		colsums[x] += bwpix[x,y]
rowavrg = rowsums / width
colavrg = colsums / height

# Find array of minimums
def get_minimums(v, threshold):
	i0 = np.where(v < threshold)[0]
	d = np.where(np.diff(i0) != 1)[0]
	i1 = np.concatenate([np.zeros(1), d + 1])
	i2 = np.concatenate([d, [len(i0)-1]])
	return [ np.argmin(v[i0[i1[i]]:i0[i2[i]]+1]) + i0[i1[i]] for i in range(len(i1)) ]
row_thresh = 215.0
col_thresh = 215.0
row_min = get_minimums(rowavrg, row_thresh)
col_min = get_minimums(colavrg, col_thresh)
# Number of fields
height = len(row_min) - 1
width = len(col_min) - 1
# Size of sampling rectangles
sx = (int)(((np.round(np.mean(np.diff(col_min))) / 3.0) - 1) / 2.0)
sy = (int)(((np.round(np.mean(np.diff(row_min))) / 3.0) - 1) / 2.0)

# Plot average luminosity of rows and columns
if verbose:
	f, ax = plt.subplots(2)
	ax[0].set_title('Average luminosity of image')
	ax[0].plot(rowavrg)
	ax[0].axhline(row_thresh, color='r')
	for r in row_min:
		ax[0].axvline(r, color='g')
	ax[0].set_ylabel('Row Luminosity [0..255]')
	ax[0].set_ylim([0, 256])
	ax[1].plot(colavrg)
	ax[1].axhline(col_thresh, color='r')
	for c in col_min:
		ax[1].axvline(c, color='g')
	ax[1].set_xlabel('Pixel')
	ax[1].set_ylabel('Column Luminosity [0..255]')
	ax[1].set_ylim([0, 256])
	plt.show()

def rectangle_full(pix, cx, cy, dx, dy):
	threshold = 128
	mincount = ((2 * dx + 1) * (2 * dy + 1)) / 3
	count = 0
	for x in range(cx - dx, cx + dx + 1):
		for y in range(cy - dy, cy + dy + 1):
			if pix[x, y] < threshold:
				count += 1
	return count >= mincount

if verbose:
	def draw_rectangle(pix, cx, cy, dx, dy, color):
		for x in range(cx - dx, cx + dx + 1):
			pix[x, cy - dy] = color
			pix[x, cy + dy] = color
		for y in range(cy - dy, cy + dy + 1):
			pix[cx - dx, y] = color
			pix[cx + dx, y] = color
	cimage = im.convert('RGBA')
	cpix = cimage.load()
	# Plot grid points
	for y in row_min:
		for x in col_min:
			cpix[x, y] = (0, 0, 255, 255) # Blue
	# Plot sample areas for vertical walls
	for y in [ (row_min[i] + row_min[i+1]) / 2.0 for i in range(len(row_min)-1) ]:
		for x in col_min:
			if rectangle_full(bwpix, int(round(x)), int(round(y)), sx, sy):
				draw_rectangle(cpix, int(round(x)), int(round(y)), sx + 1, sy + 1, (255, 0, 0, 255)) # Red
			else:
				draw_rectangle(cpix, int(round(x)), int(round(y)), sx + 1, sy + 1, (0, 255, 0, 255)) # Green
	# Plot sample areas for horizontal walls
	for y in row_min:
		for x in [ (col_min[i] + col_min[i+1]) / 2.0 for i in range(len(col_min)-1) ]:
			if rectangle_full(bwpix, int(round(x)), int(round(y)), sx, sy):
				draw_rectangle(cpix, int(round(x)), int(round(y)), sx + 1, sy + 1, (255, 0, 0, 255)) # Red
			else:
				draw_rectangle(cpix, int(round(x)), int(round(y)), sx + 1, sy + 1, (0, 255, 0, 255)) # Green
	plt.imshow(cimage)
	plt.show()
	#cimage.save(basename + '_debug.png')

# Sample areas for vertical walls
f = open(basename + '.v_walls', 'w')
for y in [ (row_min[i] + row_min[i+1]) / 2.0 for i in range(len(row_min)-1) ]:
	line = ''
	for x in col_min:
		if rectangle_full(bwpix, int(round(x)), int(round(y)), sx, sy):
			line += '1'
		else:
			line += '0'
	f.write(line + '\n')
f.close()
# Sample areas for horizontal walls
f = open(basename + '.h_walls', 'w')
for y in row_min:
	line = ''
	for x in [ (col_min[i] + col_min[i+1]) / 2.0 for i in range(len(col_min)-1) ]:
		if rectangle_full(bwpix, int(round(x)), int(round(y)), sx, sy):
			line += '1'
		else:
			line += '0'
	f.write(line + '\n')
f.close()

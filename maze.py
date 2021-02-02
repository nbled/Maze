import tkinter
import random
import numpy

class Node:
	def __init__(self, pos, p, d=False, i=False):
		self.dead_end = d
		self.intersec = i
		self.position = pos
		self.linked = []
		self.parent = p

def get_random_cell(m, n):
	"""
		Return a random cell coordinates in the maze
	"""

	return (
		numpy.random.randint(0, m),
		numpy.random.randint(0, n)
	)

def generate_cases(m, n):
	"""
		Generate a matrices and affect an unique id
		to each cell
	"""

	mat = numpy.arange(m * n)
	return mat.reshape(m, n)

def generate_vertical_walls(m, n):
	"""
		Generate vertical walls
		Initially, all cells are separated by walls
	"""

	return numpy.ones((m - 1, n))

def generate_horizontal_walls(m, n):
	"""
		Generate vertical walls
		Initially, all cells are separated by walls
	"""

	return numpy.ones((m, n - 1))

def generate_maze(m, n):
	"""
		Generate a perfect maze (~ to a directed acyclic graph)
		using the random path merge algorithm
		Worst case performance: O(m^2 * n ^ 2)
	"""

	# Initial cells, each one have a different id
	cases = generate_cases(m, n)

	# Vertical & Hori
	vwalls = generate_vertical_walls(m, n)
	hwalls = generate_horizontal_walls(m, n)

	steps = 0
	while steps < (m * n) - 1:
		# Select a random cell
		x, y = get_random_cell(m, n)

		walls = None
		c = (0, 0)
	
		# We remove a vertical or an horizontal wall
		# between towo cases with a different id
		if x >= vwalls.shape[0] and y >= hwalls.shape[1]:
			continue
		elif x >= vwalls.shape[0]:
			walls = hwalls
			c = (cases[x][y], cases[x][y + 1])
		elif y >= hwalls.shape[1]:
			walls = vwalls
			c = (cases[x][y], cases[x + 1][y])
		else:
			choice = random.randint(0, 1)
			if choice == 0:
				walls = hwalls
				c = (cases[x][y], cases[x][y + 1])
			else:
				walls = vwalls
				c = (cases[x][y], cases[x + 1][y])

		if walls is None:
			continue
	
		# If this is the same id
		# continue
		if c[0] == c[1]:
			continue

		# Merge cases ids
		for i in range(cases.shape[0]):
			for j in range(cases.shape[1]):
				if cases[i][j] == c[1]:
					cases[i][j] = c[0]

		# Remove the wall
		walls[x][y] = 0

		steps += 1

	return (vwalls, hwalls)


def get_adjacent_cells(i, j, vwalls, hwalls):
	"""
		Return adjacent accessibles cells
		(no separation with a wall)
	"""

	adjacents = []
	if i > 0 and vwalls[i - 1][j] == 0:
		adjacents.append((i - 1, j))
	if j > 0 and hwalls[i][j - 1] == 0:
		adjacents.append((i, j - 1))
	if i < vwalls.shape[0] and vwalls[i][j] == 0:
		adjacents.append((i + 1, j))
	if j < hwalls.shape[1] and hwalls[i][j] == 0:
		adjacents.append((i, j + 1))
	return adjacents

def generate_graph(i, j, parent, vwalls, hwalls):
	"""
		Generate the DAG (directed acyclic graph)
		corresponding to the maze
	"""

	adjacents = get_adjacent_cells(i, j, vwalls, hwalls)
	dead_end, intersec = False, False

	if len(adjacents) == 1: dead_end = True
	elif len(adjacents) > 2: intersec = True

	head = Node((i, j), parent, dead_end, intersec)
	for cell in adjacents:
		if parent != None and parent.position == cell:
			continue
		head.linked.append(generate_graph(cell[0], cell[1], head, vwalls, hwalls))
	return head

def draw_maze(vwalls, hwalls, block=50):
	"""
		Draw maze (tkinter API)
	"""

	# Show initial and end point
	ix, iy = get_random_cell(WIDTH, HEIGHT)
	fx, fy = get_random_cell(WIDTH, HEIGHT)
	surface.create_rectangle(
		ix * block, iy * block, (ix + 1) * block, (iy + 1) * block, 
		fill="green", outline="green"
	)
	surface.create_rectangle(
		fx * block, fy * block, (fx + 1) * block, (fy + 1) * block, 
		fill="red", outline="red"
	)
	
	# Draw vertical walls
	for i in range(vwalls.shape[0]):
		for j in range(vwalls.shape[1]):
			if vwalls[i][j] == 1:
				o = ((i + 1) * block, j * block)
				surface.create_line(o[0], o[1], o[0], o[1] + block, width=2)

	# Draw horizontal walls
	for i in range(hwalls.shape[0]):
		for j in range(hwalls.shape[1]):
			if hwalls[i][j] == 1:
				o = (i * block, (j + 1) * block)
				surface.create_line(o[0], o[1], o[0] + block, o[1], width=2)

	# Generate and draw the maze's graph
	head = generate_graph(ix, iy, None, vwalls, hwalls)
	draw_graph_node(surface, head)

def draw_graph_node(surface, node):
	"""
		Draw the graph relationship
	"""

	# Source block position
	i, j = node.position
	x = i * BLOCK_SIZE + BLOCK_SIZE // 2
	y = j * BLOCK_SIZE + BLOCK_SIZE // 2

	# Show links by drawing a line
	# between each linked node
	for sub in node.linked:
		i2, j2 = sub.position
		x2 = i2 * BLOCK_SIZE + BLOCK_SIZE // 2
		y2 = j2 * BLOCK_SIZE + BLOCK_SIZE // 2
		surface.create_line(x, y, x2, y2)
		draw_graph_node(surface, sub)

	# Draw node
	if node.dead_end:
		surface.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")
	elif (not node.dead_end) and (not node.intersec):
		surface.create_oval(x - 3, y - 3, x + 3, y + 3, fill="white")
	else:
		surface.create_rectangle(x - 3, y - 3, x + 3, y + 3, fill="red")

def reload_maze(event):
	"""
		Regenerate full maze on mouse click
	"""

	surface.delete("all")
	maze = generate_maze(WIDTH, HEIGHT)
	draw_maze(maze[0], maze[1], block=BLOCK_SIZE)


# Maze parameters
BLOCK_SIZE = 25
WIDTH = 20
HEIGHT = 20

# Generate initial maze
v, h = generate_maze(WIDTH, HEIGHT)
print(get_adjacent_cells(2, 3, v, h))

# Configure window
window = tkinter.Tk()
window.title("Maze")
window.geometry(str(WIDTH * BLOCK_SIZE) + "x" + str(HEIGHT * BLOCK_SIZE))
window.resizable(False, False)
window.bind_all("<Button-1>", reload_maze)

# Configure drawing surface
surface = tkinter.Canvas(window, width=WIDTH * BLOCK_SIZE, height=HEIGHT * BLOCK_SIZE, bg="white")
surface.pack()

draw_maze(v, h, block=BLOCK_SIZE)
window.mainloop()

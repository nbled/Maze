import tkinter
import random
import numpy

def generate_cases(m, n):
	mat = numpy.arange(m * n)
	return mat.reshape(m, n)

def generate_vertical_walls(m, n):
	return numpy.ones((m - 1, n))

def generate_horizontal_walls(m, n):
	return numpy.ones((m, n - 1))

def generate_maze(m, n):
	cases = generate_cases(m, n)
	vwalls = generate_vertical_walls(m, n)
	hwalls = generate_horizontal_walls(m, n)

	steps = 0
	while steps < (m * n) - 1:
		x = random.randint(0, WIDTH - 1)
		y = random.randint(0, HEIGHT - 1)

		walls = None
		c = (0, 0)
	
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
	
		if c[0] == c[1]:
			continue

		for i in range(cases.shape[0]):
			for j in range(cases.shape[1]):
				if cases[i][j] == c[1]:
					cases[i][j] = c[0]
		walls[x][y] = 0

		steps += 1

	return (vwalls, hwalls)


def draw_maze(vwalls, hwalls, block=50):
	for i in range(vwalls.shape[0]):
		for j in range(vwalls.shape[1]):
			if vwalls[i][j] == 1:
				o = ((i + 1) * block, j * block)
				surface.create_line(o[0], o[1], o[0], o[1] + block)
	for i in range(hwalls.shape[0]):
		for j in range(hwalls.shape[1]):
			if hwalls[i][j] == 1:
				o = (i * block, (j + 1) * block)
				surface.create_line(o[0], o[1], o[0] + block, o[1])

def reload_maze(event):
	surface.delete("all")
	maze = generate_maze(WIDTH, HEIGHT)
	draw_maze(maze[0], maze[1], block=BLOCK_SIZE)


BLOCK_SIZE = 25
WIDTH = 15
HEIGHT = 15

v, h = generate_maze(WIDTH, HEIGHT)

window = tkinter.Tk()
window.geometry(str(WIDTH * BLOCK_SIZE) + "x" + str(HEIGHT * BLOCK_SIZE))
window.resizable(False, False)
window.bind_all("<Button-1>", reload_maze)

surface = tkinter.Canvas(window, width=WIDTH * BLOCK_SIZE, height=HEIGHT * BLOCK_SIZE, bg="white")
surface.pack()

draw_maze(v, h, block=BLOCK_SIZE)

window.mainloop()

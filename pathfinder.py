from tkinter import * 
import math
import random
import time

# creating canvas in tkinter
root = Tk()
canvas = Canvas(root, width=1001, height=1001, background='white')
canvas.pack()

# grid that can be changed anytime you want
x = 50
y = 50
grid = []

# adding the open and close lists for the algorithm and adding the START Node
start = (0, 0)
goal = (48, 36)
openList = []
closedList = []
path = []

class Spot():
	def __init__(self, i, j, color="white"):
		self.f = 0
		self.g = 0
		self.h = 0
		self.width = 20
		self.i = i
		self.j = j
		self.color = color
		self.previous = None
		self.obstacle = False
		self.diagonal = False
		self.rectangle = None
		self.neighbors = []
		if (start[0] == i and start[1] == j):
			self.color = "yellow"

		#pct = random.randint(0, 100)
		#if pct <= 30:
		#	self.color = "black"
		#	self.obstacle = True

	def __repr__(self):
		return "({}, {})".format(self.i, self.j)

	def isDiagonal(self):
		self.diagonal = True

	def addNeighbors(self, grid):
		# V and H
		if self.i - 1 > 0:
			self.neighbors.append(grid[self.i - 1][self.j])
		if self.i + 1 < x:
			self.neighbors.append(grid[self.i + 1][self.j])
		if self.j - 1 > 0:
			self.neighbors.append(grid[self.i][self.j - 1])
		if self.j + 1 < y:
			self.neighbors.append(grid[self.i][self.j + 1])

		# diagonals
		if self.i - 1 > 0 and self.j - 1 > 0:
			grid[self.i - 1][self.j - 1].isDiagonal()
			self.neighbors.append(grid[self.i - 1][self.j - 1])
		if self.i + 1 < x and self.j + 1 < y:
			grid[self.i + 1][self.j + 1].isDiagonal()
			self.neighbors.append(grid[self.i + 1][self.j + 1])
		if self.i - 1 > 0 and self.j + 1 < y:
			grid[self.i - 1][self.j + 1].isDiagonal()
			self.neighbors.append(grid[self.i - 1][self.j + 1])
		if self.i + 1 < x and self.j - 1 > 0:
			grid[self.i + 1][self.j - 1].isDiagonal()
			self.neighbors.append(grid[self.i + 1][self.j - 1])

	def draw(self):
		self.rectangle = canvas.create_rectangle(self.i*self.width+1, self.j*self.width+1, self.i*self.width+1 + self.width, self.j*self.width+1 + self.width, fill=self.color, outline="black")

def fillGrid():
	for i in range(x):
		column = []
		for j in range(y):
			square = Spot(i, j)
			column.append(square)
		grid.append(column)
	grid[start[0]][start[1]].obstacle = False
	grid[start[0]][start[1]].color = "yellow"
	grid[goal[0]][goal[1]].obstacle = False
	grid[goal[0]][goal[1]].color = "yellow"

	openList.append(grid[start[0]][start[1]])

def displayGrid():
	# i = column; j = row
	for i in range(x):
		for j in range(y):
			grid[i][j].draw()

def addAllNeighbors():
	for column in grid:
		for square in column:
			square.addNeighbors(grid)

def getSpotByPosition(spot):
	return (spot.i, spot.j)

def heuristic(p1, p2):
	return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

def doNothing(event):
	pass

def beginTheJourny(event):
	canvas.bind("<Button-1>", doNothing)
	canvas.bind("<Button-3>", doNothing)
	# continue while openList is not empty
	while(len(openList) > 0):

		# get the current Node
		current_node = openList[0]
		for square in openList:
			if square.f < current_node.f:
				current_node = square
		openList.remove(current_node)
		closedList.append(current_node)
		canvas.itemconfig(current_node.rectangle, fill="red")
		#time.sleep(0.01)
		root.update()
		"""for closed in closedList:
						canvas.itemconfig(closed.rectangle, fill="orange")
						root.update()"""
		# found the goal
		if current_node.i == goal[0] and current_node.j == goal[1]:
			print("FOUND THE GOAL")
			temp = current_node
			path.append(temp)
			while temp.previous:
				path.append(temp.previous)
				temp = temp.previous
			break

		# generate children
		for neighbor in current_node.neighbors:
			if neighbor in closedList or neighbor.obstacle:
				continue
			# adding my current G with 1 because that's the distance between squares (V and H, not vertical)
			if neighbor.isDiagonal:
				tentative_gScore = current_node.g + math.sqrt(2)
			else:
				tentative_gScore = current_node.g + 1
			
			if neighbor in openList:
				if tentative_gScore < neighbor.g:
					# this path is better than the current one
					neighbor.g = tentative_gScore
			else:
				neighbor.g = tentative_gScore
				openList.append(neighbor)
				canvas.itemconfig(neighbor.rectangle, fill="green")
				#time.sleep(0.001)
				root.update()
			
			neighbor.h = heuristic((neighbor.i, neighbor.j), goal)
			neighbor.f = neighbor.g + neighbor.h
			neighbor.previous = current_node
	for square in path:
		canvas.itemconfig(grid[square.i][square.j].rectangle, fill="blue")
		root.update()

def setWalls(event):
	x, y = int(event.x/20), int(event.y/20)
	# print("{}, {}".format(x, y))
	grid[x][y].obstacle = True
	canvas.itemconfig(grid[x][y].rectangle, fill="black")

fillGrid()
displayGrid()
addAllNeighbors()

canvas.bind("<Button-3>", setWalls)
canvas.bind("<Button-1>", beginTheJourny)

displayGrid()
root.mainloop()



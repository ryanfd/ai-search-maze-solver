#!/usr/bin/env python3
from random import randrange
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Rectangle
from matplotlib.patches import Rectangle
from pathlib import Path
# import numpy as np


class Cell(object):
    """ A cell in a maze
    """
    def __init__(self, loc, value, color):
        self.location = loc     # this is the same as the loc in the maze... need?
        self.value = value
        self.active = False
        self.color = color
        self.alpha = 0.4

class Maze:
    """ A maze is a 2-Dimensional grid of Cell objects.
    """
    def __init__(self):
        self.id = 1
        self.num_rows = 0
        self.num_cols = 0
        self.maze = None

    def GenerateMaze(self, filename):
        """ generate a maze from a binary obstacle grid
        """

        if not Path(filename).is_file():
            raise BaseException(filename + " not found.")
        
        # first line of maze instance: #rows #columns
        f = open(filename)
        line = f.readline()
        self.num_rows, self.num_cols = [int(x) for x in line.split(' ')]
        print("num_rows = ", str(self.num_rows), ", num_columns = ", str(self.num_cols))

        self.maze = []

        # generate maze of Cell objects
        for row in range(self.num_rows):
            line = f.readline()
            self.maze.append([])
            for col, value in enumerate(line):

                if value == "#":
                    self.maze[row].append(Cell([row, col], "#", "black"))
                elif value == ".":
                    self.maze[row].append(Cell([row, col], ".", "white"))
                elif value == "0" or value == "1":
                    self.maze[row].append(Cell([row, col], "A", "green"))
                # else value == " ":
                #     self.maze[row].append(Cell([row, col], " ", "white"))

        return self.maze


class Visualize():
    """ Visualize and animate a maze
    """

    def __init__(self, maze_obj):
        self.ax = None
        self.patches = []
        self.fig = None
        self.cell_width = 1
        self.maze_obj = maze_obj
        self.animation = None
        # self.maze_obj.maze = np.flip(np.transpose(self.maze_obj.maze), 1)

    def SetupFigure(self):
        """ setup the properties of the maze plot.
        """

        self.fig = plt.figure(figsize = (8, 8))

        # axes
        self.ax = plt.axes()
        plt.xlim([0, self.maze_obj.num_cols])
        plt.ylim([0, self.maze_obj.num_rows])

        # Set an equal aspect ratio
        self.ax.set_aspect("equal")

        # Remove the axes from the figure
        # self.ax.axes.get_xaxis().set_visible(False)
        # self.ax.axes.get_yaxis().set_visible(False)

        # animate figure
        self.animation = animation.FuncAnimation(self.fig, self.UpdateAnimation,
                                                 frames=100,
                                                 interval=100,
                                                 blit=True)

    def UpdateAnimation(self, frame):

        rand_row = randrange(self.maze_obj.num_rows)
        rand_col = randrange(self.maze_obj.num_cols)

        self.maze_obj.maze[rand_row][rand_col].color = "red"
        self.UpdateFigure()

        return self.patches

    def UpdateFigure(self):

        self.patches.clear()
        for i in range(self.maze_obj.num_rows):
            for j in range(self.maze_obj.num_cols):
                square = plt.Rectangle((j * self.cell_width, self.maze_obj.num_rows - (i * self.cell_width)), self.cell_width, self.cell_width, fc = self.maze_obj.maze[i][j].color, alpha = self.maze_obj.maze[i][j].alpha)
                self.patches.append(square)

        for p in self.patches:
            self.ax.add_patch(p)

    def ShowFigure(self):
        plt.show()


my_maze = Maze()
my_maze.GenerateMaze("maze_instances/maze2.txt")

v = Visualize(my_maze)
v.SetupFigure()
v.UpdateFigure()
v.ShowFigure()

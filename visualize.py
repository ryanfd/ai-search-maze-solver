#!/usr/bin/env python3
from random import randrange
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Rectangle
from matplotlib.patches import Rectangle
from pathlib import Path
# import numpy as np

# # every 2d coordinate in the figure is a Rectangle()
# # each Rectangle() is accessable by indexing the squares dictionary with the Rectangles coordinates
# # Therefore, the squares dictionary holds the rectangle objects
# # every 2d coordinate must be a matplotlib.patch, so that we can draw it on screen
# # we shall set each patch as a square, so that we can index the square by the coordinate to get the underlying Rectangle() for that coordinate
# for all squares in maze:
#     square = plt.Rectangle((j, i))
#     self.squares[(i, j)] = square
#     self.patches.append(self.ax.add_patch(self.squares[(i, j)]))

# # whenever we want to change a 2d coordinate on the plot, we use the setters/getters for the associated patch, which are actually squares, and since they are squares (which is a dictionary), the underlying Rectangle() is accessable
# self.squares[(2, 2)].set_facecolor("red")


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
        self.squares = None
        # self.maze_obj.maze = np.flip(np.transpose(self.maze_obj.maze), 1)

    # create the base frame upon which the animation takes place
    def initFrame(self):

        self.squares = dict()
        # {
        #     # key: square
        #     (0, 0): square_obj
        #     (0, 1): square_obj
        #     (0, 2): square_obj
        # }

        # initial maze: no solution paths
        for i in range(self.maze_obj.num_rows):
            for j in range(self.maze_obj.num_cols):
                square = plt.Rectangle((j * self.cell_width, self.maze_obj.num_rows - (i * self.cell_width)), self.cell_width, self.cell_width, fc = self.maze_obj.maze[i][j].color, alpha = self.maze_obj.maze[i][j].alpha)
                self.squares[(i, j)] = square
                self.patches.append(self.ax.add_patch(self.squares[(i, j)]))

        # must return self.patches, 
        # it tells the animator update the patches object on the plot after each frame

        # self.maze_obj.maze[2][2].color = "red"

        # self.squares[(2, 2)].set_facecolor("red")

        return self.patches


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
        # frames should equal length of solution path
        self.animation = FuncAnimation(self.fig, 
                                       self.UpdateAnimation,
                                       init_func=self.initFrame,
                                       frames=100,    # each frame of the animation
                                       interval=100,
                                       blit=True)

        self.ShowFigure()

    # updates animation every frame to show new maze figure
    def UpdateAnimation(self, frameNumber):

        print("updating...")

        rand_row = randrange(self.maze_obj.num_rows)
        rand_col = randrange(self.maze_obj.num_cols)

        # print("rand_row = ", str(rand_row), ", rand_col = ", str(rand_col))
        self.squares[(rand_row, rand_col)].set_facecolor("red")

        # must return self.patches, 
        # it tells the animaton framework to update the patches object on the plot
        return self.patches


    def ShowFigure(self):
        plt.show()


my_maze = Maze()
my_maze.GenerateMaze("maze_instances/maze2.txt")

animation = Visualize(my_maze)
animation.SetupFigure()
animation.ShowFigure()
# v.UpdateFigure()
# v.ShowFigure()

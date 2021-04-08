#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from pathlib import Path
from random import randrange
import argparse

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
        self.value = value      # the ascii value of the maze cell ('#', '.', '0', etc.)
        self.color = color      # face color of cell
        self.alpha = 0.4        # alpha of cell 
        self.active = False


class Maze:
    """ A maze is a 2-Dimensional grid of Cell objects.
    """
    def __init__(self):
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
        self.maze_obj = maze_obj
        self.ax = None
        self.fig = None
        self.patches = None
        self.cell_width = 1
        self.animation = None
        self.squares = None     # dict indexed by location to obtain underlying Rectangles

    # create the base frame upon which the animation takes place
    def initFrame(self):
        self.patches = []
        self.squares = dict()

        # initial maze: no solution paths
        for i in range(self.maze_obj.num_rows):
            for j in range(self.maze_obj.num_cols):

                # initial cell attributes
                cell_loc = (j * self.cell_width, self.maze_obj.num_rows - (i * self.cell_width + 1))
                cell_color = self.maze_obj.maze[i][j].color
                cell_alpha = self.maze_obj.maze[i][j].alpha

                # create patch
                self.squares[(i, j)] = plt.Rectangle((cell_loc), self.cell_width, self.cell_width, fc=cell_color, alpha=cell_alpha)
                self.patches.append(self.ax.add_patch(self.squares[(i, j)]))

        # must return self.patches, 
        # it tells the animator update the patches object on the plot after each frame
        return self.patches

        # self.maze_obj.maze[2][2].color = "red"
        # self.squares[(2, 2)].set_facecolor("red")

    def StartAnimation(self):
        """ initializes figure and begins the animation.
        """

        self.fig = plt.figure(figsize = (9, 9))

        # axes
        self.ax = plt.axes()
        plt.xlim([0, self.maze_obj.num_cols])
        plt.ylim([0, self.maze_obj.num_rows])

        # Set an equal aspect ratio
        self.ax.set_aspect("equal")

        # Remove the axes from the figure
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        # animate figure
        # frames should equal length of solution path
        self.animation = FuncAnimation(self.fig, 
                                       self.UpdateAnimation,
                                       init_func=self.initFrame,
                                       frames=100,    # each frame of the animation
                                       interval=100,  # should be adjustable in the end
                                       blit=True)

        self.ShowFigure()

    # updates animation every frame to show new maze figure
    def UpdateAnimation(self, frameNumber):

        rand_row = randrange(self.maze_obj.num_rows)
        rand_col = randrange(self.maze_obj.num_cols)

        self.squares[(rand_row, rand_col)].set_facecolor("red")

        # must return self.patches, 
        # it tells the animaton framework to update the patches object on the plot
        return self.patches


    def ShowFigure(self):
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("instance", help="the path to the maze instance")
    args = parser.parse_args()

    my_maze = Maze()
    my_maze.GenerateMaze(args.instance)

    animation = Visualize(my_maze)
    animation.StartAnimation()
    animation.ShowFigure()

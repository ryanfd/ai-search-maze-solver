#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
import matplotlib.colors as mcolors
from pathlib import Path
from random import randrange
import argparse


class Cell(object):
    """ A cell in a maze
    """
    def __init__(self, loc, value, color, alpha):
        self.location = loc     # this is the same as the loc in the maze... need?
        self.value = value      # the ascii value of the maze cell ('#', '.', '0', etc.)
        self.color = color      # face color of cell
        self.alpha = alpha        # alpha of cell 
        self.active = False


class Visualize(object):
    """ Visualize and animate a maze
    """

    def __init__(self, instance_path, start_pos, goal_pos, sol_path, exp_nodes):
        # maze related stuff
        self.maze_map = None
        self.maze_num_rows = 0
        self.maze_num_cols = 0
        self.maze_sol_path = sol_path
        self.maze_exp_nodes = exp_nodes
        self.squares = None     # dict indexed by location to obtain underlying Rectangles

        # figure related stuff
        self.ax = None
        self.fig = None
        self.patches = None             # maze components that do change (i.e. path)
        self.static_patches = None      # maze components that do not change (i.e. walls)
        self.cell_width = 1
        self.animation = None

        self.GenerateMaze(instance_path)

    def GenerateMaze(self, filename):
        """ generate a maze from a binary obstacle grid
        """

        if not Path(filename).is_file():
            raise BaseException(filename + " not found.")
        
        # first line of maze instance: #rows #columns
        f = open(filename)
        # line = f.readline()
        # self.maze_num_rows, self.maze_num_cols = [int(x) for x in line.split(' ')]
        # print("maze_num_rows = ", str(self.maze_num_rows), ", num_columns = ", str(self.maze_num_cols))

        # temporarly hardcoded for now
        self.maze_num_rows = 103
        self.maze_num_cols = 201
        self.maze_map = []

        # generate maze of Cell objects
        for row in range(self.maze_num_rows):
            line = f.readline()
            self.maze_map.append([])
            for col, value in enumerate(line):

                if value == "#":
                    self.maze_map[row].append(Cell([row, col], "#", "black", 0.5))
                elif value == ".":
                    self.maze_map[row].append(Cell([row, col], ".", "white", 0.9))
                elif value == "0" or value == "1":
                    self.maze_map[row].append(Cell([row, col], "A", "green", 0.9))
                # else value == " ":
                #     self.maze[row].append(Cell([row, col], " ", "white"))


    def StartAnimation(self):
        """ initializes figure and begins the animation.
        """

        # setup figure
        aspect = self.maze_num_cols / self.maze_num_rows
        self.fig = plt.figure(figsize = (6 * aspect, 6))

        # axes
        self.ax = plt.axes()
        plt.xlim([0, self.maze_num_cols])
        plt.ylim([0, self.maze_num_rows])

        # Set an equal aspect ratio
        self.ax.set_aspect("equal")

        # Remove the axes from the figure
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        self.static_patches = []
        self.patches = []
        self.squares = dict()

        # setup initial maze frame: no solution paths
        for i in range(self.maze_num_rows):
            for j in range(self.maze_num_cols):

                # initial cell attributes
                cell_loc = (j * self.cell_width, self.maze_num_rows - (i * self.cell_width + 1))
                cell_color = self.maze_map[i][j].color
                cell_alpha = self.maze_map[i][j].alpha

                # create rectangle
                self.squares[(i, j)] = plt.Rectangle((cell_loc), self.cell_width, self.cell_width, fc=cell_color, alpha=cell_alpha)

                
                # create patch out of rectangle
                if self.maze_map[i][j].value == ".":
                    self.patches.append(self.ax.add_patch(self.squares[(i, j)]))
                else:
                    self.static_patches.append(self.ax.add_patch(self.squares[(i, j)]))

        # animate figure
        self.animation = FuncAnimation(self.fig, 
                                       self.UpdateAnimation,
                                       frames=len(self.maze_sol_path),
                                       interval=200,  # should be adjustable in the end
                                       blit=True)

        self.ShowFigure()

    # updates animation every frame to show new maze figure
    def UpdateAnimation(self, frameNumber):

        # keep popping nodes from exp_nodes list until it pops one that is in the sol_path
        while True:
            exp_row, exp_col = self.maze_exp_nodes.pop(0)
            self.squares[(exp_row, exp_col + 1)].set_facecolor("red")

            if (exp_row, exp_col) in self.maze_sol_path:
                row, col = self.maze_sol_path.pop(0)
                self.squares[(row, col + 1)].set_facecolor("green")
                break;

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

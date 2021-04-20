#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
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
        self.map_size = 0
        self.maze_sol_path = sol_path
        self.maze_exp_nodes = exp_nodes
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.squares = None     # dict indexed by location to obtain underlying Rectangles

        # figure related stuff
        self.ax = None
        self.fig = None
        self.patches = None             # maze components that do change (i.e. path)
        self.cell_width = 1
        self.maze_colors = None
        self.animation = None
        self.pop_count = 0
        self.map_percentage = 0
        self.iteration = 0

        self.GenerateMaze(instance_path)

    def GenerateMaze(self, filename):
        """ generate a maze from a binary obstacle grid
        """

        if not Path(filename).is_file():
            raise BaseException(filename + " not found.")
        
        # colors for each part of maze
        self.maze_colors = { "wall": "black", "path": "white", "sg": "blue", "exp_nodes": "red", "sol_path": "green" }

        f = open(filename)
        self.maze_num_rows = len([line.strip("\n") for line in f if line != "\n"])
        f.seek(0)
        self.maze_map = []

        # generate maze of Cell objects
        for row in range(self.maze_num_rows):
            line = f.readline()
            self.maze_map.append([])
            for col, value in enumerate(line):
                if value == "#":
                    self.maze_map[row].append(Cell([row, col], "#", self.maze_colors["wall"], 0.7))
                elif value == ".":
                    self.maze_map[row].append(Cell([row, col], ".", self.maze_colors["path"], 0.7))
                    self.map_size += 1
                elif value == "0" or value == "1":
                    self.maze_map[row].append(Cell([row, col], "A", self.maze_colors["sg"], 0.9))
                    self.map_size += 1
                # else value == " ":
                #     self.maze[row].append(Cell([row, col], " ", "white"))

            self.maze_num_cols = (col // 2) + 1

        f.close()


    def StartAnimation(self):
        """ initializes figure and begins the animation.
        """

        # setup figure
        aspect = self.maze_num_cols / self.maze_num_rows
        self.fig = plt.figure(figsize = (7 * aspect, 7))

        self.fig.subplots_adjust(left=0.001)

        # axes
        self.ax = plt.axes()
        plt.xlim([0, self.maze_num_cols]) 
        plt.ylim([0, self.maze_num_rows])

        # Set an equal aspect ratio
        self.ax.set_aspect("equal")

        # Remove the axes from the figure
        self.ax.axes.get_xaxis().set_visible(False)
        self.ax.axes.get_yaxis().set_visible(False)

        self.patches = []
        self.squares = dict()

        # setup initial legend
        sg_squares = mpatches.Patch(color=self.maze_colors["sg"], label='start and goal')
        exp_nodes_squares = mpatches.Patch(color=self.maze_colors["exp_nodes"], label='expanded nodes')
        sol_path_squares = mpatches.Patch(color=self.maze_colors["sol_path"], label='solution path')
        exp_nodes_p = mpatches.Patch(color=self.maze_colors["exp_nodes"], label='{}% map expanded'.format(round(self.map_percentage, 0)))
        plt.legend(handles=[sg_squares, sol_path_squares, exp_nodes_squares, exp_nodes_p], loc='center left', bbox_to_anchor=(1.01, 0.5))

        # setup title
        title_str = "Depth-First Search"
        plt.title(label=title_str, fontsize=18, loc='center')
        self.t1 = self.fig.text(0.25, 0.05, "iteration #0", ha='center')
        self.t2 = self.fig.text(0.75, 0.05, "nodes expanded: {}".format(self.pop_count), ha='center')

        # don't cover start and goal locations with sol_path or exp_nodes
        self.maze_sol_path.pop(0)
        if tuple(self.start_pos) in self.maze_exp_nodes:
            self.maze_exp_nodes.remove(tuple(self.start_pos))
            
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
                if (i, j) in self.maze_exp_nodes:
                    self.patches.append(self.ax.add_patch(self.squares[(i, j)]))
                else:
                    self.ax.add_patch(self.squares[(i, j)])

        self.squares[(-1, -1)] = plt.text(0, 0, "")
        self.patches.append(self.squares[(-1, -1)])
        
        # animate figure
        self.animation = FuncAnimation(self.fig, 
                                       self.UpdateAnimation,
                                       frames=len(self.maze_sol_path),
                                       repeat=False,
                                       interval=200)  # should be adjustable in the end
                                       # blit=True)

        self.ShowFigure()

    # updates animation every frame to show new maze figure
    def UpdateAnimation(self, frameNumber):

        # keep popping nodes from exp_nodes list until it pops one that is in the sol_path
        while True:
            try:
                exp_nodes_entry = self.maze_exp_nodes.pop(0)
                self.pop_count += 1
            except IndexError:
                self.animation.event_source.stop()

            self.map_percentage = (self.pop_count / self.map_size) * 100
            if exp_nodes_entry != tuple(self.start_pos) and exp_nodes_entry != tuple(self.goal_pos):
                self.squares[exp_nodes_entry].set_facecolor("red")

            if exp_nodes_entry in self.maze_sol_path:
                row, col = self.maze_sol_path.pop(0)
                self.squares[(row, col)].set_facecolor("green")
                break;

        # update legend
        sg_squares = mpatches.Patch(color=self.maze_colors["sg"], label='start and goal')
        exp_nodes_squares = mpatches.Patch(color=self.maze_colors["exp_nodes"], label='expanded nodes')
        sol_path_squares = mpatches.Patch(color=self.maze_colors["sol_path"], label='solution path')
        exp_nodes_p = mpatches.Patch(color=self.maze_colors["exp_nodes"], label='{}% map expanded'.format(round(self.map_percentage, 0)))
        plt.legend(handles=[sg_squares, exp_nodes_squares, sol_path_squares, exp_nodes_p], loc='center left', bbox_to_anchor=(1.01, 0.5))
        self.iteration = self.iteration + 1

        # update bottom title
        self.t1.set_text("iteration #{}".format(self.iteration))
        self.t2.set_text("nodes expanded: {}".format(self.pop_count))

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

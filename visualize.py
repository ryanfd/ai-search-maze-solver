#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib import animation
from pathlib import Path

class Maze:
    """ A maze is a 2-Dimensional grid of Cell objects.
    """
    def __init__(self):
        self.id = 1
        self.maze = None

    def GenerateMaze(self, filename):
        """ generate a maze from a binary obstacle grid
        """

        if not Path(filename).is_file():
            raise BaseException(filename + " not found.")
        
        # first line of maze instance: #rows #columns
        f = open(filename)
        line = f.readline()
        num_rows, num_columns = [int(x) for x in line.split(' ')]
        print("num_rows = ", str(num_rows), ", num_columns = ", str(num_columns))

        self.maze = []

        # generate maze of Cell objects
        for i in range(num_rows):
            line = f.readline()
            for c in line:
                self.maze.append([])
                if c == "#":
                    self.maze[-1].append(Cell("#"))
                elif c == ".":
                    self.maze[-1].append(Cell("."))

        # print(self.maze)


class Cell(object):
    """ A cell in a maze
    """
    def __init__(self, value):
        self.value = value

class Visualize(object):
    """ Visualize and animate a maze
    """
    def __init__(self):
        pass

    def SetupPlot(self):
        """ setup the properties of the maze plot.
        """

        # # aspect = len(self.my_map) / len(self.my_map[0])
        # aspect = 10
        # self.fig = plt.figure(figsize=(4 * aspect, 4))

        # # figure title
        # title_box = self.ax.text(0, self.maze.num_rows + self.cell_size + 0.1,

        # self.animation = animation.FuncAnimation(self.fig, self.animate_func, frames=int(self.T + 1) * 10, interval=100, blit=True)
        pass


maze = Maze()
maze.GenerateMaze("maze_instances/maze1.txt")






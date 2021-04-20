import agentBase
import visualize
import numpy as np
import heapq
import math

# required for animation. Put this wherever you want
expanded_nodes = []

def random_forest(agent):
    pass

def main():

    maze_instance = ("maze_instances/maze1.txt") 
    algorithm = "a_star algorithm"

    my_map = agentBase.Map(maze_instance)
    my_map.getMap()
    agent = agentBase.Agent(my_map)

    random_forest(agent)
    
    #sol_path, exp_nodes = random_forest(agent)
    #animation = visualize.Visualize(algorithm, maze_instance, my_map.start, my_map.goal, sol_path, exp_nodes)

    #animation.StartAnimation()


if __name__ == '__main__':
    main()

import agentBase
import visualize
import numpy as np
import heapq
import math

# required for animation. Put this wherever you want
expanded_nodes = []

"""
push_node from mapf project
"""
def push_node(curr_list, node):
    heapq.heappush(curr_list, (node['g_val'] + node['h_val'], node['h_val'], node['loc'], node))

"""
pop_node from mapf project
"""
def pop_node(curr_list):
    _, _, _, curr = heapq.heappop(curr_list)
    return curr

"""
get_path from mapf project
"""
def get_path(node):
    path = []
    curr = node
    while curr is not None:
        path.append(curr['loc'])
        curr = curr['parent']
    path.reverse()
    print("LENGTH:", len(path))
    return path


"""
Straight Line Heuristic

@author: Ryan Donnelly
"""
def straight_line_heursitic(current_pos, goal_pos):
    """
    c^2 = a^2 + b^2
    c   = sqrt((x1-x2)^2 + (y1-y2)^2)
    """
    return math.sqrt((goal_pos[0] - current_pos[0])**2 + (goal_pos[1] - current_pos[1])**2)

"""
Dept-First Search
Pseudocode: https://en.wikipedia.org/wiki/Depth-first_search#Pseudocode

@author: Ryan Donnelly
"""
def depth_first_search(self):
    expanded_nodes.clear()

    # convert from numpy to regulat list, heappush has problems with numpy
    start_pos = (self.start[0], self.start[1])
    goal_pos = (self.goal[0], self.goal[1])
    current_pos = start_pos

    # initialization
    print("\nCoordinate Configuration: (Y, X)")
    print("Start State:", start_pos)
    print("Goal State:", goal_pos, "\n")

    open_stack = []
    closed_list = dict()
    root = {'loc': start_pos, 'parent': None}
    open_stack.append(root)
    closed_list[(root['loc'])] = root

    nodes_expanded = 0
    max_size_of_open = len(open_stack)
    while len(open_stack) > 0:
        nodes_expanded += 1 # time complexity
        if len(open_stack) > max_size_of_open: # space complexity
            max_size_of_open = len(open_stack)

        node = open_stack.pop() # LIFO
        expanded_nodes.append(node['loc'])
        current_pos = node['loc']
        self.current[0] = current_pos[0]
        self.current[1] = current_pos[1]

        # path to goal state has been found
        if current_pos == goal_pos:
            print("SOLUTION FOUND:")
            print("NODES EXPANDED:", nodes_expanded)
            print("MAX SIZE OF OPEN_LIST:", max_size_of_open)
            return get_path(node), expanded_nodes

        # take movement option indices in agentBase.nextStep()...
        # map out viable indices to locations in map
        move_options = self.nextStep()
        move_list = []
        for i in range(len(move_options)):
            if move_options[i] == 1:
                move_list.append((node['loc'][0], node['loc'][1]+1))
            if move_options[i] == 2:
                move_list.append((node['loc'][0]+1, node['loc'][1]))
            if move_options[i] == 3:
                move_list.append((node['loc'][0], node['loc'][1]-1))
            if move_options[i] == 4: 
                move_list.append((node['loc'][0]-1, node['loc'][1]))
        # end of for in loop

        # for valid locations, create movement child
        for move in move_list:
            child = {'loc': move,
                    'parent': node}
            if not (child['loc']) in closed_list: # pruning
                closed_list[(child['loc'])] = child
                open_stack.append(child)
        # end of for in loop
    # end of while loop

    return None

"""
Breadth-First Search
Pseudocode: https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode

@author: Ryan Donnelly
"""
def breadth_first_search(self):
    expanded_nodes.clear()

    # convert from numpy to regulat list, heappush has problems with numpy
    start_pos = (self.start[0], self.start[1])
    goal_pos = (self.goal[0], self.goal[1])
    current_pos = start_pos

    # initialization
    print("\nCoordinate Configuration: (Y, X)")
    print("Start State:", start_pos)
    print("Goal State:", goal_pos, "\n")

    open_list = []
    closed_list = dict()
    root = {'loc': start_pos, 'parent': None}
    open_list.append(root)
    closed_list[(root['loc'])] = root

    nodes_expanded = 0
    max_size_of_open = len(open_list)
    while len(open_list) > 0:
        nodes_expanded += 1 # time complexity
        if len(open_list) > max_size_of_open: # space complexity
            max_size_of_open = len(open_list)

        node = open_list.pop(0) # FIFO
        expanded_nodes.append(node['loc'])
        current_pos = node['loc']
        self.current[0] = current_pos[0]
        self.current[1] = current_pos[1]

        # path to goal state has been found
        if current_pos == goal_pos:
            print("SOLUTION FOUND:")
            print("NODES EXPANDED:", nodes_expanded)
            print("MAX SIZE OF OPEN_LIST:", max_size_of_open)
            return get_path(node), expanded_nodes

        # take movement option indices in agentBase.nextStep()...
        # map out viable indices to locations in map
        move_options = self.nextStep()
        move_list = []
        for i in range(len(move_options)):
            if move_options[i] == 1:
                move_list.append((node['loc'][0], node['loc'][1]+1))
            if move_options[i] == 2:
                move_list.append((node['loc'][0]+1, node['loc'][1]))
            if move_options[i] == 3:
                move_list.append((node['loc'][0], node['loc'][1]-1))
            if move_options[i] == 4: 
                move_list.append((node['loc'][0]-1, node['loc'][1]))
        # end of for in loop

        # for valid locations, create movement child
        for move in move_list:
            child = {'loc': move,
                    'parent': node}
            if not (child['loc']) in closed_list: # pruning
                closed_list[(child['loc'])] = child
                open_list.append(child)
        # end of for in loop
    # end of while loop

        


"""
A* Search
Pseudocode: https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

@author: Ryan Donnelly
"""

def a_star_search(self, h):
    """
    h               - chosen heuristic
    self.map        - maze to solve
    self.start      - agent starting goal
    self.goal       - agent end goal
    self.current    - agents current position
    """

    expanded_nodes.clear()

    # convert from numpy to regulat list, heappush has problems with numpy
    start_pos = (self.start[0], self.start[1])
    goal_pos = (self.goal[0], self.goal[1])
    current_pos = start_pos

    # initialization
    print("\nCoordinate Configuration: (Y, X)")
    print("Start State:", start_pos)
    print("Goal State:", goal_pos, "\n")

    open_list = []
    closed_list = dict()
    root = {'loc': start_pos, 'g_val': 0, 'h_val': h(start_pos, goal_pos), 'parent': None}
    push_node(open_list, root)
    closed_list[(root['loc'])] = root

    nodes_expanded = 0
    max_size_of_open = len(open_list)
    while len(open_list) > 0:
        nodes_expanded += 1 # time complexity
        if len(open_list) > max_size_of_open: # space complexity
            max_size_of_open = len(open_list)

        node = pop_node(open_list)
        expanded_nodes.append(node['loc'])
        current_pos = node['loc']
        self.current[0] = current_pos[0]
        self.current[1] = current_pos[1]

        # path to goal state has been found
        if current_pos == goal_pos:
            print("SOLUTION FOUND:")
            print("NODES EXPANDED:", nodes_expanded)
            print("MAX SIZE OF OPEN_LIST:", max_size_of_open)
            return get_path(node), expanded_nodes

        # take movement option indices in agentBase.nextStep()...
        # map out viable indices to locations in map
        move_options = self.nextStep()
        move_list =[]
        
        for i in range(len(move_options)):
            if move_options[i] == 1:
                move_list.append((node['loc'][0], node['loc'][1]+1))
            if move_options[i] == 2:
                move_list.append((node['loc'][0]+1, node['loc'][1]))
            if move_options[i] == 3:
                move_list.append((node['loc'][0], node['loc'][1]-1))
            if move_options[i] == 4: 
                move_list.append((node['loc'][0]-1, node['loc'][1]))
        # end of for in loop

        # for valid locations, create movement child
        for move in move_list:
            child = {'loc': move,
                    'g_val': node['g_val'] + 1,
                    'h_val': h(move, goal_pos),
                    'parent': node}
            if not (child['loc']) in closed_list: # pruning
                closed_list[(child['loc'])] = child
                push_node(open_list, child)
        # end of for in loop

    # end of while
    return None  # Failed to find solutions



def main():

    maze_instance = ("maze_instances/maze1.txt") 
    algorithm = "a_star algorithm"

    my_map = agentBase.Map(maze_instance)
    my_map.getMap()
    agent = agentBase.Agent(my_map)

    sol_path, exp_nodes = a_star_search(agent, straight_line_heursitic)
    animation = visualize.Visualize(algorithm, maze_instance, my_map.start, my_map.goal, sol_path, exp_nodes)
    animation.StartAnimation()


if __name__ == '__main__':
    main()

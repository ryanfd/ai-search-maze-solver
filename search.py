import agentBase
import visualize
import numpy as np
import heapq
import math
import time

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
Manhattan Distance Heuristic

@author: Ryan Donnelly
"""
def manhattan_distance_heuristic(current_pos, goal_pos):
    return abs(goal_pos[0] - current_pos[0]) + abs(goal_pos[1] - current_pos[1])

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

"""
IDA* Search
Pseudocode: https://en.wikipedia.org/wiki/Iterative_deepening_A*#Pseudocode

@author: Ryan Donnelly
"""
def ida_star(self, h):
    """
    h               - chosen heuristic
    self.map        - maze to solve
    self.start      - agent starting goal
    self.goal       - agent end goal
    self.current    - agents current position
    """

    # convert from numpy to regulat list, heappush has problems with numpy
    start_pos = (self.start[0], self.start[1])
    goal_pos = (self.goal[0], self.goal[1])
    current_pos = start_pos

    # initialization
    print("\nCoordinate Configuration: (Y, X)")
    print("Start State:", start_pos)
    print("Goal State:", goal_pos, "\n")

    dist = h(start_pos, goal_pos)
    result = dist
    nodes_expanded_list = []
    max_size_of_open_list = []
    total_time_complexity = 0
    total_space_complexity = 0

    while True:
        open_list = []
        closed_list = dict()
        root = {'loc': start_pos, 'g_val': 0, 'h_val': h(start_pos, goal_pos), 'parent': None}
        push_node(open_list, root)
        closed_list[(root['loc'])] = root

        # returns int if solution not found, path if found
        result = ida_star_helper(self, open_list, goal_pos, result, closed_list, h, nodes_expanded_list, max_size_of_open_list)

        if isinstance(result, np.int64) or isinstance(result, float):
            total_time_complexity += nodes_expanded_list.pop() # add together expanded nodes through multiple calls of search helper
            if total_space_complexity < max_size_of_open_list[0]:
                total_space_complexity = max_size_of_open_list.pop()
            if result == -1:
                return None
        else:
            print("SOLUTION FOUND:")
            print("NODES EXPANDED:", total_time_complexity)
            print("MAX SIZE OF OPEN_LIST:", total_space_complexity)
            return get_path(result)


"""
IDA* Search Helper
Pseudocode: https://en.wikipedia.org/wiki/Iterative_deepening_A*#Pseudocode

@author: Ryan Donnelly
"""
def ida_star_helper(self, open_list, goal_pos, bound, closed_list, h, nodes_expanded_list, max_size_of_open_list):
    nodes_expanded = 0
    max_size_of_open = 0
    curr_dist = -1

    while len(open_list) > 0:
        nodes_expanded += 1 # time complexity
        if len(open_list) > max_size_of_open: # space complexity
            max_size_of_open = len(open_list)
        
        node = pop_node(open_list)
        current_pos = node['loc']
        self.current[0] = current_pos[0]
        self.current[1] = current_pos[1]

        # path to goal state has been found
        if current_pos == goal_pos:
            return node

        if node['g_val']+node['h_val'] > bound:
            if curr_dist != -1 and node['g_val']+node['h_val'] < curr_dist:
                curr_dist = node['g_val']+node['h_val']
            elif curr_dist == -1:
                curr_dist = node['g_val']+node['h_val']
            continue

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
    # end of while loop

    # tracking total space + time complexity
    nodes_expanded_list.append(nodes_expanded)
    max_size_of_open_list.append(max_size_of_open)

    return curr_dist


def main():

    # modify these lines to change algorithm or change maze instance
    search_algorithm = a_star_search
    maze_instance = ("maze_instances/start_far_from_goal.txt") 

    my_map = agentBase.Map(maze_instance)
    my_map.getMap()
    agent = agentBase.Agent(my_map)

    # run search
    start_time = time.time()

    sol_path, exp_nodes = search_algorithm(agent, straight_line_heursitic)
    # print(ida_star(agent, manhattan_distance_heuristic))
    print("--- %s seconds ---" % (time.time() - start_time))

    # run animation for search
    animation = visualize.Visualize(search_algorithm.__name__, maze_instance, my_map.start, my_map.goal, sol_path, exp_nodes)
    animation.StartAnimation()


if __name__ == '__main__':
    main()

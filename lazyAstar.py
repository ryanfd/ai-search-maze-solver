import agentBase
import visualize
import search
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
Helper class for A* search implementing the queue
Put method takes a function to compare elements
"""
class PQueue:
    def __init__(self):
        self.elements = list()
        self.size = 0
    
    def empty(self):
        return self.size == 0
    
    def put(self, x, compare):
        flag = True
        for a in range(len(self.elements)):
            """
            If new element have bigger priority than one of the existing ones,new element would be put in place, all less important elements would be shifted to the  right
            """
            if compare(self.elements[a],x):
                self.elements.insert(a,x)
                flag = False
        
        if flag:
            self.elements.append(x)
    
    def get(self):
        return self.elements.pop(0)




"""
Manhattan heruristics returns sum of absolute vlaue of difference in coordinates of corresponding axis
"""
def manhattan_heuristics(current_pos, goal_pos):
    return abs((current_pos[0] - goal_pos[0])) + abs((current_pos[1] - goal_pos[1]))

def compare_lazyA(iteratingEl, x):
    if (iteratingEl['g_val'] > x['g_val']):
        return True
    return False


"""
Lazy A*
Takes the agent and heuristics function
Heuristic function takes current position and goal position

Returns paths and expanded nodes
"""
def lazy_a_star(agent):
    """
    h                - chosen heuristic
    agent.map        - maze to solve
    agent.start      - agent starting goal
    agent.goal       - agent end goal
    agent.current    - agents current position
    """
    h1 = manhattan_heuristics
    h2 = search.straight_line_heursitic
    expanded_nodes.clear()

    # convert from numpy to regulat list, heappush has problems with numpy
    start_pos = (agent.start[0], agent.start[1])
    goal_pos = (agent.goal[0], agent.goal[1])
    current_pos = start_pos

    # initialization
    print("\nCoordinate Configuration: (Y, X)")
    print("Start State:", start_pos)
    print("Goal State:", goal_pos, "\n")

    open_list = PQueue()
    closed_list = dict()
    root = {'loc': start_pos, 'g_val': 0,'h2_applied': False, 'h_val': h1(start_pos, goal_pos), 'parent': None}
    
    open_list.put(root, compare_lazyA)
    #push_node(open_list, root)
    closed_list[(root['loc'])] = root

    nodes_expanded = 0
    max_size_of_open = len(open_list.elements)
    while len(open_list.elements) > 0:
        nodes_expanded += 1 # time complexity
        if len(open_list.elements) > max_size_of_open: # space complexity
            max_size_of_open = len(open_list.elements)

        node = open_list.get()   #pop_node(open_list)
            
        
        expanded_nodes.append(node['loc'])
        current_pos = node['loc']
        agent.current[0] = current_pos[0]
        agent.current[1] = current_pos[1]

        # path to goal state has been found
        if (node['loc'][0] == agent.goal[0] and node['loc'][1] == agent.goal[1]):
            print("SOLUTION FOUND!")
            print("NODES EXPANDED:", nodes_expanded)
            print("MAX SIZE OF OPEN_LIST:", max_size_of_open)
            return get_path(node), expanded_nodes
        
        if node['h2_applied'] == False:
            if h1(node['loc'], goal_pos) < h2(node['loc'], goal_pos):
                node['h_val'] = h2(node['loc'], goal_pos)
            node['h2_applied'] = True
            open_list.put(node, compare_lazyA)
        else:
        
            # take movement option indices in agentBase.nextStep()...
            # map out viable indices to locations in map
            move_options = agent.nextStep()
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
                        'h2_applied': False,
                        'g_val': node['g_val'] + 1,
                        'h_val': h1(move, goal_pos),
                        'parent': node}
                if not (child['loc']) in closed_list: # pruning
                    
                    
                    closed_list[(child['loc'])] = child
                    #push_node(open_list, child)
                    open_list.put(child, compare_lazyA)
            # end of for in loop

    # end of while
    return None  # Failed to find solutions



def main():

    maze_instance = ("maze_instances/start_close_to_goal.txt") 

    my_map = agentBase.Map(maze_instance)
    my_map.getMap()
    start_loc = my_map.start.copy()
    goal_loc = my_map.goal.copy()
    agent = agentBase.Agent(my_map)

    sol_path, exp_nodes = lazy_a_star(agent)
    animation = visualize.Visualize(maze_instance, start_loc, goal_loc, sol_path, exp_nodes)
    animation.StartAnimation()


if __name__ == '__main__':
    main()




""" A*

Coordinate Configuration: (Y, X)
Start State: (2, 1)
Goal State: (18, 26) 

SOLUTION FOUND:
NODES EXPANDED: 138
MAX SIZE OF OPEN_LIST: 8
LENGTH: 56

"""

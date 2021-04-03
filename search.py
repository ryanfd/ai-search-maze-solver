import agentBase
import heapq
import math

"""
push_node from mapf project
"""
def push_node(curr_list, node):
    heapq.heappush(curr_list, (node['g_val'] + node['h_val'], node['h_val'], node['loc'], node))

"""
pop_node from mapf project
"""
def pop_node(open_list):
    _, _, _, curr = heapq.heappop(open_list)
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
    return path


"""
Straight Line Heuristic

@autho: Ryan Donnelly
"""
def straight_line_heursitic(current_pos, goal_pos):
    """
    c^2 = a^2 + b^2
    c = sqrt((x1-x2)^2 + (y1-y2)^2)
    """
    return math.sqrt((goal_pos[0] - current_pos[0])**2 + (goal_pos[1] - current_pos[1])**2)

"""
A* Search
Pseudocode: https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

@author: Ryan Donnelly
"""

def a_star_search(self, h):
    """
    h - chosen heuristic
    self.map        - maze to solve
    self.start      - agent starting goal
    self.goal       - agent end goal
    self.current    - agents current position
    """

    open_list = []
    root = {'loc': self.start, 'g_val': 0, 'h_val': h(self.start, self.goal), 'parent': None}
    goal_state = self.goal
    push_node(open_list, root)
    # closed_list = dict()
    # closed_list[(root['loc'])] = root
    print("length:", open_list)

    while len(open_list) > 0:
        node = pop_node(open_list)
        print("curr loc:", node['loc'])

        # path to goal state has been found
        if node['loc'][0] == self.goal[0] and node['loc'][1] == self.goal[1]:
            print("PATH FOUND:")
            return get_path(node)

        move_options = self.nextStep()
        print("loc", move_options)
        # for move in move_options:
        #     child = {'loc': move,
        #             'g_val': node['g_val'] + 1,
        #             'h_val': h(move.current, goal_state),
        #             'parent': node}



def main():
    my_map = agentBase.Map("maze_instances/maze1.txt")
    my_map.getMap()
    
    agent = agentBase.Agent(my_map)

    print("Euclidian Distance:", straight_line_heursitic([0,0], [10,10]))
    a_star_search(agent, straight_line_heursitic)



if __name__ == '__main__':
    main()
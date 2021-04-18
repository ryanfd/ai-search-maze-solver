import agentBase
import visualize
import search
import numpy as np
import heapq
import math

# required for animation. Put this wherever you want
expanded_nodes = []


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

def compare_f():
    pass


"""
Lazy A*
Takes the agent and heuristics function
Heuristic function takes current position and goal position

Returns paths and expanded nodes
"""
def lazy_a_star(agent,h):
    frontier = PQueue()
    frontier.put(agent.start, 0)
    came_from = np.array()
    cost_so_far = np.array()
    came_from[agent.start] = None
    cost_so_far[agent.start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == agent.goal:
            break
        
        next_steps = agent.nextStep()
        
        for next in next_steps:
            new_cost = cost_so_far[current] + h(next, agent.goal)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + h(next, agent.goal)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far



def main():

    maze_instance = ("maze_instances/maze1.txt") 
    algorithm = "lazy a_star algorithm"

    my_map = agentBase.Map(maze_instance)
    my_map.getMap()
    agent = agentBase.Agent(my_map)

    # sol_path, exp_nodes = breadth_first_search(agent)
    #sol_path, exp_nodes = depth_first_search(agent)
    sol_path, exp_nodes = lazy_a_star(agent,manhattan_heuristics)
    animation = visualize.Visualize(algorithm, maze_instance, my_map.start, my_map.goal, sol_path, exp_nodes)
    # sol_path, exp_nodes = a_star_search(agent, straight_line_heursitic)

    animation.StartAnimation()


if __name__ == '__main__':
    main()

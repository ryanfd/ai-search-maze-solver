import agentBase
import visualize
import numpy as np
import heapq
import math
import random
import copy

# required for animation. Put this wherever you want
expanded_nodes = []

class Node:
    def __init__(self,agent):
        self.location = agent.current
        self.numOfWins = 0
        self.parent = None
    
    def setValue(self, val):
        self.valueOfVisits = val
        
    def setNum(self, num):
        self.numOfVisits = num
        
    def addWinRate(self, incr):
        self.numOfWins += incr
        
    def getWinRate(self):
        return self.numOfWins

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



class MCTSearch:
    def __init__(self, agent):
        self.map = agent.map
        self.currentNode =  Node(agent) 
        self.visited = np.ndarray(agent.start)
      
    
    def move(self, direction,agent):
        agent.current = direction
    
    
    def moveOld(self, direction,agent):
        if direction == 1:
            agent.current[1] += 1
            
        if direction == 2:
            
            agent.current[0] += 1
            
        if direction == 3:
            agent.current[1] -= 1
            
        if direction == 4:
            agent.current[0] -= 1
            
        return agent.current
    
    
    def randPlayDFS(self, movePosition, agent):
        
        
        start_pos = (agent.start[0], agent.start[1])
        goal_pos = (agent.goal[0], agent.goal[1])
        current_pos = start_pos
        agentScout = copy.deepcopy(agent)
        
      

        open_stack = list()
        closed_list = dict()
        root = {'loc': start_pos, 'parent': None}
        open_stack.append(root)
        closed_list[(root['loc'])] = root

        nodes_expanded = 0
        max_size_of_open = len(open_stack)
        penalty = 0
        while len(open_stack) > 0:
            penalty += 1
            nodes_expanded += 1 # time complexity
            if len(open_stack) > max_size_of_open: # space complexity
                max_size_of_open = len(open_stack)
            random.shuffle(open_stack)
            node = open_stack.pop() # LIFO
 
            current_pos = node['loc']
            agentScout.current[0] = current_pos[0]
            agentScout.current[1] = current_pos[1]

            # path to goal state has been found
            if current_pos == goal_pos:
                return 10000 - penalty

            # take movement option indices in agentBase.nextStep()...
            # map out viable indices to locations in map
            move_options = agentScout.nextStep()
            random.shuffle(move_options)
            move_list = []
            for i in range(len(move_options)):
            #if len(move_options) > 0:
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
            for moveOption in move_list:
                child = {'loc': moveOption,
                         'parent': node}
                if not (child['loc']) in closed_list: # pruning
                    closed_list[(child['loc'])] = child
                    open_stack.append(child)
                    # end of for in loop
                    # end of while loop
        return -10 - penalty
    
    
    def randPlayBlind(self, movePosition, agent):
        agentScout = copy.deepcopy(agent)
        closed_list = []
        
        counter = 0
        while counter < 100:
            counter += 1
            direction = agentScout.randomMove()
            
            if (type(agent.current) is tuple):
                agent.current = np.asarray(agent.current)
                
            self.moveOld(direction, agent)
        
            if agentScout.map[agentScout.current[0]][agentScout.current[1]] != '1':
                return 10000
        
        return -10
        
    def treeSearch(self, agent):
        move_options = agent.nextStep()
        validMoves = []
        node = Node(agent)
        for i in range(len(move_options)):
            if move_options[i] == 1:
                validMoves.append((node.location[0], node.location[1]+1))
            if move_options[i] == 2:
                validMoves.append((node.location[0]+1, node.location[1]))
            if move_options[i] == 3:
                validMoves.append((node.location[0], node.location[1]-1))
            if move_options[i] == 4: 
                validMoves.append((node.location[0]-1, node.location[1]))
        # end of for in loop
        
        winRates = []
        for i in range(len(validMoves)):
            node = Node(agent)
            winRates.append(node)
            
        for i in range(len(validMoves)):
            for k in range(50):
                res = self.randPlayBlind(validMoves[i], agent)
                winRates[i].addWinRate(res)
        
        if len(validMoves) == 0:
            return agent.current
        
        
        bestChoice = validMoves[0]
        maxVal = 0
        for i in range(len(validMoves)):
            if winRates[i].getWinRate() > winRates[maxVal].getWinRate():
                maxVal = i
                bestChoice = validMoves[i]
                
        return bestChoice




    def random_forest(self,agent):
        counter = 0
        path = []
        print("START")
        while agent.map[agent.current[0]][agent.current[1]] != '1' and counter < 10:
            counter += 1
            direction = self.treeSearch(agent)
            #print("DIRECTION " + str(direction))
            #print(str(agent.current[0]) + " _ " + str(agent.current[1]))
            #print("MOVE " + str(self.agent.move(direction)))
            path.append(agent.current)
            self.move(direction,agent)
            
        
        print("DONE")
        return path, expanded_nodes



def main():
    #TODO - add time measurements!!!!!!!
    maze_instance = ("maze_instances/maze1.txt") 
    algorithm = "a_star algorithm"

    my_map = agentBase.Map(maze_instance)
    my_map.getMap()
    agent = agentBase.Agent(my_map)
    
    print("\nCoordinate Configuration: (Y, X)")
    print("Start State:", agent.start)
    print("Goal State:", agent.goal, "\n")
    
    mtc = MCTSearch(agent)

    #mtc.treeSearch()
    
    path, expanded_nodes = mtc.random_forest(agent)
    print(path)
    
    
    
    #sol_path, exp_nodes = random_forest(agent)
    #animation = visualize.Visualize(algorithm, maze_instance, my_map.start, my_map.goal, sol_path, exp_nodes)

    #animation.StartAnimation()


if __name__ == '__main__':
    main()

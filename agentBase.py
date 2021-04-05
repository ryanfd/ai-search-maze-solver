#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 19:13:46 2021

@author: vladyslav
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 18:00:06 2021

@author: vladyslav
"""
import numpy as np

class Map:
    def __init__(self, fileName):
        self.map = np.array([]) # 2D array representing a map
        self.start = np.array([0,0])
        self.goal = np.array([0,0])
        self.fileName = fileName
    
    """
    Takes an instance of the map and returns it as a 2D array of corresponding 'free' and 'blocked' cells
    """
    def getMap(self):
        with open(self.fileName) as textFile:
            self.map = np.array([line.split() for line in textFile])
        
        #print(self.map)
        
        # Searching for start and goal positions on the map
        for row in range(len(self.map)):
            for coll in range(len(self.map[row])):
                # Checking each cell one by one
                if self.map[row][coll] == '0':
                    self.start = np.array([row,coll])
                elif self.map[row][coll] == '1':
                    self.goal = np.array([row,coll])
                    
        print(self.start)
        print(self.goal)

class Agent:
    def __init__(self, my_map):
        self.map = my_map.map                      # 2D array representing a map
        self.start = my_map.start                  # Start coordinates
        self.goal = my_map.goal                    # Goal coordinates
        self.current = my_map.start                # Current position of the agent. For obvious reasons, intialy set to start location
        # All positions are represented as 1D numpy arrays, where 0th entry is x coordinate and
        # 1st entry is y
    
    
    """
    Performs a random move for an agent, if it is not blocked by an obsticle
    """
    def randomMove(self):
        nextSteps = self.nextStep()
        direction = np.random.choice(nextSteps)
        if direction == 1:
            self.current[1] += 1
            
        if direction == 2:
            self.current[0] += 1
            
        if direction == 3:
            self.current[1] -= 1
            
        if direction == 4:
            self.current[0] -= 1
            
        return self.current



    """
    Returns a list of not blocked directions for a next step. If none found, will return current
    Directions:          1
                         ^
                    4 <  0  > 2
                         v
                         3
    Meaning, that going 1 step up is coded as 1, right - 2, down - 3, left - 4 and not moving is 0
    The [0,0] is located at top left corner
    """
    def nextStep(self):
        possibleDirections = np.array([0])
        y = self.current[0]
        x = self.current[1]
        
        if (self.map[y][(x + 1)] == '.' or self.map[y][(x + 1)] == '1'):
            possibleDirections = np.append(possibleDirections,3)
            
        if (self.map[(y + 1)][x] == '.' or self.map[(y + 1)][x] == '1'):
            possibleDirections = np.append(possibleDirections,2)
                      
        if (self.map[y][(x - 1)] == '.' or self.map[y][(x - 1)] == '1'):
            possibleDirections = np.append(possibleDirections,1)
                      
        if (self.map[(y - 1)][x] == '.' or self.map[(y - 1)][x] == '1'):
            possibleDirections = np.append(possibleDirections,4)

        
        #if len(possibleDirections) == 0:
        #    possibleDirections.append(0)
        print("POSSIBLE DIRECTIONS" + str(possibleDirections))
        # print(str(self.map[self.current[0]][(self.current[1] + 1)]) + "---" + 
        #       str(self.map[(self.current[0] + 1)][self.current[1]]) + "---" + 
        #       str(self.map[self.current[0]][(self.current[1] - 1)]) + "---" + 
        #       str(self.map[(self.current[0])][self.current[1]]) + "---")
        # print(possibleDirections)
        return possibleDirections


"""
keep things to the bare minimum here
"""
def main():
    my_map = Map("maze_instances/maze1.txt")
    my_map.getMap()
    
    agent = Agent(my_map)
    for i in range(10):
        move = agent.randomMove()
        print(move)
        agent.current = move



if __name__ == '__main__':
    main()

import numpy as np

class Map:
    def __init__(self, fileName):
        self.map = np.array([]) # 2D array representing a map
        self.start = np.array([0,0])
        self.goal = np.array([0,0])
        self.fileName = fileName
        self.map_size = 0
    
    """
    Takes an instance of the map and returns it as a 2D array of corresponding 'free' and 'blocked' cells
    """
    def getMap(self):
        with open(self.fileName) as textFile:
            self.map = np.array([line.split() for line in textFile])
        
        # Searching for start and goal positions on the map
        for row in range(len(self.map)):
            for coll in range(len(self.map[row])):
                # Checking each cell one by one
                if self.map[row][coll] == '0':
                    self.map_size += 1
                    self.start = np.array([row,coll])
                elif self.map[row][coll] == '1':
                    self.goal = np.array([row,coll])
                    self.map_size += 1
                elif self.map[row][coll] == '.':
                    self.map_size += 1
        
        print("SIZE:", self.map_size)

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
        return np.random.choice(nextSteps)

    def move(self, direction):
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
    """
    def nextStep(self):
        possibleDirections = np.array([0])
        x = self.current[0]
        y = self.current[1]
        
        if (self.map[x][(y + 1)] == '.' or self.map[x][(y + 1)] == '1'):
            possibleDirections = np.append(possibleDirections,1)
            
        if (self.map[(x + 1)][y] == '.' or self.map[(x + 1)][y] == '1'):
            possibleDirections = np.append(possibleDirections,2)
                      
        if (self.map[x][(y - 1)] == '.' or self.map[x][(y - 1)] == '1'):
            possibleDirections = np.append(possibleDirections,3)
                      
        if (self.map[(x - 1)][y] == '.' or self.map[(x - 1)][y] == '1'):
            possibleDirections = np.append(possibleDirections,4)

        return possibleDirections



"""
keep things to the bare minimum here
"""
def main():
    my_map = Map("maze_instances/maze1.txt")
    my_map.getMap()
    
    agent = Agent(my_map)
    counter = 0
    # Code to keep agent moving around for a while. To search for bugs. Actually reached goal cell in 10000 steps
    while agent.map[agent.current[0]][agent.current[1]] != '1' and counter < 10000:
        counter += 1
        direction = agent.randomMove()
        print(str(agent.current[0]) + " " + str(agent.current[1]))
        agent.current = agent.move(direction)



if __name__ == '__main__':
    main()

import heapq
import random
import numpy as np
from collections import defaultdict 
from collections import namedtuple
class DecisionFactory:
    
    def __init__ (self, name='Davros'):
        self.name = name
        self.directions = [[ 'wait', 'up', 'down', 'right', 'left' ],
                           
                           [ 'wait', 'down', 'right', 'left' ], #wall up *4
                           [ 'wait', 'up', 'down', 'right'],    #wall left
                           [ 'wait', 'up', 'right', 'left' ],   #wall down
                           [ 'wait', 'up', 'down', 'left' ],    #wall right
                           
                           [ 'wait', 'down', 'right' ],        #wall up & left
                           [ 'wait', 'up', 'right'],           #wall down & left
                           [ 'wait', 'up', 'left'],            #wall down & right
                           [ 'wait', 'down','left' ],          #wall up & right
                           [ 'wait', 'right', 'left'],         #wall up & down
                           [ 'wait', 'up', 'down' ],           #wall right & left

                           [ 'wait', 'down'],                  #wall up & left & right
                           [ 'wait', 'up' ],                   #wall down & left & right
                           [ 'wait', 'left' ],                 #wall up & down & right
                           [ 'wait', 'right']]                 #wall up & down & left *17
        self.last_result = 'success'
        self.last_direction = 'wait'
        self.pos = [0,0]
        self.map=np.zeros((2,2),dtype=int)
        self.StartPos = [0,0]
        self.graph = defaultdict(list) 
        self.goal = [0,0]
        self.PATH = []
        
        Node = namedtuple("Node", "px py f g h")
        
        

    def get_decision(self, verbose = True):
        return self.random_direction()
    
    def random_direction(self):
        #r = random.randint(0,4) # Includes wait state
        print(self.last_result)
        print('position:',self.pos)
        print(self.map)
        print('Start position:',self.StartPos)
        print(self.PATH)
        if (len(self.PATH) != 0):
            next = self.PATH[0]
            print(next[0])
            print(self.pos[0])
            if(next[0] == self.pos[0]+1):
                self.last_direction = 'right'
                self.PATH.pop(0)
                return 'right'
            if(next[0] == self.pos[0]-1):
                self.last_direction = 'left'
                self.PATH.pop(0)
                return 'left'
            if(next[1] == self.pos[1]+1):
                self.last_direction = 'down'
                self.PATH.pop(0)
                return 'down'
            if(next[1] == self.pos[1]-1):
                self.last_direction = 'up'
                self.PATH.pop(0)
                return 'up'
            
                
                
        else:
            if(self.pos[1]+1 > self.map.shape[0]-1 and self.map[self.pos[1]][self.pos[0]] not in [6,10,12,15,16,17]) : # y > height
                self.last_direction = 'down'
                return 'down'
            elif(self.pos[1]-1 < 0 and self.map[self.pos[1]][self.pos[0]] not in [4,8,12,14,16,17]): # y < 0
                self.last_direction = 'up'
                return 'up'
            elif(self.pos[0]-1 < 0 and self.map[self.pos[1]][self.pos[0]] not in [5,8,9,13,14,15,17]): # x < 0
                self.last_direction = 'left'
                return 'left'
            elif(self.pos[0]+1 > self.map.shape[1]-1 and self.map[self.pos[1]][self.pos[0]] not in [7,10,11,13,14,15,16]): # x > length
                self.last_direction = 'right'
                return 'right'
            elif(self.map[self.pos[1]-1][self.pos[0]]  == 0): #if up is 0
                self.last_direction = 'up'
                return 'up'
            elif(self.map[self.pos[1]+1][self.pos[0]]  == 0): #if down is 0
                self.last_direction = 'down'
                return 'down'
            elif(self.map[self.pos[1]][self.pos[0]+1]  == 0): #if right is 0
                self.last_direction = 'right'
                return 'right'
            elif(self.map[self.pos[1]][self.pos[0]-1]  == 0): #if left is 0
                self.last_direction = 'left'
                return 'left'


            elif(self.map[self.pos[1]][self.pos[0]]  == 0 or self.map[self.pos[1]][self.pos[0]]  == -1): #can move anywhere
                r = random.randint (1,4) # Does NOT include wait
                i = 0
            else:
                i = self.map[self.pos[1]][self.pos[0]] -3
                n = len(self.directions[i]) #number of directions 
                r = random.randint (1,n-1) # Does NOT include wait

            # Update last direction to be the one just
            self.last_direction = self.directions[i][r]
            print(self.last_direction)
            return self.directions[i][r]


    def heuristic(self, goal, next):
        return abs(next[0] - goal[0]) + abs(next[1] - goal[1]) 
    
    class PriorityQueue:
        def __init__(self):
            self.elements = []
        def empty(self):
            return len(self.elements) == 0

        def put(self, item, priority):
            heapq.heappush(self.elements, (priority, item))

        def get(self):
            return heapq.heappop(self.elements)[1]

    def isValid(self, xy):
        if (self.map[xy[0]][xy[1]] == 1):
            return False
        else:
            return True
            
    def neighbors(self):
        x = self.pos[0]
        y = self.pos[1]
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(self.isValid, results)
        print(results)
        return results
    
    class Node():
        def __init__(self, parent=None, position=None):
            self.parent = parent
            self.position = position
            
            self.g = 0
            self.h = 0
            self.f = 0
            
        def __eq__(self, other):
            return self.position == other.position
        
    def a_star_search(self):
        start = (self.StartPos[0],self.StartPos[1])
        goal =(self.goal[0],self.goal[1])
        start_node = self.Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = self.Node(None, goal)
        end_node.g = end_node.h = end_node.f = 0
        
        open_list = []
        closed_list = []
        
        open_list.append(start_node)
        
        while len(open_list) > 0:
            #print(len(open_list))
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            
            open_list.pop(current_index)
            closed_list.append(current_node)
            
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] #reversed path
            
            children = []
            for new_position in [(0,1),(0,-1),(1,0),(-1,0)]:
                if current_node.position[0]+new_position[0] >= 0 and current_node.position[1]+new_position[1] >= 0 and current_node.position[0]+new_position[0] < self.map.shape[1]-1 and current_node.position[1]+new_position[1] < self.map.shape[0]-1:
                    node_position = (current_node.position[0]+new_position[0], current_node.position[1]+new_position[1])
                    if self.map[node_position[1]][node_position[0]] == 1 or self.map[node_position[1]][node_position[0]] == 0:
                        continue
                    new_node = self.Node(current_node, node_position)
                    children.append(new_node)

            for child in children:
                
                for closed_child in closed_list:
                    if child == closed_child:
                        continue
                        
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0])**2)+((child.position[1]-end_node.position[1])**2)
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                open_list.append(child)
                    

            
        
    
    def put_result(self, result):
        
        self.last_result = result
        
        if(self.last_direction == 'up'):
           self.pos[1] -= 1
        if(self.last_direction == 'left'):
           self.pos[0] -= 1
        if(self.last_direction == 'right'):
           self.pos[0] += 1
        if(self.last_direction == 'down'):
           self.pos[1] += 1
        if (self.last_result == 'portal'):
           self.map[self.pos[1]][self.pos[0]] = 2
           self.goal[0] = self.pos[0]
           self.goal[1] = self.pos[1]
           self.pos[1] = self.StartPos[1]
           self.pos[0] = self.StartPos[0]
           self.PATH = self.a_star_search()
           self.PATH.pop(0)
           return
            
        if (self.pos[1] < 0):    #expand up
            new=np.zeros((1,self.map.shape[1]),dtype=int)
            self.map=np.vstack((new,self.map))
            self.pos[1] = 0
            self.StartPos[1] +=1
            print("expand up")
        elif (self.pos[1] > self.map.shape[0]-1):    #expand down
            new=np.zeros((1,self.map.shape[1]),dtype=int)
            self.map=np.vstack((self.map,new))
            print("expand down")
        elif (self.pos[0] < 0):    #expand left
            new=np.zeros((self.map.shape[0],1),dtype=int)
            self.map=np.hstack((new, self.map))
            self.pos[0]=0
            self.StartPos[0] +=1
            print("expand left")
        elif (self.pos[0] > self.map.shape[1]-1):    #expand right
            new=np.zeros((self.map.shape[0],1),dtype=int)
            self.map=np.hstack((self.map, new))
            print("expand right")
        
        if(result == 'success' and self.map[self.pos[1]][self.pos[0]] == 0):
            self.map[self.pos[1]][self.pos[0]] = -1
            
        if (result == 'wall'):
            self.map[self.pos[1]][self.pos[0]] = 1
            if(self.last_direction == 'up'):
                self.pos[1] += 1
                if(self.map[self.pos[1]][self.pos[0]] == -1):
                    self.map[self.pos[1]][self.pos[0]]  = 4
                elif(self.map[self.pos[1]][self.pos[0]]  == 5):
                    self.map[self.pos[1]][self.pos[0]]  = 8
                elif(self.map[self.pos[1]][self.pos[0]]  == 6):
                    self.map[self.pos[1]][self.pos[0]]  = 12
                elif(self.map[self.pos[1]][self.pos[0]]  == 7):
                    self.map[self.pos[1]][self.pos[0]]  = 11
                elif(self.map[self.pos[1]][self.pos[0]]  == 9):
                    self.map[self.pos[1]][self.pos[0]]  = 17
                elif(self.map[self.pos[1]][self.pos[0]]  == 10):
                    self.map[self.pos[1]][self.pos[0]]  = 16
                elif(self.map[self.pos[1]][self.pos[0]]  == 13):
                    self.map[self.pos[1]][self.pos[0]]  = 14
            elif(self.last_direction == 'left'):
                self.pos[0] += 1
                if(self.map[self.pos[1]][self.pos[0]]  == -1):
                    self.map[self.pos[1]][self.pos[0]]  = 5
                elif(self.map[self.pos[1]][self.pos[0]]  == 4):
                    self.map[self.pos[1]][self.pos[0]]  = 8
                elif(self.map[self.pos[1]][self.pos[0]]  == 6):
                    self.map[self.pos[1]][self.pos[0]]  = 9
                elif(self.map[self.pos[1]][self.pos[0]]  == 7):
                    self.map[self.pos[1]][self.pos[0]]  = 13
                elif(self.map[self.pos[1]][self.pos[0]]  == 10):
                    self.map[self.pos[1]][self.pos[0]]  = 14
                elif(self.map[self.pos[1]][self.pos[0]]  == 11):
                    self.map[self.pos[1]][self.pos[0]]  = 14
                elif(self.map[self.pos[1]][self.pos[0]]  == 12):
                    self.map[self.pos[1]][self.pos[0]]  = 17
            elif(self.last_direction == 'right'):
                self.pos[0] -= 1
                if(self.map[self.pos[1]][self.pos[0]]  == -1):
                    self.map[self.pos[1]][self.pos[0]]  = 7
                elif(self.map[self.pos[1]][self.pos[0]]  == 4):
                    self.map[self.pos[1]][self.pos[0]]  = 11
                elif(self.map[self.pos[1]][self.pos[0]]  == 5):
                    self.map[self.pos[1]][self.pos[0]]  = 13
                elif(self.map[self.pos[1]][self.pos[0]]  == 6):
                    self.map[self.pos[1]][self.pos[0]]  = 10
                elif(self.map[self.pos[1]][self.pos[0]]  == 8):
                    self.map[self.pos[1]][self.pos[0]]  = 14
                elif(self.map[self.pos[1]][self.pos[0]]  == 12):
                    self.map[self.pos[1]][self.pos[0]]  = 16
                elif(self.map[self.pos[1]][self.pos[0]]  == 9):
                    self.map[self.pos[1]][self.pos[0]]  = 15
            elif(self.last_direction == 'down'):
                self.pos[1] -= 1
                if(self.map[self.pos[1]][self.pos[0]]  == -1):
                    self.map[self.pos[1]][self.pos[0]]  = 6
                elif(self.map[self.pos[1]][self.pos[0]]  == 4):
                    self.map[self.pos[1]][self.pos[0]]  = 12
                elif(self.map[self.pos[1]][self.pos[0]]  == 5):
                    self.map[self.pos[1]][self.pos[0]]  = 9
                elif(self.map[self.pos[1]][self.pos[0]]  == 7):
                    self.map[self.pos[1]][self.pos[0]]  = 10
                elif(self.map[self.pos[1]][self.pos[0]]  == 8):
                    self.map[self.pos[1]][self.pos[0]]  = 17
                elif(self.map[self.pos[1]][self.pos[0]]  == 11):
                    self.map[self.pos[1]][self.pos[0]]  = 16
                elif(self.map[self.pos[1]][self.pos[0]]  == 13):
                    self.map[self.pos[1]][self.pos[0]]  = 15
            
            
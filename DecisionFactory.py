  
import random
import numpy as np

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
        

    def get_decision(self, verbose = True):
        return self.random_direction()
    
    def random_direction(self):
        #r = random.randint(0,4) # Includes wait state
        print(self.last_result)
        print('position:',self.pos)
        print(self.map)
        
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
        
        if (self.pos[1] < 0):    #expand up
            new=np.zeros((1,self.map.shape[1]),dtype=int)
            self.map=np.vstack((new,self.map))
            self.pos[1] = 0
            print("expand up")
        elif (self.pos[1] > self.map.shape[0]-1):    #expand down
            new=np.zeros((1,self.map.shape[1]),dtype=int)
            self.map=np.vstack((self.map,new))
            print("expand down")
        elif (self.pos[0] < 0):    #expand left
            new=np.zeros((self.map.shape[0],1),dtype=int)
            self.map=np.hstack((new, self.map))
            self.pos[0]=0
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
            
            
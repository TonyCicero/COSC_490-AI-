
  
import random
#import numpy as np

class DecisionFactory:
	
    def __init__ (self, name='Davros'):
    	self.name = name
    	self.directions = [[ 'wait', 'up', 'down', 'right', 'left' ],
						   
						   [ 'wait', 'down', 'right', 'left' ],
						   [ 'wait', 'up', 'down', 'right'],
						   [ 'wait', 'up', 'right', 'left' ],
						   [ 'wait', 'up', 'down', 'left' ],
						   
						   [ 'wait', 'down', 'right' ],
						   [ 'wait', 'up', 'right'],
						   [ 'wait', 'up', 'left'],
						   [ 'wait', 'down','left' ],
						   [ 'wait', 'right', 'left'],
						   [ 'wait', 'up', 'down' ],

						   [ 'wait', 'down'],
						   [ 'wait', 'up' ],
						   [ 'wait', 'left' ],
						   [ 'wait', 'right']]
    	self.last_result = 'success'
    	self.last_direction = 'wait'
		self.pos = [0,0]
		self.map=np.zeros((1,1),dtype=int)
		self.map[0,0] = 2
		

    def get_decision(self, verbose = True):
    	return self.random_direction()
    
    def random_direction(self):
    	#r = random.randint(0,4) # Includes wait state
    	r = random.randint (1,4) # Does NOT include wait
    	
        if(self.last_result == 'wall'):
            if(self.directions[r] == self.last_direction):
                self.random_direction()
		
            
        
        # Update last direction to be the one just
    	self.last_direction = self.directions[r]

      
    	return self.directions[r]
    
    def put_result(self, result):
    	self.last_result = result
		

		if(self.last_direction == 'up'):
		   self.pos[1] += 1
		if(self.last_direction == 'left'):
		   self.pos[0] -= 1
		if(self.last_direction == 'right'):
		   self.pos[0] += 1
		if(self.last_direction == 'down'):
		   self.pos[1] -= 1
		
		if (self.pos[0] < 0):	#expand left
			new=np.zeros((self.a,self.b),dtype=int)
			self.map=np.vstack((new,self.map))
		elif (self.pos[0] > self.map.shape[0]):	#expand right
			new=np.zeros((self.a,self.b),dtype=int)
			self.map=np.vstack((new,self.map))
		elif (self.pos[1] < 0):	#expand up
			new=np.zeros((self.a,self.b),dtype=int)
			self.map=np.hstack((new,self.map))
		elif (self.pos[0] > self.map.shape[1]):	#expand down
			new=np.zeros((self.a,self.b),dtype=int)
			self.map=np.hstack((new,self.map))
			
		if (result == 'wall'):
			self.map[self.pos[0]][self.pos[1]] = 1
			if(self.last_direction == 'up'):
		   		self.pos[1] -= 1
				if(self.map[self.pos[0]][self.pos[1]] == 0):
					self.map[self.pos[0]][self.pos[1]] = 4
				elif(self.map[self.pos[0]][self.pos[1]] == 5):
					self.map[self.pos[0]][self.pos[1]] = 8
				elif(self.map[self.pos[0]][self.pos[1]] == 6):
					self.map[self.pos[0]][self.pos[1]] = 12
				elif(self.map[self.pos[0]][self.pos[1]] == 7):
					self.map[self.pos[0]][self.pos[1]] = 11
				elif(self.map[self.pos[0]][self.pos[1]] == 9):
					self.map[self.pos[0]][self.pos[1]] = 17
				elif(self.map[self.pos[0]][self.pos[1]] == 10):
					self.map[self.pos[0]][self.pos[1]] = 16
				elif(self.map[self.pos[0]][self.pos[1]] == 13):
					self.map[self.pos[0]][self.pos[1]] = 14
			elif(self.last_direction == 'left'):
		   		self.pos[0] += 1
				if(self.map[self.pos[0]][self.pos[1]] == 0):
					self.map[self.pos[0]][self.pos[1]] = 5
				elif(self.map[self.pos[0]][self.pos[1]] == 4):
					self.map[self.pos[0]][self.pos[1]] = 8
				elif(self.map[self.pos[0]][self.pos[1]] == 6):
					self.map[self.pos[0]][self.pos[1]] = 9
				elif(self.map[self.pos[0]][self.pos[1]] == 7):
					self.map[self.pos[0]][self.pos[1]] = 13
				elif(self.map[self.pos[0]][self.pos[1]] == 10):
					self.map[self.pos[0]][self.pos[1]] = 14
				elif(self.map[self.pos[0]][self.pos[1]] == 11):
					self.map[self.pos[0]][self.pos[1]] = 14
				elif(self.map[self.pos[0]][self.pos[1]] == 12):
					self.map[self.pos[0]][self.pos[1]] = 17
			elif(self.last_direction == 'right'):
		   		self.pos[0] -= 1
				if(self.map[self.pos[0]][self.pos[1]] == 0):
					self.map[self.pos[0]][self.pos[1]] = 7
				elif(self.map[self.pos[0]][self.pos[1]] == 4):
					self.map[self.pos[0]][self.pos[1]] = 11
				elif(self.map[self.pos[0]][self.pos[1]] == 5):
					self.map[self.pos[0]][self.pos[1]] = 13
				elif(self.map[self.pos[0]][self.pos[1]] == 6):
					self.map[self.pos[0]][self.pos[1]] = 10
				elif(self.map[self.pos[0]][self.pos[1]] == 8):
					self.map[self.pos[0]][self.pos[1]] = 14
				elif(self.map[self.pos[0]][self.pos[1]] == 12):
					self.map[self.pos[0]][self.pos[1]] = 16
				elif(self.map[self.pos[0]][self.pos[1]] == 9):
					self.map[self.pos[0]][self.pos[1]] = 15
			elif(self.last_direction == 'down'):
		   		self.pos[1] += 1
				if(self.map[self.pos[0]][self.pos[1]] == 0):
					self.map[self.pos[0]][self.pos[1]] = 6
				elif(self.map[self.pos[0]][self.pos[1]] == 4):
					self.map[self.pos[0]][self.pos[1]] = 12
				elif(self.map[self.pos[0]][self.pos[1]] == 5):
					self.map[self.pos[0]][self.pos[1]] = 9
				elif(self.map[self.pos[0]][self.pos[1]] == 7):
					self.map[self.pos[0]][self.pos[1]] = 10
				elif(self.map[self.pos[0]][self.pos[1]] == 8):
					self.map[self.pos[0]][self.pos[1]] = 17
				elif(self.map[self.pos[0]][self.pos[1]] == 11):
					self.map[self.pos[0]][self.pos[1]] = 16
				elif(self.map[self.pos[0]][self.pos[1]] == 13):
					self.map[self.pos[0]][self.pos[1]] = 15
			
			
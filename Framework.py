from DecisionFactory import DecisionFactory  
import pygame, sys
from pygame.locals import *
from pygame.time import Clock

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
grey = (50, 50, 50)

colours = {
            0 : white,
            1 : grey,
            2 : green,
            3 : blue,
            4 : red
            }

Grid =[]


TILESIZE = 50
MAPWIDTH = 10
MAPHEIGHT = 10

#current position of player [row, col]
POSITION = [3,3]

#PLAYER HAS FOUND GOAL
FINISHED = False

#Steps to reach Portal
STEPS = 0;

#find starting position
def find_pos():
    global POSITION
    
    for row in range(MAPHEIGHT):
        for col in range(MAPWIDTH):
            tile = Grid[row][col]
            if tile == 2:
                POSITION = [row, col]
                return

#gets decision & checks if valid
def validate_move(DF):
    global FINISHED
    global POSITION
    global Grid
    global STEPS
    choice = DF.get_decision()
    if choice == 'right':
        check_pos = [POSITION[0],POSITION[1]+1]
    if choice == 'left':
        check_pos = [POSITION[0],POSITION[1]-1]
    if choice == 'down':
        check_pos = [POSITION[0]+1,POSITION[1]]
    if choice == 'up':
        check_pos = [POSITION[0]-1,POSITION[1]]
    if choice == 'wait':
        check_pos = [POSITION[0],POSITION[1]]
    tile = Grid[check_pos[0]][check_pos[1]]
    if tile == 3:
        Grid[POSITION[0]][POSITION[1]] = 0
        POSITION[0] = check_pos[0]
        POSITION[1] = check_pos[1]
        Grid[POSITION[0]][POSITION[1]] = 2
        FINISHED = True
        STEPS += 1
        return 'portal'
    if tile == 0:
        Grid[POSITION[0]][POSITION[1]] = 0
        POSITION[0] = check_pos[0]
        POSITION[1] = check_pos[1]
        Grid[POSITION[0]][POSITION[1]] = 2
        STEPS += 1
        return 'success'
    else: 
        STEPS += 1
        return 'wall'
    
def open_map():
    global Grid
    row = 0
    with open('map.txt', 'r') as file:
        for line in file.readlines():
            line =line.strip()
            Grid.append([])
            for ch in line:
                Grid[row].append(int(ch))
            row += 1
            

    
def main():
    global MAPWIDTH
    global MAPHEIGHT
    global Grid
    #read map
    open_map()
    
    #Set Map dimensions
    MAPHEIGHT= len(Grid) 
    MAPWIDTH = len(Grid[0]) 
    
    find_pos()
 
	# Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))
    pygame.display.set_caption('490 AI')
    clock = pygame.time.Clock()
    #instantiate DF
    DF = DecisionFactory()

    # Event loop
    while not FINISHED:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
 
	
        for row in range(MAPHEIGHT):
            for col in range(MAPWIDTH):
                pygame.draw.rect(screen, colours[Grid[row][col]], [col*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE])
            
        
    	
        DF.put_result(validate_move(DF))   
        pygame.display.flip()
        clock.tick(10)
    print ("Portal found in:",STEPS,"steps")

if __name__ == '__main__': main()
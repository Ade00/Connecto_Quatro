import pygame, random, colours
from pygame.locals import *
from colours import *

pygame.init()

#Constants
W = 100
ROWS = 6
COLS = 7
WINDOWHEIGHT = W * ROWS
WINDOWWIDTH = W * COLS
CAPTION = 'Connect 4'
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
MARGIN = 0.8
GAP = W*(1-MARGIN)/2
BOXSIZE = W * MARGIN

pygame.Surface.fill(DISPLAYSURF, YELLOW)

def DrawRectangle(row, column, colour):
    pygame.draw.rect(DISPLAYSURF,colour,(W * column + GAP, W * row + GAP, BOXSIZE, BOXSIZE))
    pygame.display.update()

def DrawBoard():
    for row in range(ROWS):
        for column in range(COLS):
            DrawRectangle(row, column, WHITE)
            
    pygame.display.update()

def setup():
    DrawBoard()

def playerTurn(column, grid):
    for row in range(ROWS):                    # Search the Column for the 1st SPACE
        if grid[row][column] == ' ': break

    grid[row][column] = 'P'
    DrawRectangle(ROWS-1-row,column, ORANGE)
    return grid

def computerTurn(grid, IBEF_grid):
    plays = {}
    for column in range(COLS):                 # Determine available moves by
        for row in range (ROWS):               # searching all columns for 1st SPACE
            if grid[row][column] == ' ':
                # Assemble a dictionary of moves and Weightings
                plays[IBEF_grid[row][column]] = (row, column)
                break

    IBEF = []
    for play in plays:
        IBEF.append(play)

    move = plays[max(IBEF)]
    
    print(plays)
    print(IBEF)
    print(move)
    grid[move[0]][move[1]] = 'C'
    DrawRectangle(ROWS-1-move[0],move[1], GREEN)
    
    return grid
    

#Game code
setup()
turn = 'player'

# Initialise Grids
grid = []
for x in range(ROWS):
    grid.append([' '] * COLS)

IBEF_grid = [[3, 4, 5, 7, 5, 4, 3],
             [4, 6, 8,10, 8, 6, 4],
             [5, 8,11,13,11, 8, 5],
             [5, 8,11,13,11, 8, 5],
             [4, 6, 8,10, 8, 6, 4],
             [3, 4, 5, 7, 5, 4, 3]]


#Main loop

while True:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            column = int(pos[0] / W)
            row = int(pos[1] / W)

            grid = playerTurn(column, grid)
            
            grid = computerTurn(grid, IBEF_grid)

    pygame.display.update()



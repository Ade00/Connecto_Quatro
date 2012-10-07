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

def match_r_diag(match, grid):
    match = []
    for row in range(ROWS):
        for col in range(COLS):
            diag_list = []
            for c in range(ROWS):
                diag_list.append(grid[c][col])

            diag_str = ''
            diag_str = diag_str.join(diag_list)
                
            try:
                row = diag_str.index(match_str)
            except ValueError:
                row = -1

            if (row != -1):
                match.append(row)
                match.append(col)
                
    return tuple(match)

def match_hor(match_str, grid):
    match = []
    for row in range(ROWS):
        row_str = ''
        row_str = row_str.join(grid[row])
        try:
            col = row_str.index(match_str)
        except ValueError:
            col = -1

        if (col != -1):
            match.append(row)
            match.append(col)
                
    return tuple(match)

def match_ver(match_str, grid):
    match = []
    for col in range(COLS):
        col_list = []
        for c in range(ROWS):
            col_list.append(grid[c][col])

        col_str = ''
        col_str = col_str.join(col_list)
            
        try:
            row = col_str.index(match_str)
        except ValueError:
            row = -1

        if (row != -1):
            match.append(row)
            match.append(col)
                
    return tuple(match)


def match_all(mat, grid):
    move = []
    for sp in range(4):
        match_base = [mat]*4
        match_str = ''
        match_base[sp] = ' '
        match_str = match_str.join(match_base)      # Form the string to MATCH
        
        match = match_hor(match_str,grid)
        if match != ():
            move.append((match[0],match[1]+sp))
        
        match = match_ver(match_str,grid)
        if match != ():
            move.append((match[0]+sp,match[1]))

    return move


def playerTurn(column, grid):
    for row in range(ROWS):                    # Search the Column for the 1st SPACE
        if grid[row][column] == ' ': break

    grid[row][column] = 'P'
    DrawRectangle(ROWS-1-row,column, ORANGE)
    return grid


def computerTurn(grid, IBEF_grid):

    plays = {}                                 # Plays with different IBEF weights
    plays_all = []                             # Find all available moves
    for column in range(COLS):                 # Determine available moves by
        for row in range (ROWS):               # searching all columns for 1st SPACE
            if grid[row][column] == ' ':
                # Assemble a dictionary of moves and Weightings
                plays[IBEF_grid[row][column]] = (row, column)
                plays_all.append((row,column))
                break
            
    # Can the Computer win in this turn?
    move = ()
    mv = match_all('C', grid)
    print(mv)
    for m in mv:
        for play in range(len(plays_all)):
                if plays_all[play] == m: move = m
    
    if move == ():
        # Can the Player win in this turn?
        mv = match_all('P', grid)
        print(mv)
        for m in mv:
            for play in range(len(plays_all)):
                if plays_all[play] == m: move = m

    if move == ():                                 # Nobody can win.
        IBEF = []
        for play in plays:
            IBEF.append(play)

        move = plays[max(IBEF)]
        print(IBEF)
        
    print(plays_all)                
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

Play = True
grid = computerTurn(grid, IBEF_grid)        # Computer Turn
while Play:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            column = int(pos[0] / W)
            row = int(pos[1] / W)

            grid = playerTurn(column, grid)     # Player Turn

            if (match_hor('PPPP', grid) != () or match_ver('PPPP', grid) != ()):
                print('PLAYER WINS !!')
                Play = False

            grid = computerTurn(grid, IBEF_grid)        # Computer Turn

            if (match_hor('CCCC', grid) != () or match_ver('CCCC', grid) != ()):
                print('COMPUTER WINS !!')
                Play = False

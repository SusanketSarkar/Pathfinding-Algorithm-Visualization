import pygame
import sys, os
from colors import *
import random
from cells import *


# this function displays the screen when there is no solution
def displayResultScreen():
    pygame.display.flip() # updates the pygame application
    pygame.time.wait(3000) # waits for 3 seconds before continuing the program

# this function will check if the user wants to quit the program
def checkForExit():
    for event in pygame.event.get(): # gets the user input
        if event.type == pygame.QUIT: # checks if the event type is quit
            exitProgram() # calls the exit program function

# this function exits the program
def exitProgram():
    pygame.quit() # quits the application
    sys.exit() # exits the program

# this function will determine what cell the mouse is hovering over and then change the state of the cell
def selectWall(grid, mouse_pos, new_state, end_node, start_node): # takes 4 variables as parameters
    x = mouse_pos[0] // 20 # determines the x index
    y = mouse_pos[1] // 20 # determines the y index
    if grid[x][y] != end_node and grid[x][y] != start_node: # ensures the current cell is not the start or end node
        grid[x][y].wall = new_state # changes the state of the cell

# this function will determine what cell the mouse is hovering over and then return the value to select it as start
def selectStart(grid, mouse_pos, start_node, end_node):
    x = mouse_pos[0] // 20 # determines the x index
    y = mouse_pos[1] // 20 # determines the y index
    # print(str(x) + " " + str(y)) # this print statement can be uncommented to see the x and y of the start cell
    if grid[x][y] != end_node: # ensures the cell is not the end node
        return grid[x][y] # returns the corresponding cell
    else:
        return start_node # returns the original start node

# this function will determine what cell the mouse is hovering over and then return the value to select it as end
def selectEnd(grid, mouse_pos, start_node , end_node): 
    x = mouse_pos[0] // 20 # determines the x index
    y = mouse_pos[1] // 20 # determines the y index
    if grid[x][y] != start_node: # ensures the cell is not the start node
        return grid[x][y] # returns the corresponding cell
    else:
        return end_node # returns the original end node

# this function will draw the grid and color each cell with the correct color
def drawGrid(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list):
    screen.fill(BLACK) # fills the entire screen with a light green which will later be the color of the grid lines
    
    # this loop will cycle through all the cells in the grid
    for y in range(grid_rows): 
        for x in range(grid_col):
            
            cell = grid[x][y] 
            cell.colorCell(screen, VLIGHTGRN, "small square") # this is the color of a regular cell

            if cell == start: # checks if the cell is the start node
                cell.colorCell(screen, RED, "node")
            
            elif cell == end: # checks if the cell is the end node
                cell.colorCell(screen, VIOLET, "node")
            
            elif cell in path: # checks if the cell is in the path list
                cell.colorCell(screen, DARKGREEN, "small square")
            
            elif cell in open_list: # checks if the cell is in the open_list list
                cell.colorCell(screen, DARKSAND, "circle")
            
            elif cell in closed_list: # checks if the cell is in the closed_list list
                cell.colorCell(screen, DARKLIME, "small square")
            
            elif cell.wall: # checks if the cell is a wall
                cell.colorCell(screen, BLACK, "small square")
                
    pygame.display.update() # updates the pygame display to show the new changes

'''# this function will display the image on the screen
def displayImage(screen, image): # takes an image as the parameter
    screen.blit(image, (0,0))
    pygame.display.flip()'''

# this program will clear all the walls from the grid
def clearWall(grid, grid_rows, grid_col):
    for x in range(grid_col): # loops through all the columns
        for y in range(grid_rows): # loops through all the rows
            grid[x][y].wall = False # sets the wall state to false for every cell

# this function will generate random walls in the grid
def generateRandomWalls(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list):
    clearWall(grid, grid_rows, grid_col)
    for x in range(grid_col): # loops through all the columns
        for y in range(grid_rows): # loops through all the rows
            if grid[x][y] == start or grid[x][y] == end: # if the current cell is the start or end it will skip it
                continue # goes back to the top of the loop
            else:
                if random.randint(1, 1000) < 400: # generates a random integer and then checks if it is less than 400; 400 is a random number which can be changed to effect the probability that the cell will be a wall
                    grid[x][y].wall = True # makes the current cell a wall        
                else:
                    continue
        drawGrid(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list) # updates the grid

# this function will initialize the grid that will be used for the logic and gui of the program
def initGrid(grid, grid_rows, grid_col, use_diagonal):
    # adds all the cells to the grid
    for x in range(grid_col): # loops through every column
        row_list = [] # instantiates a new list
        for y in range(grid_rows): # loops through every row
            row_list.append(Cells(x, y)) # adds a cell for each row
        grid.append(row_list) # adds the row_list to the grid list
    
    # adds the neighbors of all the cells in the grid
    for x in range(grid_col):
        for y in range(grid_rows):
            grid[x][y].addNeighbors(grid, grid_col, grid_rows, use_diagonal)
            grid[x][y].wall = False
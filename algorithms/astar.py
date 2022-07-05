# this is the program file for astar algorithm
import math 
from colors import *
from functions import *

# This function returns the absolute euclidean distance between the current and end node
def heuristic(current_node, end_node):
    return math.sqrt((current_node.x_pos - end_node.x_pos)**2 + abs(current_node.y_pos - end_node.y_pos)**2) 

# this function will backtrack to determine all the cells that are in the shortest path
def aStarBackTrack(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list, current): # takes the current node as the only parameter
    print("Backtracking called.") # this print statement is used for debugging
    in_path = current # assigns the current to the path_node
    while True: # runs the loop until it reaches the start node
        checkForExit()
        if in_path.previous_node == None or in_path.previous_node == start: # checks whether there is no previous node or the current node is the start node
            break # exits the loop
        else:
            path.append(in_path.previous_node) # adds the previous node to the path list
            in_path = in_path.previous_node # assigns the previouse node to the in_path variable
            drawGrid(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list)
    print("Done Backtracking") # this print statement should be uncommented when debugging the program

# this function implements the A* algorithm
def aStarSearch(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list):
    print('Finding the shortest route with A* algorithm')
    start.h_score = heuristic(start, end) # determines the euclidean distance from the start node to end node
    open_list.append(start) # adds the start node to the open_list list   
    while len(open_list) > 0: # runs the loop until the open_list list is empty
        
        checkForExit()
        
        open_list.sort(key=lambda x: x.f_score) # this returns the open_list sorted by f_scores using a lambda function passed in the optional key parameter

        current_node = open_list[0] # the current node is assigned to the cell with the lowest f score in the open_list      
        
        if current_node == end: # checks if the current node is the end
            open_list.remove(current_node) # removes the current node from the open set
            aStarBackTrack(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list, current_node) # passes the current node to the backtracking function
            return
        
        else:
            open_list.remove(current_node) # removes from open_list and adds to closed_list
            closed_list.append(current_node)

            for cells in current_node.neighbors: # loops through all the neighbors of a cell
                
                if cells in closed_list or cells.wall == True: # checks if the cell has already been looked at or is a wall
                    continue # goes back to the top of the loop
                
                else:

                    new_g_score = current_node.g_score + 1 # adds one to the g score
                    use_new_path = False # initializes the use_new_path as false
                    
                    if cells in open_list: # checks if the cell is in the open list
                        if new_g_score < cells.g_score: #  checks if the new g score is less than the current g score
                            cells.g_score = new_g_score # assigns the new g score to the cell
                            use_new_path = True # since the g score is lower than the original one, the algorithm will now use this new path to the cell
                    
                    else:
                        cells.g_score = new_g_score # assigns the new g score to the cell
                        use_new_path = True # since this cell has not been visited yet it will use it as a new path
                        open_list.append(cells) # adds this cell to the open_list
                    
                    if use_new_path == True: # checks if the algorithm has to use the new path
                        cells.h_score = heuristic(cells, end) # determines the h score of the cell
                        cells.f_score = cells.g_score + cells.h_score # determines the f score of the cell
                        cells.previous_node = current_node # assigns the current node as the previous node to this cell
        
        #print(open_list, closed_list, path)
        drawGrid(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list) # updates the screen
    pygame.time.wait(7000) # wait 700 milliseconds before continuing 
    displayResultScreen() # this screen will only run when the open_list is empty and there are no other neighbors; this means there is no possible path between the start and end node

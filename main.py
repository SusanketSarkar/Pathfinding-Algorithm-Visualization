import pygame
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from pygame.locals import *
import math
import os, sys, random
import numpy as np
from cells import Cells
from colors import BLACK, DARKLIME, DEEPBLUE, GREEN, LIGHTLIME, LIME, RED
from functions import *
from Algorithms.astar import *
from Algorithms.djkistra import *
 
# initialize the constant variables
grid = []
grid_rows = 70
grid_col = 70
side_length = 10
screen_length = grid_col * side_length 
screen_width = grid_rows * side_length 
use_diagonal = TRUE
screen_size = (screen_length, screen_width)

# Initializing the pygame and tkinter application
pygame.init() 
screen = pygame.display.set_mode((640,640))
pygame.display.set_caption("Visualize your pathfinding algorithms")

# main program loop
while True: # this loop will run until the user wishes to quit the program
    initGrid(grid, grid_rows, grid_col, use_diagonal)
    # initializes the positions of the start and end nodes
    start = grid[5][18]
    end = grid[54][18]
    
    # instantiates/resets all the lists
    open_list = []
    closed_list = []
    path = []

    # initializes all the flag variables
    is_selecting_start = True
    is_selecting_end = False
    is_selecting_walls = False 
    start_search = False
    reset_game = False


    drawGrid(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list) # draws the current grid
    pygame.display.flip() 

    # this loop will run until the user wishes to reset the grid
    while True:
        
        # checks if the user is selecting the start node
        if is_selecting_start == True:
            for event in pygame.event.get(): # gets the user input
                if event.type == pygame.QUIT: # checks if the user wants to quit the program
                    exitProgram()
                if event.type == pygame.MOUSEBUTTONDOWN: # checks if the user pressed a mouse button
                    if event.button in (1, 3): # checks if they pressed mouse button 1, 2 or 3
                        start = selectStart(grid, pygame.mouse.get_pos(), start, end)
                if event.type == pygame.KEYDOWN: # checks if the user pressed a key
                    if event.key == pygame.K_RETURN: # checks if the key was return/enter
                        is_selecting_start = False 
                        is_selecting_end = True
                    if event.key == pygame.K_c: # checks if the key pressed was c
                        reset_game = True
        
        # checks if the user is selecting the end node
        if is_selecting_end == True: 
            for event in pygame.event.get(): # gets the user input
                if event.type == pygame.QUIT: # checks if the user wants to quit the program
                    exitProgram()
                if event.type == pygame.MOUSEBUTTONDOWN:  # checks if the user pressed a mouse button
                    if event.button in (1, 3): # checks if they pressed mouse button 1, 2 or 3
                        end = selectEnd(grid, pygame.mouse.get_pos(), start, end)
                if event.type == pygame.KEYDOWN: # checks if the user pressed a key
                    if event.key == pygame.K_RETURN: # checks if the key was return/enter
                        is_selecting_end = False
                        is_selecting_walls = True
                    if event.key == pygame.K_c: # checks if the key pressed was c
                        reset_game = True

        # checks if the user is selecting walls
        if is_selecting_walls == True:
            for event in pygame.event.get(): # gets the user input
                if event.type == pygame.QUIT: # checks if the user wants to quit the program
                    exitProgram()
                if event.type == pygame.MOUSEBUTTONDOWN: # checks if the user pressed a mouse button  
                    if event.button in (1, 3): # checks if they pressed mouse button 1, 2 or 3
                        selectWall(grid, pygame.mouse.get_pos(), event.button==1, end, start)
                if event.type == pygame.MOUSEMOTION: # checks if the user moved their mouse
                    if event.buttons[0] or event.buttons[2]:
                        selectWall(grid, pygame.mouse.get_pos(), event.buttons[0], end, start) 
                if event.type == pygame.KEYDOWN: # checks if the user pressed a key
                    '''if event.key == pygame.K_RETURN: # checks if the key was return/enter
                        start_search = True
                        is_selecting_walls = False'''
                    if event.key == pygame.K_a: # checks if the key was return/enter
                        start_search = 'astar'
                    if event.key == pygame.K_d: # checks if the key was return/enter
                        start_search = 'dijkstra'
                    if event.key == pygame.K_b: # checks if the key was return/enter
                        start_search = 'bfs'
                    if event.key == pygame.K_f: # checks if the key was return/enter
                        start_search = 'dfs'
                    if event.key == pygame.K_c: # checks if the key pressed was c
                        reset_game = True
                    if event.key == pygame.K_w: # checks if the key pressed was w
                        generateRandomWalls(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list)
                    if event.key == pygame.K_BACKSPACE: # checks if the key pressed was backspace
                        clearWall(grid, grid_rows, grid_col)

        # checks if the program should start the search with astar algorithm
        if start_search == 'astar': 
            aStarSearch(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list)
            pygame.time.wait(3000)
            start_search = False
        if start_search == 'dijkstra': 
            dijkstra(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list)
            pygame.time.wait(3000)
            start_search = False
            

        # checks if the user wants to quit the program or clear the grid
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitProgram()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    reset_game = True
        
        if reset_game == True:
            break

        drawGrid(screen, grid, grid_rows, grid_col, start, end, path, open_list, closed_list) # draws the current grid
        pygame.display.flip() # updates the screen
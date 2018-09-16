#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:52:53 2018
"""
import math
import random
from PIL import Image, ImageDraw
#from image import create_image, draw_square, save_image

#
def segMeasure(grid, numColors, numColored):
#simulation is the grid we are measuring segregation of, type is the actor type we are measuring it for
    measure = 0
    count = 0#number of actors of the type we are inspecting/total number of actors
    vacant = 0
    bigDist = 12
    for i in range(0,(len(grid)-12)//12):
        for j in range(0,(len(grid[0])-12)//12):
            count=0
            vacant=0
            if grid[i][j] != 'e':
                for k in range(i-bigDist+1, i+bigDist):
                    for l in range(j-bigDist+1, j+bigDist):
                        if grid[i][j] == grid[j][k]:
                            count = count + 1
                        elif grid[j][k] == 'e':
                            vacant = vacant + 1
                measure+=.5*(count/(144-vacant))/(numColors[grid[i][j]]/numColored)-144/((len(grid)*len(grid[1])))
    return measure

## Takes inputs of size (grid size as a tuple of # rows, # columns), numSquares
    ##(#rows*#cols), numEmpty (numSquares*empty-to-color ratio), and groups
    ##(a dictionary where each key is a group and each value is a list of the group's
    ## ratio and color)
def createGrid(size, numSquares, numEmpty, groups):
   orderedDots = ['e']*numEmpty
   for group in groups.keys():
       numDots = groups[group][0]*numSquares
       orderedDots = orderedDots + group*numDots

   grid = []
   empties = []
   #appends empty lists to dot grid array for each row
   for i in range(size[0]):
       grid.append([])
   for i in range(numSquares):
       #gets a random dot from orderedDots and places in grid
       x = random.randint(0, len(orderedDots)-1)
       grid[math.floor(i/size[1])].append(orderedDots[x]) ##not assigning to grid[10]

       if orderedDots[x] == 'e':
           empties.append((math.floor(i/size[1]), i % (size[1])))
       orderedDots.remove(orderedDots[x])
   return [grid, empties]

def checkNeighbors(dots, dotLoc, dist, happyRat):
    dotType = dots[dotLoc[0]][dotLoc[1]]
    neighbors = ""
    for i in range(max(0, dotLoc[0]-dist), min(len(dots)-1, dotLoc[0]+dist)+1):
        for j in range(max(0, dotLoc[1]-dist), min(len(dots[0])-1, dotLoc[1]+dist)+1):
            if i != dotLoc[0] or i != j:
                neighbors = neighbors + dots[i][j]     
    if neighbors.count(dotType)/(len(neighbors) - neighbors.count('e')) < happyRat:
        return False
    return True

def simulate(size, EtoC, RtoB, dist, happyRat, iteration):
    numSquares = size[0]*size[1]
    numEmpty = math.floor(EtoC*numSquares)
    numRed = math.floor(RtoB*(numSquares - numEmpty))
    numBlue = numSquares - numEmpty - numRed
    numColors = {'r': numRed, 'b': numBlue}
    gAndE = createGrid(size, numSquares, numEmpty, [numRed, numBlue])
    grid = gAndE[0]
    empties = gAndE[1]
    return simHelp(grid, empties, dist, happyRat, numSquares, numColors, iteration)

def simHelp(grid, empties, dist, happyRat, numSquares, numColors, iteration):
    drawGrid(grid)
    unhappy = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 'e' and not checkNeighbors(grid, (i,j), dist, happyRat):
                unhappy.append((i,j))
    if len(unhappy) == 0 or iteration >10:
        print(segMeasure(grid, numColors, numSquares-len(empties)))
        return False
    else:
        for cell in unhappy:
            x = random.randint(0, len(empties)-1)
            #print(str(cell) + " moves to " + str(empties[x]))
            grid[empties[x][0]][empties[x][1]] = grid[cell[0]][cell[1]]
            grid[cell[0]][cell[1]] = 'e'
            empties[x] = (cell[0],cell[1])   
        print(segMeasure(grid, numColors, numSquares-len(empties)))
        iteration = iteration + 1
        simHelp(grid, empties, dist, happyRat, numSquares, numColors, iteration)

    
# =============================================================================
#     row = empties[0][0]
#     col = empties[0][1]
#     while grid[row][col] == 'e':
#         row = random.randint(0, len(grid)-1)
#         col = random.randint(0, len(grid[row])-1)
#     satisfied = checkNeighbors(grid, [row, col], dist, happyRat)
#     if iteration < 100 and satisfied:
#         print(grid)
#         simHelp(grid, empties, EtoC, RtoB, dist, happyRat, iteration+1)
#     elif iteration < 100:
#         x = random.randint(0, len(empties)-1)
#         grid[empties[x][0]][empties[x][1]] = grid[row][col]
#         grid[row][col] = 'e'
#         empties[x] = (row, col)
#         drawGrid(grid)
#         simHelp(grid, empties, EtoC, RtoB, dist, happyRat, iteration+1)
# =============================================================================

##Create images
# i selects row, j selects column


def drawGrid(grid):   
    SWATCH_WIDTH=32
    R_COLOR=(228, 28, 28)
    B_COLOR=(28, 48, 228)
    E_COLOR= (255,255,255)
    imgR = Image.new('RGB', (SWATCH_WIDTH, SWATCH_WIDTH), color = R_COLOR)
    imgB = Image.new('RGB', (SWATCH_WIDTH, SWATCH_WIDTH), color = B_COLOR)
    img = Image.new('RGB', (SWATCH_WIDTH*len(grid[0]), SWATCH_WIDTH*len(grid)), color = E_COLOR)
    imgD = ImageDraw.Draw(img)
    #im = create_image(SWATCH_WIDTH*len(grid),SWATCH_WIDTH*len(grid[0]))
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "r":
                color = R_COLOR
                img.paste(imgR, (32*j, 32*i))
            elif grid[i][j] == "b":
                img.paste(imgB, (32*j, 32*i))
            else:
                pass

    img.show()      
    #img.save('pil_text.png')
            #draw_square(im, j*SWATCH_WIDTH,i*SWATCH_WIDTH,
            #            SWATCH_WIDTH-2, color)
    #save_image(im, filename)           

simulate([36, 36], .2, .6, 1, .5, 0)





#36 by 36, neighborhood size 6
##inputs: size of grid, proportion of red, proportion of empty,
##          proportion of same-type neighbors needed to be happy

## red is between 0 and 1, non-inclusive
## empty is also between 0 and 1, non-inclusive




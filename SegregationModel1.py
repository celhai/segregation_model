#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:52:53 2018
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
#from image import create_image, draw_square, save_image

#
def segMeasure(grid, groups, numColored):
#simulation is the grid we are measuring segregation of, type is the actor type we are measuring it for
    measurelist=[]
    count = 0#number of actors of the type we are inspecting/total number of actors
    vacant = 0
    bigDist = 12
    numSquares = len(grid)*len(grid[0])
    #iterates through neighborhood of size bigDist
    keys = groups.keys()
    for key in keys:
        measure = 0
        measure1 = 0
        for i in range(0,(len(grid)-bigDist)//bigDist):
            for j in range(0,(len(grid[0])-bigDist)//bigDist):
                count=0
                vacant=0
                for k in range(bigDist*i, bigDist*(i+1) - 1):
                    for l in range(bigDist*j, bigDist*(j+1) - 1):
                        if key == grid[k][l]:
                            count = count + 1
                        elif grid[k][l] == 'e':
                            vacant = vacant + 1
                if vacant != bigDist*bigDist:
                    measure += abs((count/(bigDist*bigDist-vacant))/(groups[key][0]*numSquares/numColored)-1)
        measurelist.append([key, round(measure/(numSquares/bigDist/bigDist), 5)])
    return measurelist

def segMeasure1(grid, groups, numColored):
#simulation is the grid we are measuring segregation of, type is the actor type we are measuring it for
    measurelist=[]
    count = 0#number of actors of the type we are inspecting/total number of actors
    vacant = 0
    dist = 1
    numSquares = len(grid)*len(grid[0])
    #iterates through neighborhood of size bigDist
    keys = groups.keys()
    for key in keys:
        numSame = 0
        numEmpts = 0
        for k in range(len(grid)):
            for l in range(len(grid[0])):
                if grid[k][l] == key:
                    for i in range(max(0, k-dist), min(len(grid)-1, k+dist)+1):
                        for j in range(max(0, l-dist), min(len(grid[0])-1, l+dist)+1):
                            if grid[i][j] == key and (i != k or i != j):
                                numSame += 1
                            elif grid[i][j] == 'e':
                                numEmpts += 1
        measurelist.append([key, round(numSame/(numSquares*groups[key][0]*8 - numEmpts), 5)])

    return measurelist

## Takes inputs of size (grid size as a tuple of # rows, # columns), numSquares
    ##(#rows*#cols), numEmpty (numSquares*empty-to-color ratio), and groups
    ##(a dictionary where each key is a group and each value is a list of the group's
    ## ratio and color)
def createGrid(size, numSquares, numEmpty, groups):
   orderedDots = ['e']*numEmpty
   for group in groups.keys():
       numDots = groups[group][0]*numSquares
       orderedDots = orderedDots + [str(group)]*int(numDots)
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
    if neighbors.count('e') != len(neighbors) and neighbors.count(dotType)/(len(neighbors) - neighbors.count('e')) < happyRat:
        return False
    return True

#Takes tuple for grid size (rows, columns), empty-to-colored ratio
def simulate(size, EtoC, groups, dist, happyRat, iteration):
    numSquares = size[0]*size[1]
    numEmpty = math.floor(EtoC*numSquares)
    gAndE = createGrid(size, numSquares, numEmpty, groups)
    grid = gAndE[0]
    empties = gAndE[1]
    datas =  simHelp(grid, empties, dist, happyRat, numSquares, groups, iteration, [[],[]], [[],[]], [[],[]], [[],[]], [])
    plt.figure(1)
    plt.plot(list(range(len(datas[0][0]))), datas[0][0], 'r')
    plt.plot(list(range(len(datas[1][0]))), datas[1][0], 'b')
    plt.plot(list(range(len(datas[2][0]))), datas[2][0], 'y')
    plt.plot(list(range(len(datas[3][0]))), datas[3][0], 'orange')
    plt.plot(list(range(len(datas[3][0]))), datas[4], 'k')
    plt.figure(2)
    plt.plot(list(range(len(datas[0][1]))), datas[0][1], 'r')
    plt.plot(list(range(len(datas[1][1]))), datas[1][1], 'b')
    plt.plot(list(range(len(datas[2][1]))), datas[2][1], 'y')
    plt.plot(list(range(len(datas[3][1]))), datas[3][1], 'orange')
    plt.plot(list(range(len(datas[3][1]))), datas[4], 'k')
    plt.show()
    return True

def simHelp(grid, empties, dist, happyRat, numSquares, groups, iteration, segR, segB, segY, segO, happyPercList):
    unhappy = []

    for i in range(len(grid)):
        for j in range(len(grid[0])): ##iterates through squares to check which ones are unhappy agents
            if grid[i][j] != 'e' :
                myHappyRat = groups[grid[i][j]][1]
                if not checkNeighbors(grid, (i,j), dist, myHappyRat):
                    unhappy.append((i,j))
    segMeas = segMeasure(grid, groups, numSquares-len(empties))
    segMeas1 = segMeasure1(grid, groups, numSquares-len(empties))
    segR[0].append(segMeas[0][1])
    segB[0].append(segMeas[1][1])
    segY[0].append(segMeas[2][1])
    segO[0].append(segMeas[3][1])
    segR[1].append(segMeas1[0][1])
    segB[1].append(segMeas1[1][1])
    segY[1].append(segMeas1[2][1])
    segO[1].append(segMeas1[3][1])
    happyPercList.append(1-len(unhappy)/(numSquares-len(empties)))
    drawGrid(grid, segMeas, iteration, round((1-len(unhappy)/(numSquares-len(empties)))*100, 5))
    if len(unhappy) == 0 or len(unhappy)/(numSquares-len(empties)) < .05 or iteration > 149: ##stops when all are happy, 95% are happy, or it runs 150 iterations
        return [segR, segB, segY, segO, happyPercList]
    else:
        for cell in unhappy:
            x = random.randint(0, len(empties)-1)
            #print(str(cell) + " moves to " + str(empties[x]))
            grid[empties[x][0]][empties[x][1]] = grid[cell[0]][cell[1]]
            grid[cell[0]][cell[1]] = 'e'
            empties[x] = (cell[0],cell[1])
        #print(segMeasure(grid, groups, numSquares-len(empties)))
        iteration = iteration + 1
    return simHelp(grid, empties, dist, happyRat, numSquares, groups, iteration, segR, segB, segY, segO, happyPercList)


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


def drawGrid(grid, segMeas, iteration, happyPerc):
    SWATCH_WIDTH=32
    R_COLOR=(228, 28, 28) #red, asian
    B_COLOR=(28, 48, 228) #blue, white people
    G_COLOR = (16,163,38)#green, black people
    O_COLOR = (229,155,18) #orange, hispanic people
    E_COLOR= (255,255,255) #empty, white
    imgR = Image.new('RGB', (SWATCH_WIDTH, SWATCH_WIDTH), color = R_COLOR)
    imgB = Image.new('RGB', (SWATCH_WIDTH, SWATCH_WIDTH), color = B_COLOR)
    imgG = Image.new('RGB', (SWATCH_WIDTH, SWATCH_WIDTH), color = G_COLOR)
    imgO = Image.new('RGB', (SWATCH_WIDTH, SWATCH_WIDTH), color = O_COLOR)
    img = Image.new('RGB', (SWATCH_WIDTH*len(grid[0]), SWATCH_WIDTH*len(grid)+30), color = E_COLOR)
    imgD = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)

    #im = create_image(SWATCH_WIDTH*len(grid),SWATCH_WIDTH*len(grid[0]))

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "r":
                color = R_COLOR
                img.paste(imgR, (32*j, 32*i))
            elif grid[i][j] == "b":
                img.paste(imgB, (32*j, 32*i))
            elif grid[i][j] == "g":
                img.paste(imgG, (32*j, 32*i))
            elif grid[i][j] == "o":
                img.paste(imgO, (32*j, 32*i))
            else:
                pass
    imgD.text((SWATCH_WIDTH*len(grid[0])/2-270, SWATCH_WIDTH*len(grid)+3), "Segregation: " + str(segMeas[0][0]) + ": " + str(segMeas[0][1]) + ", " + str(segMeas[1][0]) + ": " + str(segMeas[1][1]) + ", " + str(segMeas[2][0]) + ": " + str(segMeas[2][1]) + ", " + str(segMeas[3][0]) + ": " + str(segMeas[3][1]), font=fnt, fill=(0, 0, 0))
    imgD.text((5, SWATCH_WIDTH*len(grid)+3), "Iteration: " + str(iteration), font=fnt, fill=(0, 0, 0))
    imgD.text((SWATCH_WIDTH*len(grid[0])-250, SWATCH_WIDTH*len(grid)+3), "Percent Happy: " + str(happyPerc), font=fnt, fill=(0, 0, 0))
    #img.show()
    imgPath = "/Users/justinberman/Documents/Williams/Sophomore Year/MATH 433/pictures/" + str(iteration) + ".jpg"
    img.save(imgPath)
    #img.save('pil_text.png')
            #draw_square(im, j*SWATCH_WIDTH,i*SWATCH_WIDTH,
            #            SWATCH_WIDTH-2, color)
    #save_image(im, filename)

simulate([36, 36], .25, {'r': [.25,.5], 'b': [.25,.5], 'g': [.25,.5], 'o': [.25,.5]}, 3, .5, 0)


#36 by 36, neighborhood size 6
##inputs: size of grid, proportion of red, proportion of empty,
##          proportion of same-type neighbors needed to be happy

## red is between 0 and 1, non-inclusive
## empty is also between 0 and 1, non-inclusive

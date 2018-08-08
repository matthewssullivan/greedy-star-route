# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:47:26 2018

@author: oneey_000
By Matt Sullivan
"""

import math             # used for sqrt function
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

class star:
    def __init__(self, idnum, HD, HR, gliese, BayerFlamsteed, proper, dist, xcoord, ycoord, zcoord):
        self.idnum= int(idnum)                  
        self.dist = float(dist)
        self.xcoord = float(xcoord)
        self.ycoord = float(ycoord)
        self.zcoord = float(zcoord)
        self.HD = str(HD)
        self.HR = str(HR)
        self.gliese = str(gliese)
        self.BayerFlamsteed = str(BayerFlamsteed)
        self.proper = str(proper)
        self.distanceTravelled=0
        self.totalDistanceTravelled=0
        if self.proper:                         #Sets name of star, prioritizing Proper name, BayerFlamsteed, Gliese, HR, HD, or generated name
            self.name=proper
        elif self.BayerFlamsteed:
            self.name = str(BayerFlamsteed)
        elif self.gliese:
            self.name = "Gliese " + str(gliese)
        elif self.HR:
            self.name = "Harvard Revised " + str(HR)
        elif self.HD:
            self.name = "Henry Draper " + str(HD)
        else:
            self.name = "Unnamed Star " + str(idnum)

    def __repr__(self):             #Sets the return value of the star object
        return (self.name)
    def __str__(self):              #Sets the return value of the object in print statements
        return (self.name)
    def __lt__(self,other):         #Sets the less than value of the star object
        return (self.dist<other.dist)
        
def readFromFile(readFile):        #CSV parser I wrote for to read stars from file
    starList=[]
    myFile = open(readFile, "r")
    next(myFile)                    #Skips first line
    for line in myFile:
        workLine=line.split(",")
        newStar=star(workLine[0], workLine[2], workLine[3], workLine[4], workLine[5], workLine[6], workLine[9], workLine[17], workLine[18],workLine[19])
        starList.append(newStar)
    return starList

totalStarList = readFromFile("hygxyz.csv")
medStarList=[]
smallStarList=[]

print("Total Star List Size: " + str(len(totalStarList)))

for entry in totalStarList:
    if entry.dist <=100:
        medStarList.append(entry)

print("# Stars within 100 parsecs: " + str(len(medStarList)))

for entry in medStarList:
    if entry.dist <=10:
        smallStarList.append(entry)

print("# Stars within 10 parsecs: " + str(len(smallStarList)))

def greedyStarRoute(origin, starList):          #Program to select nearest star
    iteration=0
    currentTotalDistance=1000000000                 #Arbitarily large number set as default
    for destination in starList:                #Steps through list
        iteration+=1
        xDist=(destination.xcoord - origin.xcoord)**2   #Gets difference of x values squared
        yDist=(destination.ycoord - origin.ycoord)**2   #gets difference of y values squared
        zDist=(destination.zcoord - origin.zcoord)**2   #gets difference of z values squared
        totalDist = math.sqrt(xDist + yDist + zDist)    #Gets the square root of all of those values added
        if totalDist < currentTotalDistance:            #if it's smaller than the smallest distance
            currentTotalDistance=totalDist              #set the current distance to the smallest distance
            target=destination                          #the target is the destination
    starList.remove(target)                             #Delete the closest target from the list
    target.distanceTravelled = currentTotalDistance     #Set the target's distance travelled variable to the current leg
    target.totalDistanceTravelled = currentTotalDistance+origin.totalDistanceTravelled     #Update the total distance travelled
    return target, iteration             #return the target
                                 
def calculateStarRoute(starList):
    origin =min(starList)                     #Sets the origin
    routeInOrder=[]
    totalDistance = 0
    totalIt=0
    while len(starList)>0:                            #While there's still stars left
        nextStop, numIt = greedyStarRoute(origin, starList)  #Next stop is the target of greedyStarRoute
        routeInOrder.append(nextStop)                      #Append the stop to the route
        origin = nextStop                                  #Sets the next stop to the origin value of greedyStarRoute
        totalDistance += nextStop.distanceTravelled
        totalIt+=numIt    

    print(len(routeInOrder))

    for index, entry in enumerate(routeInOrder):
        if index < len(routeInOrder)-1:
            print(entry.name + " -> " + routeInOrder[index+1].name + " Distance: " + str('%s' % float('%.3g' % routeInOrder[index+1].distanceTravelled)) + " Total Distance Travelled: " + str('%s' % float('%.5g' % routeInOrder[index+1].totalDistanceTravelled)))
    
    print("Total Distance Travelled: " + str('%s' % float('%.5g' % totalDistance)))
    print("Number of iterations Greedy: " + str(totalIt))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xline=[]
    yline=[]
    zline=[]
    for element in routeInOrder:
        xline.append(element.xcoord)
        yline.append(element.ycoord)
        zline.append(element.zcoord)
    ax.plot(xline,yline,zline)
    plt.show()

#    for angle in range(0, 360):     #Rotating plot of star route, uncomment to enable
#        ax.view_init(30, angle)
#        plt.draw()
#        plt.pause(.001)

calculateStarRoute(smallStarList)

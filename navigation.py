import numpy as np
import math as math
import heapq
from robot import Robot as robot
from Canvas import Canvas
import time
from place_rec_bits import SignatureContainer


def square(dist=40):
    offset = 100
    wpts = np.array([[offset, offset, 0],
                     [offset + dist, offset, 0],
                     [offset + dist, offset - dist, 0],
                     [offset, offset - dist, 0],
                     [offset, offset, 0],
                     [offset+ 10, offset, 0]])
    
    navigateThroughWaypoints(wpts)
       
def line(dist=100):
    
    offset = 100
    wpts = np.array([[offset, offset, 0],
                     [offset + dist, offset, 0],
                     [offset, offset, 0],
                     [offset + 10, offset, 0]])
    
    navigateThroughWaypoints(wpts)
    

def userInput():   
    myLoc = np.array([0, 0, 0])
    r = robot(myLoc)
    
    while True:
        x = float(input("Enter a x coordinate (in cm): "))
        y = float(input("Enter a y coordinate (in cm): "))
        dest = np.array([x, y, 0])
        myLoc = navigateToWaypoint(myLoc, dest)
        print(myLoc)

def cwWaypoints():
    wpts = np.array([[84, 30, 0], #XXX
                     [132, 30, 0], 
                     [180, 30, 0], #XXX
                     [180, 42, 0],
                     [180, 54, 0], #XXX
                     [159, 54, 0], 
                     [138, 54, 0], #XXX
                     [138, 111, 0], 
                     [138, 168, 0], #XXX
                     [126, 168, 0],
                     [114, 168, 0], #XXX 
                     [114, 126, 0],
                     [114, 84, 0], #XXX
                     [99, 84, 0],
                     [84, 84, 0], #XXX
                     [84, 57, 0], 
                     [84, 30, 0]])
    
    navigateThroughWaypoints(wpts)

def compWaypoints():
    wpts = np.array([[84, 30, 0], # 1
                     [132, 30, 0], 
                     [180, 30, 0], # 2
                     [180, 54, 0], # 3
                     [138, 54, 0], # 4
                     [138, 111, 0], 
                     [138, 168, 0], # 5
                     [111, 99, 0], #XXX
                     [84, 30, 0] # 1
                     ])
    
    navigateThroughWaypoints(wpts)

    
def compWaypoints_rt():
    wpts = np.array([[84, 30, 0], # 1
                     [180, 30, 0], # 2
                     [180, 54, 0], # 3
                     [138, 54, 0], # 4                 
                     [138, 168, 0], # 5
                     [84, 30, 0] # 1
                     ])
    
    navigateThroughWaypoints(wpts)
    
    
def navigateThroughWaypoints(wpts):    
    
    # myLoc = wpts[0]
    canvas = Canvas()
    r = robot(wpts, canvas)
    startingLoc = r.getStartingLocation()
    
    n_wpts = len(wpts)
    
    for wp in wpts:
        canvas.drawWaypoint(wp)
    
    for i in range(n_wpts):
        myLoc = r.navigateToWaypoint(wpts[(i + 1 + startingLoc) % n_wpts])
        # myLoc = r.navigateToWaypoint_rt(wpts[(i + 1 + startingLoc) % n_wpts])
        print("At location: {0}".format(myLoc))                 
        time.sleep(1)
        print '\a'
        
        
if __name__ == "__main__":
    
    # line(80)
    # userInput()
    
    #square(100)
    compWaypoints()
    # cwWaypoints()
    # square(80)
    # compWaypoints_rt()
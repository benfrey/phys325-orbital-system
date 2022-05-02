#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:21:02 2020

OrbitDriver is the driver file for the movement of planets.

@author: Ben Frey
"""

import sys
sys.path.insert(1, 'lib')
import Model as md
import pandas as pd
import matplotlib.pyplot as plt
import Render as rn
import Animate as an

def main():    
    # Time step width in seconds needs to be at least 0.01 (or smaller) for
    # a good orbit to occur. Otherwise, the planet's orbit is thrown off.
    dt = 0.01
    # Total time steps
    steps = 600
    
    #SolarSystemModel
    mySolarSystem = md.SolarSystemModel()
    
    names = ["Mercury","Venus","Earth","Mars","Comet"]
    
    # Create a dataframe to store all planet attributes in.
    df = pd.DataFrame({"planet":[],
                       "x":[],"y":[],"z":[],
                       "r":[],"v":[],"e":[]})

    # Iterate and advance solar system. Heart of program.
    tNext = []
    for i in range(steps):
        # progress update
        if i%(steps/10-1) == 0:
            print(str(10*i/((steps/10)-1))+"%...")
            
        tn, bodies = mySolarSystem.advance(dt)     
        tNext.append(tn)
        
        for j in range(len(bodies)):
            dTemp = pd.DataFrame({"planet":[names[j]],
                                   "x":[bodies[j].state[0]],
                                   "y":[bodies[j].state[1]],
                                   "z":[bodies[j].state[2]],
                                   "r":[bodies[j].pos],
                                   "v":[bodies[j].vel],
                                   'e':[mySolarSystem.total_energy(names[j])]})
            df = df.append(dTemp, ignore_index = True) 
            
    # We'll plot only the planets we want 
    # (Earth and Mars)
    fig = plt.figure()
    ax = plt.axes(xlim=(-2.0, 1.5), ylim=(-1.6, 1.6), aspect=1)
    ax.scatter([0], [0], s=10, label="Sun")

    for i, val in enumerate([2,3]):
        dTemp = df.loc[df['planet'] == names[val]]
        ax.scatter(dTemp['x'].values, dTemp['y'].values, s=1, label=names[val])
    
    ax.set_xlabel('Distance (AU)')
    ax.set_ylabel('Distance (AU)')
    plt.legend(loc=2)
    plt.show()    
        
    # Show animated plot, input selected colors.
    colors = [[153,76,0],[76,0,153],[0,153,75],[153,0,0],[96,96,96]]
    sizes = [8,9,15,12,5]
    
    render = rn.RenderSolarSystem([100,-100],[600,300],colors,sizes)
    myDim = [800,600]
    ani = an.Animate(mySolarSystem,render,myDim)
    
    ani.run()

if __name__=="__main__":
    main()
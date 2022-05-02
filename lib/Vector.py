#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 09:32:15 2020

Creates a class that allows us to manipulate vectors.

@author: Ben Frey
"""
import numpy

def main():
    myVec1 = Vector(2,4)    
    myVec2 = Vector(1,3)
    myVec3 = Vector(1,2)
    
    newVec1 = myVec1*3.0
    print("Mult by 3.0: ["+repr(newVec1.x)+","+repr(newVec1.y)+"]")
    
    newVec2 = myVec1 + myVec2    
    print("Add myVec1 and myVec2: ["+repr(newVec2.x)+","+repr(newVec2.y)+"]")
    
    myVec3.theta = 40
    print("Change angle of myVec3 to 40 degrees: ["+repr(myVec3.x)+","+repr(myVec3.y)+"]")
        
class Vector():
    """A vector that exists in the universe.

    Attributes
    ----------
    x : float
        X value of vector
    y : float
        Y value of vector
    r : float
        Magnitude of vector
    theta : float
        Theta of vector
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @property
    def r(self):
        """Returns the magnitude of the vector"""
        return numpy.sqrt(numpy.square(self.x)+numpy.square(self.y))

    @r.setter
    def r(self,val):
        """Sets the magnitude of the vector"""
        ratio = self.r/val 
        self.x = self.x/ratio
        self.y = self.y/ratio

    @property
    def theta(self):
        """Gets the angle between the components of the vector"""
        return numpy.rad2deg(numpy.arctan(self.y/self.x))

    @theta.setter
    def theta(self,val):
        """Sets the angle between the components of the vector"""
        currentR = self.r
        self.x = currentR*numpy.cos(numpy.deg2rad(val))
        self.y = currentR*numpy.sin(numpy.deg2rad(val))
        
    def __mul__(self,val):
        """Scalar multiplication
        
        Parameters
        ----------
        val : float
            Value by which to multiply each element of the vector
            
        Returns
        -------
        New Vector containing scaled vector.
        """
        
        xNew = self.x*val
        yNew = self.y*val
        return Vector(xNew, yNew)
    
    def __add__(self,newVec):
        """Vector addition
        
        Parameters
        ----------
        val : Vector
            Vector to add component-wise to self
            
        Returns
        -------
        New Vector containing added vectors.
        """

        xNew = self.x+newVec.x
        yNew = self.y+newVec.y
        return Vector(xNew,yNew)
        
if __name__=="__main__":
    main()

    


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 19:00:06 2020

Render the scene.

@author: Ben Frey
"""
import numpy as np
import pygame as pg

class Render(object):
    """Render class handles the drawing of animation to the screen.

    Parameters
    ----------
    scale : 1x2 float array
        Scale of animation with respect to units in model.
    offset : 1x2 float array
        Redefine origin of model to better fit screen.

    Returns
    -------
    None.
    """
    def __init__(self,scale,offset):
        self.scale = scale
        self.offset = offset
        
    def draw(self,model,screen):
        """Draw the animation to screen. To be implemented below"""
        print("Should never be printed")
        # Needs to be implemented in RenderSolarSystem
    
    def coord_transform(self,coords):
        """Transformation of each coordinate to match the new scale and
        origin provided by offset.

        Parameters
        ----------
        coords : 1x2 float array
            Coordinate of body in model.

        Returns
        -------
        Float array
            New adjusted corrdinate of body in a model.
        """
        transform = np.array([[self.scale[0],0],[0,-1*self.scale[1]]])
        origin = self.offset
        return np.matmul(transform, coords) + origin
    
class RenderSolarSystem(Render):
    """Child of render, meant for a SolarSystem.

    Attributes
    ----------
    scale : 1x2 float array
        Scale of animation with respect to units in model.
    offset : 1x2 float array
        Redefine origin of model to better fit screen.
    colors : 1xn array of RGB tuples
        Array of RGB colors for each body.
    sizes : 1xn array of Ints
        Size representation of each body.

    Returns
    -------
    None.
    """
    def __init__(self,scale,offset,colors,sizes):
        self.colors = colors
        self.sizes = sizes
        super().__init__(scale,offset)   

    def draw(self,model,screen):
        """Draw animation to the screen.
        
        Paramaters
        ----------
        model : Model
            Model to be drawn.
        screen : pg.display object
            Screen to draw model to.
            
        Returns
        -------
        None.
        """
        # Reset screen
        screen.fill((0,0,0))
        # Draw the sun again.
        pg.draw.circle(screen,[255,255,0],self.offset,10)
        
        # Draw each body in model.
        for i in range(len(model.bodies)):
            x = model.bodies[i].x
            y = model.bodies[i].y
            pos = self.coord_transform([x, y])
            # Draw new body position (note pos need to be ints)
            pg.draw.circle(screen,self.colors[i],pos.astype(int),self.sizes[i])

            
        
        
        
        
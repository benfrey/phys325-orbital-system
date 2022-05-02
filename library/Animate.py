#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 17:34:31 2020

Class represents the process of Animation.

@author: Ben Frey
"""
import pygame as pg

class Animate(object):
    """To be extended by another sub class, composite of multiple objects
    
    Attributes
    ----------
    model : Model
        Model object containing bodies to be animated.
    render : Render
        Render instance that controls drawing to screen
    screen_size : Int array
        Int array of screen dimensions.
        
    Returns
    ----------
    None
    """
    def __init__(self,model,render,ss):
        self.model = model
        self.render = render
        self.screen_size = ss
        self.done = False;
        self.time = 0;
        self.dt = 0
        self.screen = pg.display.set_mode(self.screen_size)
        self.time_scale = (1/3e3) #years per 3e3 ms
    
    def _timing_handler(self):
        """Handle the differences in clock speed we will find across 
        different machines. Implements a time scale so that the animation will
        run at the same rate on different machines.

        Returns
        -------
        None.
        """
        # Handle time
        previous_time = self.time
        self.time = pg.time.get_ticks()
        self.dt = (self.time - previous_time)*self.time_scale
        previous_time = self.time
        
    def _event_handler(self):
        """Observes events that take place on the user's machine. These
        involve interactions with the keyboard or screen by xing out or
        pressing escape.

        Returns
        -------
        None.
        """
        # Handle events
        for event in pg.event.get():
            # Closing the pygame window causes a quit event
            if event.type == pg.QUIT:
                self.done = True
            
            # Look for the escape key
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True 
    
    def run(self):
        """Handles the initialization and destruction of the pygame window.
        Provides continous animation until an event handler is met.
        
        Returns
        -------
        None.
        """
        # Initialize pygame and open a window
        pg.init()   
        
        while not self.done:   # Some event triggers done
            # Check handlers
            self._timing_handler()
            self._event_handler()
        
            # Draw the picture, gotta pass in model and existing screen
            self.render.draw(self.model,self.screen)
                    
            # Advance the model
            self.model.advance(self.dt)
            
            # Update the display
            pg.display.update()
        
            # Loop runs too fast, must throttle it
            pg.time.delay(10)
        
        pg.quit()
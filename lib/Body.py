# -*- coding: utf-8 -*-
"""
Classes representing physical objects
This set of classes represents physical objects.  It is primarily a way to 
keep track of the attributes (temperature, position, velocity, etc) of objects
in the simulator.  They are inteded for use with the  Physics classes.
"""
import numpy as np

class ThermalBody(object):
    '''An object that has temperature

    Attributes
    ----------
    temperature : float
        The current temperature of the object    
    '''
    
    def __init__(self,temperature):
        self.temperature = temperature
        
    @property
    def state(self):
        return self.temperature
    
    @state.setter
    def state(self,temperature):
        self.temperature = temperature
        
class GravBody(object):
    """An planet to orbit the sun
    
    Attributes
    ----------
    x : float
        x coordinate for pos.
    y : float
        y coordinate for pos.
    z : float
        z coordinate for pos.
    vx : float
        x coordinate for vel.
    vy : float
        y coordinate for vel.
    vz : float
        z coordinate for vel.
    m : float
        mass of GravBody.
        
    Returns
    -------
    None.
    """
    def __init__(self,x,y,z,vx,vy,vz,m):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.m = m
        self.r = np.sqrt(np.square(x)+np.square(y)+np.square(z))
        self.v = np.sqrt(np.square(vx)+np.square(vy)+np.square(vz))
    
    @property
    def pos(self):
        """Returns the magnitude of the pos"""
        return self.r
    
    @property
    def vel(self):
        """Returns the magnitude of the velocity"""
        return self.v
       
    @property
    def state(self):
        """
        Getter for state of GravBody.

        Returns
        -------
        List
            Contains 7 floats describing pos and motion of body.
        """
        return [self.x, self.y, self.z, self.vx, self.vy, self.vz, self.m]
    
    @state.setter
    def state(self,f):
        """Setter for state of GravBody.

        Parameters
        ----------
        f : list
            Contains info to set the state of the planet.
            
        Returns
        -------
        None.
        """
        self.x = f[0]
        self.y = f[1]
        self.z = f[2]
        self.vx = f[3]
        self.vy = f[4]
        self.vz = f[5]
        self.m = f[6]
        self.r = np.sqrt(np.square(f[0])+np.square(f[1])+np.square(f[2])) 
        self.v = np.sqrt(np.square(f[3])+np.square(f[4])+np.square(f[5])) 
        
    def __str__(self):
        """Output the GravBody in an easy to read format.

        Returns
        -------
        String
            Easy format to read in console.
        """
        pos = "Pos: <"+"{:.3f}".format(self.x)+","+"{:.3f}".format(self.y)+">, "
        vel = "Vel: <"+"{:.3f}".format(self.vx)+","+"{:.3f}".format(self.vy)+">, "
        dist = "Dist: "+"{:.3f}".format(self.r)+">"
        return pos+vel+dist
    
class PopulationBody(object):
    """A body that has population

    Attributes
    ----------
    P : float
        The current population of the object    
    """
    
    def __init__(self,P):
        self.P = P
        
    @property
    def state(self):
        return self.P
    
    @state.setter
    def state(self,P):
        self.P = P
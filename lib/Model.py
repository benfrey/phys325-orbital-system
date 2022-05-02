# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 16:51:03 2020

Classes represent complex models. For example, the OrbitModel contains the
orbit dynamics of multiple planets.

@author: Ben Frey
"""
import Physics as phys
import Solver as slv
import Body as bd
import numpy as np

class Model(object):
    """To be extended by another sub class, composite of multiple objects"""
    def __init__(self,physics,bodies,time=0):
        self.bodies = bodies
        self.physics = physics
        self.time = time
        
    def advance(self,t):
        """ Advance the all of the bodies in the model by one timestep.

        Parameters
        ----------
        t : float
            Time to advance the model to.
        
        Returns
        -------
        Float of time after advance, updated list of bodies.
        """
        for i in range(len(self.bodies)):
            # Planet object advancement
            currentBody = self.bodies[i]
            tn, self.bodies[i] = self.physics.advance(self.time,currentBody,t)
        self.time = tn
        return tn, self.bodies
    
class OrbitModel(Model):
    """Takes in list of semi major axis, eccentricities, initiates a
    Gravity class, then creates grav body classes for each planet.
    
    Attributes
    ----------
    aList : list of floats
        Semi-major axis list.
    eList : list of floats
        List of eccentricities of the orbit.
    masses : list of floats
        Solar mass of each object
    names : list of strings
        Names for each object
    """    
    def __init__(self,aList,eList,masses,names):
        # Create list of bodies and associated dictionary.
        bodies = []
        dic = {}
        for i in range(len(aList)):            
            # Get constants from instantiated grav class.
            G = 4*np.pi**2
            gravParam = G*1 # One solar mass for mass of sun.
            parahelionDist = aList[i]*(1-eList[i]) 
            
            # Calculate velocity (entire magnitude in y direction) at
            # perihelion distance. This is where planet will start.
            weirdTerm = (1+eList[i])/(1-eList[i])
            yVel = np.sqrt(gravParam*1*weirdTerm/aList[i])

            # Create the new body.
            newBody = bd.GravBody(parahelionDist, 0.0, 0.0, 0.0, yVel, 0.0, masses[i])
            bodies.append(newBody)
            dic[names[i]] = newBody
            
        # Instantiate a CentralGravity class for specific orbit.            
        RK4 = slv.RK4()  
        # Dynamic Gravity Solver
        grav = phys.CentralGravity(RK4)
        
        # Set the dictionary for the instance (names) and push all init
        # info to the super class, which has the advance function we want
        # to use.
        self.dic = dic
        super().__init__(grav,bodies)
        
    def get_body(self,name):
        """Returns a body for a specified planet name.

        Parameters
        ----------
        name : string
            Name of planet.
            
        Returns
        -------
        GravBody for associated planet.
        """
        return self.dic[name];
    
    def total_energy(self,name):
        """Returns the total energy for a planet at a given position in orbit.
        
        Parameters
        ----------
        name : string
            Name of planet.

        Returns
        -------
        Tot energy of planet (U and KE).
        """
        p = self.get_body(name)
        pMass = p.state[6]
        rad = p.pos
        v = p.vel
        GM = 4*np.pi**2
        pot = GM*pMass/rad
        ke = 0.5*pMass*v**2
        return pot+ke
    
class SolarSystemModel(OrbitModel):
    """Represents and instance of an OrbitModel 
    object with the bodies (planets): Mercury, Venus, Earth, Mars, Comet.
    
    Returns
    -------
    None.
    """
    def __init__(self):
        # Planet names
        names = ["Mercury","Venus","Earth","Mars","Comet"]
        # List of semi-major axis
        aList = [0.3871, 0.7233, 1.0, 1.5273, 3.0]
        # List of eccentricities
        eList = [0.206, 0.007, 0.017, 0.093, 0.9]
        # List of masses
        nonadjust = [0.17, 2.44, 3.00, 0.32, 1]
        masses = [element * (10**(-6)) for element in nonadjust]
        
        super().__init__(aList, eList, masses, names)
        
        self.mercury = self.get_body("Mercury")
        self.venus = self.get_body("Venus")
        self.earth = self.get_body("Earth")
        self.mars = self.get_body("Mars")
        self.comet = self.get_body("Comet")

class EnragedAvian(Model):
    """Takes in list of semi major axis, eccentricities, initiates a
    Gravity class, then creates grav body classes for each planet.
    
    Attributes
    ----------
    aList : list of floats
        Semi-major axis list.
    eList : list of floats
        List of eccentricities of the orbit.
    masses : list of floats
        Solar mass of each object
    names : list of strings
        Names for each object
    
    """
    def __init__(self, avianPos, avianVel, porcinePos):
        # Single Avian
        self.avian = bd.GravBody(avianPos[0], avianPos[1], avianPos[2], avianVel[0], avianVel[1], avianVel[2], 1.0)
        # Porcine
        self.porcinePos = porcinePos
        
        # Instantiate a CentralGravity class for specific orbit.            
        RK4 = slv.RK4()  
        # Dynamic Gravity Solver
        grav = phys.CentralGravity(RK4)
        
        super().__init__(grav, [self.avian])

        
    def distance(self):
        avianPos = self.avian.state[0:3]
        
        return np.linalg.norm(np.subtract(self.porcinePos,avianPos))
    
    
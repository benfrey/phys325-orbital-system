# -*- coding: utf-8 -*-
"""
The Physics base class and its children
This set of classes implements various differential equations that represent
different physical environments.  They are intended for use with the
differential equation solving classes derived from Solver.
"""
import numpy as np
import Vector

class Physics():
    """Base class for Physics objects.

    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation

    """
    def __init__(self,solver,dt_max=0.001):
        """To be extended by Physics subclass"""
        self.solver = solver
        self.dt_max = dt_max
        
    def advance(self,t,body,dt):
        """Advance the body one time step

        This advance implementation in the Physics base class is a stub.
        It exists only to define the interface for the advance method.
        Classes derived from Physics should define their own versions of
        advance following the same interface.

        Parameters
        ----------
        t : float
            The current time
            
        body : Body
            An instance of a class derived from Body
            
        dt : float
            The amount of time to advance. (the time step)

        Returns
        -------
        time : float
            The new time
        body : Body
            The body advanced one time step
        """
        while np.abs(dt) > 0:
            if np.abs(dt) > self.dt_max:
                step = self.dt_max*np.sign(dt)
            else:
                step = dt
            t, body.state = self.solver.advance(t,body.state,step)
            dt = dt - step
        return t, body

    def diff_eq(self,t,T):
        """The cooling differential equation

        This diff_eq implementation in the Physics base class is a stub.
        It exists only to define the interface for the advance method.
        Classes derived from Physics should define their own versions of
        advance following the same interface.

        Parameters
        ----------
        T : float
            The current temperature of the object

        t : float
            The current time

        Returns
        -------
        dTdt : float
            The slope at T
        """
        print("Physics.diff_eq is a stub!  This line should never be executed")
        return          # Do nothing, simply return.

class Cooling(Physics):
    """Implements cool cooling.

    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation

    Ta : float
        The ambient temperature

    k : float
        The cooling coefficient
    """
    def __init__(self,solver,Ta,k):
        self.solver = solver
        self.Ta = Ta
        self.k = k
        self.dt_max = super.dt_max
        super().__init__(solver)

        # Solver's physics instance is this instance of physics (cooling).
        self.solver.physics = self
        
    def diff_eq(self,t,T):
        """See class Physics for full docstring"""
        k = self.k
        Ta = self.Ta
        return k*(Ta-T)
    
class CentralGravity(Physics):
    """Implements changing gravity (dependent on distance). Based on the
    equaiton for gravity as a function of radius between objects, and the
    Gravity paramater.

    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation
    gravConstant : float
        Gravitational constant in terms of a solar masses, distance in AU and 
        time in years.
    planetMass : float
        Mass of planet in solar masses.
    """
    
    def __init__(self,solver,planetMass=1,gravConstant=(4*np.pi**2)):
        self.solver = solver
        self.G = gravConstant
        self.M = planetMass
        super().__init__(solver)
    
        # I am who i am physics thinks they are... Jk
        # Solver's physics instance is this instance of physics 
        # (CentralGravity).
        self.solver.physics = self
        
    def diff_eq(self,t,f):
        """See class Physics for full docstring, Computes diff eq for 6 eq."""
        # Radius vector to 3/2 power (denom of each diff eq).
        rad = (f[0]**2+f[1]**2+f[2]**2)**(3/2)
        
        # Velcoties
        drxdt = f[3]
        drydt = f[4]
        drzdt = f[5]
        
        # Accelerations
        k = self.G*self.M
        dvxdt = -(k*f[0])/rad
        dvydt = -(k*f[1])/rad
        dvzdt = -(k*f[2])/rad
        
        # Compiled np array of values.
        dfdt = np.array([drxdt,drydt,drzdt,dvxdt,dvydt,dvzdt])
        return dfdt
        
class UniformGravity(Physics):
    """Implements constant gravity.

    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation
    """
    def __init__(self,solver):
        self.solver = solver
        self.g = -9.81
        super().__init__(solver)
  
        # I am who i am.
        self.solver.physics = self
        
    def diff_eq(self,t,f):
        """See class Physics for full docstring"""
        drdt = f[1]
        dvdt = self.g
        dfdt = np.array([drdt,dvdt])
        return dfdt
    
class LogisticPopGrowth(Physics):
    """Implements logistic population growth.

    Attributes
    ----------
    solver : Solver
        An instance of a class derived from Solver to solve the differential
        equation
    r : float
        Population growth rate.
    N : float
        Maximum population.
    """
    
    def __init__(self,solver,r,N):
        self.solver = solver
        self.r = r
        self.N = N
        super().__init__(solver)
  
        # I am who i am.
        self.solver.physics = self
        
    def diff_eq(self,t,P):
        """See class Physics for full docstring"""
        r = self.r
        N = self.N
        return r*P*(1-P/N)
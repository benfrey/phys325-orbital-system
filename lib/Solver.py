# -*- coding: utf-8 -*-
"""
The Solver base class and its children
This set of classes implements various differential equation solving 
algorithms.  They are intended for use with the classes derived from Physics.
"""
import numpy as np

class Solver(object):
    """Differential equation solver base class.
    
    Attributes
    ----------
    physics : Physics 
        A reference to a physics class for access to a differential equation
    """
    
    def __init__(self,physics=None):
        self.physics = physics
                        
    def advance(self,x,f,dx):
        ''' Advance a differential equation one step
        
        This advance implementation in the Solver base class is a stub.
        It exists only to define the interface for the advance method.
        Classes derived from Solver should define their own versions of 
        advance following the same interface.
        
        Parameters
        ----------
        x : float
            The independent variable

        f : float
            The dependent variable(s)
                        
        dx : float
            The distance to advance the independent variable. 
            (ie. the stepsize)
            
        Returns
        -------
        xnext : float
            The value of the independent variable at the next step

        fnext : float
            The value of the dependent variable at the next step            
        '''
        print("Solver.advance is a stub!  This line should never be executed")
        return          # Do nothing, simply return.
    
class Euler(Solver):
    """Euler's technique for differential equation solving"""
            
    def advance(self,x,f,dx):
        """See class Solver for full docstring"""
        xnext = x + dx
        fnext = f + self.physics.diff_eq(x,f)*dx
        return xnext, fnext

class RK2(Solver):
    """Runge-Kutta 2nd order technique for differential equation solving"""
    
    def advance(self,x,f,dx):
        """See class Solver for full docstring
        
        k1 = G(Xn, f(Xn))
        k2 = G(Xn+dX/2, f(Xn)+k1*dX/2)
        f(Xn+1) = f(Xn) + k2*dx
        """
        xnext = x + dx
        k1 = self.physics.diff_eq(x, f)
        k2 = self.physics.diff_eq(x+0.5*dx,f+0.5*k1*dx)
        fnext = f + k2*dx
        return xnext, fnext
    
class RK4(Solver):
    """Runge-Kutta 4th order technique for differential equation solving"""
    
    def advance(self,x,f,dx):
        """See class Solver for full docstring
        
        k1 = G(Xn, f(Xn))*dx
        k2 = G(Xn+dX/2, f(Xn)+k1/2)*dx
        k3 = G(Xn+dX/2, f(Xn)+k2/2)*dx
        k4 = G(Xn+dx,f(Xn)+k3)*dx
        f(Xn+1) = f(Xn) + (1/6)(k1+2k2+2k3+k4)
        """
        # Uh oh, this doesn't seem very modular...
        mass = f[6]
        f=f[:6]
        
        xnext = x + dx
        k1 = self.physics.diff_eq(x, f)
        k2 = self.physics.diff_eq(x+0.5*dx,f+0.5*k1*dx)
        k3 = self.physics.diff_eq(x+0.5*dx,f+0.5*k2*dx)
        k4 = self.physics.diff_eq(x+dx,f+k3*dx)
        fnext = f + (1/6)*(k1+2*k2+2*k3+k4)*dx
        
        #print(dx)
        
        # Or this either...
        fnext = np.append(fnext, mass)
        
        #print(xnext)
        #print(fnext)
        return xnext, fnext
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 08:51:01 2016

@author: gtruch
"""

import Vector as vec
import numpy as np


class GravBodies():
    """A container to hold GravBodies for use with NBody simulations

    Internally stores the GravBody state variables in nx6 matrix to allow
    the use of numpy in nbody simulations.  Individual GravBodys are
    reconstructed on user request.

    Individual GravBodys can be accessed using the normal array notation.
        eg.  if gbods is a GravBodies object:
           gbods[0]       returns the zeroth GravBody

           gbods[1:5]     returns a GravBodies object containing four
                          GravBodys

           gbods["Mars"]  returns the GravBody named "Mars" if one was
                          assigned

    GravBodies can also store objects that inherit GravBody.  Attributes of the
    child class can be accessed by accessing the individual objects in the
    collection.  For example, if a new ChromaBody class that has a 'color'
    attribute were derived from GravBodies, the color attribute could be
    accessed as:
        gbods[3].color

    Attributes
    ----------
    bodies : list of GravBodys
        All of the GravBodys in the system in a list.

    names : list of str
        The names of the GravBodys in the system in a list.

    x,y,z : array of floats
        An array containing the x,y, or z cartesian components of the
        positions of all of the bodies

    r,theta,phi : array of floats
        An array containing the r,theta, or phi spherical components of the
        positions of all of the bodies

    position : list of Vectors
        The positions of the bodies as a list of Vectors

    vx,vy,vz : array of floats
        An array containing the x,y, or z cartesian components of the
        velocities of all of the bodies

    vr,vtheta,vphi : array of floats
        An array containing the r,theta, or phi spherical components of the
        velocities of all of the bodies

    velocity : list of Vectors
        The velocities of the bodies as a list of Vectors

    mass : array of floats
        The masses of the bodies

    state : nx6 matrix of floats
        A matrix containing the state of each body in the system.
        Each row is a body.
        Columns 0,1,2 are position
        Columns 3,4,5 are velocity
    """

    def __init__(self,bodies,names=None):
        """Initialize the collection

        Parameters
        ----------
        bodies : list of GravBodies
            A list of gravbodies to add to the collection

        names : optional, list of strings
            A list of strings representing the names of the bodies.
            used by the get_by_name and __getitem__ to fetch an individual
            body
            Names defaults to body<n> where <n> is the index of the body
        """

        # Keep a reference to the original gravbodies
        self._bodies = [b for b in bodies]

        # Build the state array
        self.state = np.array([b.state for b in bodies])

        # Save the masses
        self.mass = np.array([b.mass for b in bodies])

        # Build a dictionary of names and associated state matrix index
        # for name based lookups
        if names is not None:
            self._dict = { name : i for i,name in enumerate(names) }
        else:
            self._dict = {"body%d"%i : i for i in range(len(self)) }

        return

    @property
    def x(self):
        return self.state[:,0]

    @property
    def y(self):
        return self.state[:,1]

    @property
    def z(self):
        return self.state[:,2]

    @property
    def r(self):
        return np.array([p.r for p in self.position])

    @property
    def theta(self):
        return np.array([p.theta for p in self.position])

    @property
    def phi(self):
        return np.array([p.phi for p in self.position])


    @property
    def vx(self):
        return self.state[:,3]

    @property
    def vy(self):
        return self.state[:,4]

    @property
    def vz(self):
        return self.state[:,5]

    @property
    def vr(self):
        return np.array([v.r for v in self.velocity])

    @property
    def vtheta(self):
        return np.array([v.theta for v in self.velocity])

    @property
    def vphi(self):
        return np.array([v.phi for v in self.velocity])

    @property
    def position(self):
        return [vec.Vector.asArray(c[:3]) for c in self.state]

    @property
    def velocity(self):
        return [vec.Vector.asArray(c[3:]) for c in self.state]

    def add(self,body,name=None):
        """Add a GravBody to the collection

        Parameters
        ----------
        body : GravBody
            The GravBody to add

        name : default, string
            A string describing the name of the GravBody.
            default = None (no dictionary entry will be added)
        """

        # Add a new row to the state matrix
        self.state = np.vstack((self.state,body.state))
        self.mass  = np.append(self.mass,body.mass)

        # Add a new entry to the dictionary
        if name is None:
            name = "body"%(len(self)-1)
        self._dict[name] = len(self)-1

        # Append the original body to the bodies list.
        self._bodies.append(body)

    def pop(self,index):
        """Remove a GravBody from the collection based on index or name

        Removes the row from the state matrix and the entry from the
        dictionary.  The indices of all GravBodys following the removed
        GravBody will change.

        Parameters
        ----------
        index : int
            The index of the GravBody to be removed.
        """

        if isinstance(index,str):
            index = self._dict[index]

        # Save a copy of the GravBody to return
        ret = self[index]

        # Remove the appropriate row from the state matrix
        self.state = np.delete(self.state,index,axis=0)

        # Remove the mass entry
        self.mass = np.delete(self.mass,index)

        # Scan the dictionary to remove the desired element and update the
        # indices
        for name in list(self._dict.keys()):

            # Delete the appropriate entry
            if self._dict[name] == index:
                self._dict.pop(name)

            # Decrease the index of any entries greater than the current index
            elif self._dict[name] > index:
                self._dict[name] -= 1

        # Remove the gravbody from the bodies list
        self._bodies.pop(index)

        return ret


    @property
    def bodies(self):
        return [b for b in self]

    def __getitem__(self,index):
        """Use indexing notation to fetch GravBodys"""

        # Handle slicing
        if isinstance(index,slice):

            # Update the states
            for i in np.arange(index.start,index.stop,index.step):
                self._bodies[i].state = self.state[i,:]

            # Build a new GravBodies instance
            names = list(self._dict.keys())
            return GravBodies(self._bodies[index],
                              names=names[index])

        # Handle dictionary lookups
        if isinstance(index,str):
            index = self._dict[index]

        # Update the state
        self._bodies[index].state = self.state[index,:]

        return self._bodies[index]

    def __setitem__(self,index,body):
        """Update a body"""

        # Have to implement slicing on the lhs someday...
        if isinstance(index,slice):
            raise ValueError("Sorry, __setitem__ "
                             "slicing is not yet implemented")

        # Handle dictionary lookups
        if isinstance(index,str):
            index = self._dict[index]

        # Set the appropriate row of the state matrix
        self.state[index,:] = body.state
        self._bodies[index] = body

    def __iter__(self):

        # Allow iteration over the collection
        for i,b in enumerate(self._bodies):
            b.state = self.state[i,:]
            yield b


    def __len__(self):
        return self.state.shape[0]

    def __repr__(self):
        return repr(self.bodies)


class GravBody():
    """An object that has a mass, position, and velocity

    Attributes
    ----------
    x,y,z : float
        The cartesian components of the body's position

    position : Vector
        The position of the body as a Vector

    vx,vy,vz : float
        The cartesian components of the body's velocity

    velocity : Vector
        The velocity of the body as a Vector

    mass : float
        The mass of the body

    state : array of floats
        The state of the gravbody (position and velocity) as an array
        state[0] = x, state[1] = y, state[2] = z
        state[3] = vx, state[4] = vy, state[5] = vz
    """

    def __init__(self, pos, vel, mass=1.0, state=None):

        if state is None:
            self.state = np.array([pos.x,pos.y,pos.z,vel.x,vel.y,vel.z])
        else:
            self.state = state

        self.mass = mass

    @property
    def x(self):
        return self.state[0]

    @x.setter
    def x(self,val):
        self.state[0] = val

    @property
    def y(self):
        return self.state[1]

    @y.setter
    def y(self,val):
        self.state[1] = val

    @property
    def z(self):
        return self.state[2]

    @z.setter
    def z(self,val):
        self.state[2] = val

    @property
    def r(self):
        return self.position.r

    @r.setter
    def r(self,r):
        pos = self.position
        pos.r = r
        self.pos = pos

    @property
    def theta(self):
        return self.position.theta

    @theta.setter
    def theta(self,theta):
        pos = self.position
        pos.theta = theta
        self.pos = pos

    @property
    def phi(self):
        return self.position.phi

    @phi.setter
    def phi(self,phi):
        pos = self.position
        pos.phi = phi
        self.pos = pos

    @property
    def vx(self):
        return self.state[3]

    @vx.setter
    def vx(self,val):
        self.state[3] = val

    @property
    def vy(self):
        return self.state[4]

    @vy.setter
    def vy(self,val):
        self.state[4] = val

    @property
    def vz(self):
        return self.state[5]

    @vz.setter
    def vz(self,val):
        self.state[5] = val

    @property
    def vr(self):
        return self.velocity.r

    @vr.setter
    def vr(self,vr):
        vel = self.velocity
        vel.r = vr
        self.velocity = vel

    @property
    def vtheta(self):
        return self.velocity.theta

    @vtheta.setter
    def vtheta(self,vtheta):
        vel = self.velocity
        vel.theta = vtheta
        self.velocity = vel

    @property
    def vphi(self):
        return self.velocity.phi

    @vphi.setter
    def vphi(self,vphi):
        vel = self.velocity
        vel.phi = vphi
        self.velocity = vel

    @property
    def position(self):
        return vec.Vector.asArray(self.state[0:3])

    @position.setter
    def position(self,value):
        self.state[0:3] = np.array([value.x,value.y,value.z])

    @property
    def velocity(self):
        return vec.Vector.asArray(self.state[3:])

    @velocity.setter
    def velocity(self,value):
        self.state[3:] = np.array([value.x,value.y,value.z])

    def __repr__(self):
        return ("GravBody(postion=" + repr(self.position) +
                     ", velocity=" + repr(self.velocity) +
                     ", mass=" + repr(self.mass) + ")")


class ThermalBody(object):
    """An object that has temperature

    Attributes
    ----------
    temperature : float
        The current temperature of the object
    """

    def __init__(self,temperature):
        self.temperature = temperature
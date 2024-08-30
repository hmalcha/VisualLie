#!/usr/bin/env python3

# This file is part of VisualLie.
#
# Copyright (C) 2024 Hannes Malcha 
#
# VisualLie is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# VisualLie is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with VisualLie.  If not, see <https://www.gnu.org/licenses/>.
#
#
# This class is an exact copy of the Root class from the SimpLie programm
# written by Teake Nutma, which is available at
# https://github.com/teake/simplie.

"""
VisualLie is a web app to visualize the root system of the Feingold-Frenkel
algebra.

This class is part of the rootsystem package that constructs the root system 
of the Feingold-Frenkel algebra up to a given height.

This class store root information.
"""

import numpy as np

class Root:
    """
    A class for storing root information.
    
    Attributes:
        vector: The oot vector
        mult: The root multiplicity
        co_mult: The co-multiplicity of the root
        norm: The norm of the root
    """
    
    def __init__(self, root_vector):
        """
        Initialize a new root from a given root vector.
        
        The attributes initialize to 0 or None and have
        to be assigned manually".
        """
        
        self.vector = root_vector.copy()
        self.mult = 0
        self.co_mult = None
        self.norm = 0
    
        
    def height(self):
        """Return the height of the root."""
        return np.sum(self.vector)
    

    def highest(self):
        """Return the highest (biggest) component of the root vector."""
        return np.max(self.vector)
    
    
    def div(self, factor):
        """
        Divide the root vector with an integral value and return a new
        root with that vector.
        """
        
        _new_vector = np.zeros_like(self.vector, dtype=int)
        
        for i in range(len(self.vector)):
            if self.vector[i] % factor != 0:
                return None
            else:
                _new_vector[i] = self.vector[i] // factor
        
        return Root(_new_vector)
    
    
    def times(self, factor):
        """
        Multiply the root vector with an integral value and return
        a new root with that vector.
        """
        
        _new_vector = np.zeros(len(self.vector), dtype=int)
        
        for i in range(len(self.vector)):
            _new_vector[i] = self.vector[i] * factor
            
        return Root(_new_vector)
    
    
    def __eq__(self, other):
        """
        Override the default equals() function.
        Roots are equal if their root vectors are equal.
        """
        
        if self is other:
            return True
        if other is None or type(other) is not type(self):
            return False 
        _compare_root = other
        if len(self.vector) != len(_compare_root.vector):
            return False
        for i in range(len(self.vector)):
            if self.vector[i] != _compare_root.vector[i]:
                return False  
        return True

    
    def __hash__(self):
        """Return a hashcode based on the vector of the root."""
        _hash_val = 0
        _length = len(self.vector)
    
        for i in range(_length):
            # Left shift hash value by 1
            _hash_val <<= 1
            if _hash_val < 0:
                # Set the least significant bit to 1
                _hash_val |= 1
            # XOR with the current element
            _hash_val ^= self.vector[i]
    
        return int(_hash_val)
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
# This class is based on the Algebra class from the SimpLie programm written
# by Teake Nutma, which is available at https://github.com/teake/simplie.
# 
# Changes from the original:
# - Specialized to the Feingold-Frenkel algebra F
# - The class does not require a Cartan matrix as an input
# - Removed a number of symbols and functions that are not relevant to
#   constructing the root system of F 

"""
VisualLie is a web app to visualize the root system of the Feingold-Frenkel
algebra.

This class is part of the rootsystem package that constructs the root system
of the Feingold-Frenkel algebra up to a given height.

This class creates an object which has most properties of the Feingold-Frenkel
algebra F.
"""

import numpy as np

class Feingold_Frenkel_Algebra:
    """
    Feingold_Frenkel_Algebra stores information on the Feingold-Frenkel algebra F.
    
    Attributes:
        cartan_matrix: The Cartan matrix of F
        rank: The rank of F
    """
    
    
    def __init__(self):
        """Initializes Feingold_Frenkel_Algebra."""   
        self.cartan_matrix = np.array([[2,-1,0],[-1,2,-2],[0,-2,2]])
        self.d = np.diag([1,1,1])
        self.rank = 3
        self.finite = False
        self.metric = np.dot(self.cartan_matrix, self.d)
     
        
    def inner_product(self, root_1, root_2):
        """Computes the inner product of root_1 and root_2."""
        
        return np.dot(root_1.vector , np.dot(self.metric, root_2.vector))
    
    
    def root_to_weight(self, root_vector):
        """Computes the weight vector of a root."""
        return np.dot(root_vector, self.cartan_matrix)
        
        
    def simp_weyl_refl_root(self, root_vector, i):
        """
        Computes a simple Weyl reflection of a root
        
        Keyword arguments:
            root_vector: The root vector to reflect
            i: The index of the simple root with respect to which we reflect.
        """
        
        # Do not reflect for imaginary simple roots.
        if self.cartan_matrix[i][i] <= 0:
            return root_vector
        
        _output = root_vector.copy()
        _dynkin_labels = self.root_to_weight(root_vector)

        _output[i] = _output[i] - _dynkin_labels[i]
        
        return _output
    
    
    def rho(self, root):
        """Calculate the action of the Weyl vector on a root."""
        return np.sum(np.dot(root.vector, self.d))
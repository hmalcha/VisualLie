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
# This class is based on the RootSystem class from the SimpLie
# programm written by Teake Nutma, which is available at
# https://github.com/teake/simplie.
#
# Changes from the original:
# - Removed conditional statements for finite dimensional Lie algebras#


"""
VisualLie is a web app to visualize the root system of the Feingold-Frenkel
algebra.

This class is part of the rootsystem package that constructs the root system
of the Feingold-Frenkel algebra up to a given height.

Given an infinite dimensional algebra this class stores its root system.
"""

import numpy as np
from fractions import Fraction
from .root import Root

class Root_System:
    """
    A class for storing the root system of an algebra.
    
    Attributes:
        algebra: The algebra of the root system
        rank: The rank of the algebra
        root_system: The root system itself
        """
    
    
    def __init__(self, algebra):
        """
        Initialize a new root system from a given infinite dimensional algebra.
        
        The root system is automatically constructed up to height 1.
        """
        
        self.algebra = algebra
        self.rank = algebra.rank
        self.root_system = []
        
        # Add the CSA to the root table
        _csa = set()
        _csa_vector = np.zeros(self.rank, dtype=int)
        _csa_root = Root(_csa_vector)
        _csa_root.mult = self.rank
        _csa_root.co_mult = Fraction(0)
        _csa_root.norm = 0
        _csa.add(_csa_root)
        self.root_system.append(_csa)
        
        # Stop the construction if the algebra has rank 0
        if self.rank == 0:
            return
            
        # Add the simple roots
        _simple_roots = set()
        
        for i in range(self.rank):
            # Skip the index if the diagonal element in the 
            # Cartan matrix is not positive
            if self.algebra.cartan_matrix[i][i] <= 0:
                continue
            
            _root_vector = np.zeros(self.rank, dtype=int)
            for j in range(self.rank):
                _root_vector[j] = 1 if i == j else 0
                
            _simple_root = Root(_root_vector)
            _simple_root.mult = 1
            _simple_root.co_mult = Fraction(1)
            _simple_root.norm = self.algebra.d[i] * self.algebra.cartan_matrix[i][i]
            _simple_roots.add(_simple_root)
           
        
        self.root_system.append(_simple_roots)
        
        # Set the construction height to 1
        self._constructed_height = 1
        self._fully_constructed = False
        
        # Define the lists of the root multiples
        self._root_multiples = []
        self._root_multiples.append([])
        self._root_multiples.append([])
        
        # If the algebra is finite, we can construct the root system to all heights.
        if self.algebra.finite:
            construct(0)  

    def constructed_height(self):
        """Return the height to which we so far have constructed the root system."""
        return self._constructed_height
    
        
    def _get_root_mult_vector(self, vector):
        """Get the root multiplicity by its root vector."""
        _vector = np.absolute(vector)
        return self._get_root_mult(Root(_vector))


    def _get_root_mult(self, root_to_get):
        """Get the root multiplicity."""
        _root_height = root_to_get.height()
        _roots = set()
        
        if _root_height < 0:
            return 0
        
        # If we haven't constructed the roots system this far, do so now
        if _root_height > self._constructed_height and not self._fully_constructed:
            self.construct(_root_height)
            
        # Try to fetch the root
        if len(self.root_system) > _root_height:
            _roots = self.root_system[_root_height]
            if root_to_get in _roots:
                for root in _roots:
                    if root_to_get == root:
                        return root.mult
                    
        #The root is not in the root system, so return null 
        return 0
     
     
    def write_txt_file(self, file_path_and_name):
        """Write the root system constructed thus far to a text file."""    
        _output = np.zeros(4, dtype=int)
    
        # Iterate through the root system and append the sorted roots
        # to the output
        for subset in self.root_system[:self._constructed_height+1]:
            _new_block = np.zeros(4, dtype=int)
            for root in subset:
                _new_row = np.append(root.vector, root.mult)
                _new_block = np.vstack((_new_block, _new_row))
            _new_block = np.array(sorted(_new_block[1:].tolist()))
            _output = np.vstack((_output, _new_block))

        try:
            np.savetxt(file_path_and_name, _output[2:], fmt='%d', delimiter=',')
        except IOError:
            print("The file could not be written!")


    def construct(self, max_height):
        """Construct the root system up to the given height."""
        
        # If the root system is already fully constructed, just do nothing and return.
        if self._fully_constructed or (not self.algebra.finite and max_height == 0) or self.rank == 0:
            return
        
        
        while(self._constructed_height < max_height or max_height == 0):
            _prev_roots = self.root_system[self._constructed_height]
            _next_height = self._constructed_height + 1
            
            # First determine all the possible new roots
            for root in _prev_roots:
                _dynkin_labels = self.algebra.root_to_weight(root.vector)
                
                for i in range(self.rank):
                    # Only do this for real simple roots.
                    if self.algebra.cartan_matrix[i][i] <=0:
                        continue
                    
                    # For every negative Dynkin label we can add 
					# a (partial) root string to the root table
                    if _dynkin_labels[i] >= 0:
                        continue
                    
                    # The root string stops at \gamma = \beta + pMax \alpha_i,
					# with \gamma being the new root, \beta the old, and
					# pMax equal to -p_i
                    _p_max = -1 * _dynkin_labels[i]
                    
                    for j in range(1, _p_max + 1):
                        if len(self.root_system) - 1 < self._constructed_height + j:
                            # This will be the first time this height will be reached,
                            # so create a new container for these roots
                            self.root_system.insert(self._constructed_height + j, set())

                        _new_vector = root.vector.copy()
                        _new_vector[i] =  _new_vector[i] + j
                        _new_root = Root(_new_vector)
                        _new_height = self._constructed_height + j
                        
                        if j == _p_max:
                            # This is the Weyl reflection of the old root
                            # Thus they have the same multiplicity
                            _new_root.mult = root.mult
                            # The other multiplicities will be calculated below
                            
                        #  Add the new root to the root table if it isn't there already
                        _new_roots = self.root_system[_new_height]
                        
                        if _new_root not in _new_roots:
                            _new_root.norm = self.algebra.inner_product(_new_root, _new_root)
                            _new_roots.add(_new_root)
            
            if _next_height > len(self.root_system) - 1:
                # We did nothing, and thus reached the highest root
				# Make a note that we constructed the root system fully, and return
                self._fully_constructed = True
                return
                            
            # Calculate the co_mult and the mult for
            # all the added roots at the first new height
            _new_roots = self.root_system[_next_height]
            
            for root in _new_roots:
                # Determine the co_mult minus the root multiplicity
                _co_mult = self._calculate_co_mult(root)
                
                # Only calculate the mult is it hasn't been set before
                if root.mult == 0:
                    # First try to get the multiplicity from another root in 
					# this roots Weyl-orbit. We only need to do one simple Weyl-reflection 
					# down, as all the roots below this height have been calculated before.

					# First determine the first positive Dynkin label.
					# We will do a simple Weyl reflection in this index later.
                    _dynkin_labels = self.algebra.root_to_weight(root.vector)
                    _reflect_index = 0
                    _can_reflect = False
                    for _reflect_index in range(self.rank):
                        if _dynkin_labels[_reflect_index] > 0:
                            _can_reflect = True
                            break
                    
                    if _can_reflect:
                        # We can reflect down, so do it
                        _reflected_vector = self.algebra.simp_weyl_refl_root(root.vector, _reflect_index)
                        # Get the multiplicity
                        root.mult = self._get_root_mult_vector(_reflected_vector)
                    else:
                        root.mult = self._calculate_mult(root, _co_mult)
                        
                root.co_mult = _co_mult + Fraction(root.mult)
                
            # Construct all the root multiples of the roots at the new height
            _multiples_list = []
            for i in range(1, int(np.floor(_next_height / 2) + 1)):
                # We're only interested in i's with zero divisor
                if _next_height % i != 0:
                    continue
                        
                _factor = _next_height // i
                _roots = self.root_system[i]
                    
                for root in _roots:
                    _root_multiple = root.times(_factor)
                    # Don't add it if it's already in the 'proper' root list
                    # Else we would count this one double
                    if _root_multiple in _new_roots:
                        continue

                    _root_multiple.co_mult = self._calculate_co_mult(_root_multiple)
                    _multiples_list.append(_root_multiple)
                        
                        
            self._root_multiples.insert(_next_height, _multiples_list)
                
            # Finally bump the constructed height number.
            self._constructed_height += 1


    ################################       
    #                              #
    # Multiplicity functions below #
    #                              #
    ################################ 
     
     
    def _calculate_co_mult(self, root):
        """
        Calculates the "co-multiplicity", i.e. the fractional sum of multiplicities
        of all fractional roots. Used in the Peterson formula.
        """
        
        _co_mult = Fraction(0)
        
        # There are no root multiples if the root is real
        if root.norm > 0:
            return _co_mult
        
        for i in range(2, root.highest() + 1):
            _div_root = root.div(i)
            
            if _div_root is not None:
                _co_mult += Fraction(self._get_root_mult(_div_root),i)
                
        return _co_mult
                    
                                        
            
    # Calculates the multiplicity of a root.
    # Based on the Peterson formula. Note that it is necessary to give the co-multiplicity
	# in advance.
    def _calculate_mult(self, root, co_mult):
        """
        Calculates the multiplicity of a root.
        Based on the Peterson formula. 
        Note that it is necessary to give the co-multiplicity in advance.
        """
  
        _multiplicity = Fraction(0)
        
        # We split the Peterson formula into two symmetric halves
		# plus a remainder if the root height is even
        _half_height = int(np.ceil(root.height() / 2))
        
        for i in range(1, _half_height):
            _multiplicity += self._peterson_part(root, i)
            
        _multiplicity *= 2
        
        if root.height() % 2 == 0:
            _multiplicity += self._peterson_part(root, root.height()//2)
            
        _multiplicity *= Fraction(1,self.algebra.inner_product(root, root) - (2 * self.algebra.rho(root)))
        _multiplicity -= co_mult
        
        # Issue a warning if the multiplicity is not an integer.
        # This usually happens as soon as one of the co-multiplicities
        # is of the order 2^64.
        # At the moment there is no fix for this.
        # One should not trust the root system for heights at which
        # the warning message is issued.
        # Currently this height is 84.
        if not _multiplicity.is_integer():
            print("WARNING: Mult of root " + str(root.vector) + " is not an int but " + str(_multiplicity) + "." )
        
        # Return the multiplicity as an integer
        return round(_multiplicity)
                

    def _peterson_part(self, root, height):
        """
        Calculate a part of the Peterson formula.
        
        That is the r.h.s for a given value of the height
        of one of the decomposition parts.
        """
        
        _betas = self.root_system[height]
        _gammas = self.root_system[root.height() - height]

        _multiplicity = self._peterson_sub_part(root, _betas, _gammas)
        
        _beta_multiples = self._root_multiples[height]
        _gamma_multiples = self._root_multiples[root.height() - height]
        
        _multiplicity += self._peterson_sub_part(root, _beta_multiples, _gamma_multiples)
        _multiplicity += self._peterson_sub_part(root, _betas, _gamma_multiples)
        _multiplicity += self._peterson_sub_part(root, _beta_multiples, _gammas)
        
        return _multiplicity
    
    
    def _peterson_sub_part(self, root, list_1, list_2):
        """
        Calculate a part of the r.h.s of the Peterson formula
        for a root from two given lists of roots.
        
        Keyword arguments:
            root: The root for which we compute the multiplicity
            list_1: The first list of roots that is used in the r.h.s
                    of the Peterson formula.
            list_2: The second list of roots that is used in the r.h.s
                    of the Peterson formula.
        """
        
        _multiplicity = Fraction(0)
        for beta in list_1:
            for gamma in list_2:
                for i in range(self.rank):
                    if beta.vector[i] + gamma.vector[i] != root.vector[i]:
                        break
                else:
                    _part = (beta.co_mult) * (gamma.co_mult)
                    _part *= Fraction(self.algebra.inner_product(beta, gamma))
                    _multiplicity += _part

        return _multiplicity



#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  PyFiVol - Python-based finite volume PDE solver
 # 
 #  FILE: "array.py"
 #                                    created: 1/10/04 {10:23:17 AM} 
 #                                last update: 1/16/04 {12:16:56 PM} 
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  PFM is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  See the file "license.terms" for information on usage and  redistribution
 #  of this file, and for a DISCLAIMER OF ALL WARRANTIES.
 #  
 # ###################################################################
 ##

import Numeric
import umath

import fivol.variables.variable
import fivol.tools.dimensions.physicalField

def _isPhysical(arr):
    return isinstance(arr,fivol.variables.variable.Variable) \
	or isinstance(arr,fivol.tools.dimensions.physicalField.PhysicalField)
	
def take(arr, ids):
    if _isPhysical(arr):
	return arr.take(ids)
    
    elif type(arr) is type(Numeric.array((0))):
	return Numeric.take(arr, ids)
    else:
	raise TypeError, 'cannot take from object ' + str(arr)
    
def reshape(arr, shape):
    if _isPhysical(arr):
	return arr.reshape(shape)
    elif type(arr) is type(Numeric.array((0))):
	return Numeric.reshape(arr, shape)
    else:
	raise TypeError, 'cannot reshape object ' + str(arr)
	
def sum(arr, index = 0):
    if _isPhysical(arr):
	return arr.sum(index)
    elif type(arr) is type(Numeric.array((0))):
	return Numeric.sum(arr, index)
    else:
	raise TypeError, 'cannot sum object ' + str(arr)

def sqrt(arr):
    if _isPhysical(arr):
	return arr.sqrt()
    elif type(arr) is type(Numeric.array((0))):
	return Numeric.sqrt(arr)
    else:
	return umath.sqrt(arr)
	
def tan(arr):
    if _isPhysical(arr):
	return arr.tan()
    elif type(arr) is type(Numeric.array((0))):
	return Numeric.tan(arr)
    else:
	return umath.tan(arr)

def arctan(arr):
    if _isPhysical(arr):
	return arr.arctan()
    elif type(arr) is type(Numeric.array((0))):
	return Numeric.arctan(arr)
    else:
	return umath.arctan(arr)
		
def arctan2(arr, other):
    if _isPhysical(arr):
	return arr.arctan2(other)
    elif _isPhysical(other):
	return physicalField.PhysicalField(value = arr, unit = "rad").arctan2(other)
    elif type(arr) is type(Numeric.array((0))):
	return Numeric.arctan2(arr,other)
    else:
	return umath.arctan2(arr,other)
	

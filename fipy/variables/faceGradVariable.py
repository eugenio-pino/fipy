#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  PyFiVol - Python-based finite volume PDE solver
 # 
 #  FILE: "faceGradVariable.py"
 #                                    created: 12/18/03 {2:52:12 PM} 
 #                                last update: 2/2/04 {2:52:19 PM}
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

from fivol.variables.vectorFaceVariable import VectorFaceVariable
from fivol.tools import array
from fivol.inline import inline

class FaceGradVariable(VectorFaceVariable):
    def __init__(self, var):
	VectorFaceVariable.__init__(self, var.getMesh())
	self.var = self.requires(var)

    def calcValue(self):        
	inline.optionalInline(self._calcValueInline, self._calcValue)
    
    def _calcValue(self):
    
        dAP = self.mesh.getCellDistances()
	id1, id2 = self.mesh.getAdjacentCellIDs()
##	N = self.mod(array.take(self.var,id2) - array.take(self.var,id1)) / dAP
	N = (array.take(self.var,id2) - array.take(self.var,id1)) / dAP
	normals = self.mesh.getOrientedFaceNormals()
	
	tangents1 = self.mesh.getFaceTangents1()
	tangents2 = self.mesh.getFaceTangents2()
	cellGrad = self.var.getGrad().getNumericValue()
        
	grad1 = array.take(cellGrad,id1)
	grad2 = array.take(cellGrad,id2)
	t1grad1 = array.sum(tangents1*grad1,1)
	t1grad2 = array.sum(tangents1*grad2,1)
	t2grad1 = array.sum(tangents2*grad1,1)
	t2grad2 = array.sum(tangents2*grad2,1)
	
	T1 = (t1grad1 + t1grad2) / 2.
	T2 = (t2grad1 + t2grad2) / 2.
	
	N = N[:,Numeric.NewAxis]
	T1 = T1[:,Numeric.NewAxis]
	T2 = T2[:,Numeric.NewAxis]

	self.value = normals * N + tangents1 * T1 + tangents2 * T2

    def _calcValueInline(self):
        
	id1, id2 = self.mesh.getAdjacentCellIDs()
        
	inline.runInlineLoop1("""
	int j;
	double t1grad1, t1grad2, t2grad1, t2grad2, N;

	N = (var(id2(i)) - var(id1(i))) / dAP;

	t1grad1 = t1grad2 = t2grad1 = t2grad2 = 0.;

	for (j = 0; j < nj; j++) {
	    t1grad1 += tangents1(i,j) * cellGrad(id1(i),j);
	    t1grad2 += tangents1(i,j) * cellGrad(id2(i),j);
	    t2grad1 += tangents2(i,j) * cellGrad(id1(i),j);
	    t2grad2 += tangents2(i,j) * cellGrad(id2(i),j);
	}
	
	for (j = 0; j < nj; j++) {
	    val(i,j) = normals(i,j) * N;
	    val(i,j) += tangents1(i,j) * (t1grad1 + t1grad2) / 2.;
	    val(i,j) += tangents2(i,j) * (t2grad1 + t2grad2) / 2.;
        }""",tangents1 = mesh.getFaceTangents1(),
                              tangents2 = self.mesh.getFaceTangents2(),
                              cellGrad = self.var.getGrad().getNumericValue(),
                              normals = self.mesh.getOrientedFaceNormals(),
                              id1 = id1,
                              id2 = id2,
                              dAP = self.mesh.getCellDistances(),
                              val = self.value.value,
                              ni = tangents1.shape[0],
                              nj = tangents1.shape[1])

    

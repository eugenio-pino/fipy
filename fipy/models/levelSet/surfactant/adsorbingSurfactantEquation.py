#!/usr/bin/env python

## 
 # -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "adsorbingSurfactantEquation.py"
 #                                    created: 8/31/04 {10:39:23 AM} 
 #                                last update: 2/18/05 {10:44:37 AM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
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
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-12 JEG 1.0 original
 # ###################################################################
 ##

r"""

The `AdsorbingSurfactantEquation` object solves the
`SurfactantEquation` but with an adsorbing species from some bulk
value. The equation that describes the surfactant adsorbing is given
by,

.. raw:: latex

    $$ \dot{\theta} = J v \theta + k c (1 - \theta) $$

This last term in this equation accounts for Langmuir type adsorption
from the bulk. It assumes a vacant proportion of surface sites. The adsorption term
is added to the source by setting

.. raw:: latex

    $ S_c = k c $ and $ S_p = k c $.

The following is a test case:

   >>> from fipy.models.levelSet.distanceFunction.distanceVariable import DistanceVariable
   >>> from fipy.models.levelSet.surfactant.surfactantVariable import SurfactantVariable
   >>> from fipy.meshes.grid2D import Grid2D
   >>> dx = .5
   >>> dy = 2.3
   >>> dt = 0.25
   >>> k = 0.56
   >>> initialValue = 0.1
   >>> c = 0.2
   >>> mesh = Grid2D(dx = dx, dy = dy, nx = 5, ny = 1)
   >>> distanceVar = DistanceVariable(mesh = mesh, 
   ...                                value = (-dx*3/2, -dx/2, dx/2, 3*dx/2 ,5*dx/2))
   >>> surfactantVar = SurfactantVariable(value = (0, 0, initialValue, 0 ,0), 
   ...                                    distanceVar = distanceVar)
   >>> bulkVar = CellVariable(mesh = mesh, value = (c , c, c, c, c))
   >>> eqn = AdsorbingSurfactantEquation(surfactantVar = surfactantVar,
   ...                                   distanceVar = distanceVar,
   ...                                   bulkVar = bulkVar,
   ...                                   rateConstant = k)
   >>> eqn.solve(surfactantVar, dt = dt)
   >>> answer = (initialValue + dt * k * c) / (1 + dt * k * c)
   >>> Numeric.allclose(surfactantVar.getInterfaceVar(), Numeric.array((0, 0, answer, 0, 0)))
   1

The following test case is for two surfactant variables. One has more
surface affinity than the other.

   >>> from fipy.models.levelSet.distanceFunction.distanceVariable import DistanceVariable
   >>> from fipy.models.levelSet.surfactant.surfactantVariable import SurfactantVariable
   >>> from fipy.meshes.grid2D import Grid2D
   >>> dx = 0.5
   >>> dy = 2.73
   >>> dt = 0.001
   >>> k0 = 1.
   >>> k1 = 10.
   >>> theta0 = 0.
   >>> theta1 = 0.
   >>> c0 = 1.
   >>> c1 = 1.
   >>> totalSteps = 100
   >>> mesh = Grid2D(dx = dx, dy = dy, nx = 5, ny = 1)
   >>> distanceVar = DistanceVariable(mesh = mesh, 
   ...                                value = dx * (Numeric.arange(5) - 1.5))
   >>> var0 = SurfactantVariable(value = (0, 0, theta0, 0 ,0), distanceVar = distanceVar)
   >>> var1 = SurfactantVariable(value = (0, 0, theta1, 0 ,0), distanceVar = distanceVar)
   >>> bulkVar0 = CellVariable(mesh = mesh, value = (c0, c0, c0, c0, c0))
   >>> bulkVar1 = CellVariable(mesh = mesh, value = (c1, c1, c1, c1, c1))

   >>> eqn0 = AdsorbingSurfactantEquation(surfactantVar = var0,
   ...                                    distanceVar = distanceVar,
   ...                                    bulkVar = bulkVar0,
   ...                                    rateConstant = k0)

   >>> eqn1 = AdsorbingSurfactantEquation(surfactantVar = var1,
   ...                                    distanceVar = distanceVar,
   ...                                    bulkVar = bulkVar1,
   ...                                    rateConstant = k1,
   ...                                    otherVar = var0,
   ...                                    otherBulkVar = bulkVar0,
   ...                                    otherRateConstant = k0)

   >>> for step in range(totalSteps):
   ...     eqn0.solve(var0, dt = dt)
   ...     eqn1.solve(var1, dt = dt)
   >>> answer0 = 1 - Numeric.exp(-k0 * c0 * dt * totalSteps)
   >>> answer1 = (1 - Numeric.exp(-k1 * c1 * dt * totalSteps)) * (1 - answer0)
   >>> Numeric.allclose(var0.getInterfaceVar(), Numeric.array((0, 0, answer0, 0, 0)), rtol = 1e-2)
   1
   >>> Numeric.allclose(var1.getInterfaceVar(), Numeric.array((0, 0, answer1, 0, 0)), rtol = 1e-2)
   1
   >>> dt = 0.1
   >>> for step in range(10):
   ...     eqn0.solve(var0, dt = dt)
   ...     eqn1.solve(var1, dt = dt)
   >>> print var0.getInterfaceVar()[2] + var1.getInterfaceVar()[2]
   1.0

The following test case is to fix a bug where setting the adosrbtion
coefficient to zero leads to the solver not converging and an eventual
failure.

   >>> var0 = SurfactantVariable(value = (0, 0, theta0, 0 ,0), distanceVar = distanceVar)
   >>> bulkVar0 = CellVariable(mesh = mesh, value = (c0, c0, c0, c0, c0))

   >>> eqn0 = AdsorbingSurfactantEquation(surfactantVar = var0,
   ...                                    distanceVar = distanceVar,
   ...                                    bulkVar = bulkVar0,
   ...                                    rateConstant = 0)

   >>> eqn0.solve(var0, dt = dt)
   >>> eqn0.solve(var0, dt = dt)
   >>> Numeric.allclose(var0.getInterfaceVar()[2], 0)
   1

The following test case is to fix a bug that allos the accelerator to
become negative.

   >>> nx = 5
   >>> ny = 5
   >>> mesh = Grid2D(dx = 1., dy = 1., nx = nx, ny = ny)
   >>> values = Numeric.ones(mesh.getNumberOfCells(), 'd')
   >>> values[0:nx] = -1
   >>> for i in range(ny):
   ...     values[i * nx] = -1

   >>> disVar = DistanceVariable(mesh = mesh, value = values)
   >>> disVar.calcDistanceFunction()

   >>> levVar = SurfactantVariable(value = 0.5, distanceVar = disVar)
   >>> accVar = SurfactantVariable(value = 0.5, distanceVar = disVar)

   >>> levEq = AdsorbingSurfactantEquation(levVar,
   ...                                     distanceVar = disVar,
   ...                                     bulkVar = 0,
   ...                                     rateConstant = 0)

   >>> accEq = AdsorbingSurfactantEquation(accVar,
   ...                                     distanceVar = disVar,
   ...                                     bulkVar = 0,
   ...                                     rateConstant = 0,
   ...                                     otherVar = levVar,
   ...                                     otherBulkVar = 0,
   ...                                     otherRateConstant = 0)

   >>> extVar = CellVariable(mesh = mesh, value = accVar.getInterfaceVar())

   >>> from fipy.models.levelSet.advection.higherOrderAdvectionEquation import buildHigherOrderAdvectionEquation
   >>> advEq = buildHigherOrderAdvectionEquation(advectionCoeff = extVar)

   >>> dt = 0.1

   >>> for i in range(50):
   ...     disVar.calcDistanceFunction()
   ...     extVar.setValue(Numeric.array(accVar.getInterfaceVar()))
   ...     disVar.extendVariable(extVar)
   ...     disVar.updateOld()
   ...     advEq.solve(disVar, dt = dt)
   ...     levEq.solve(levVar, dt = dt)
   ...     accEq.solve(accVar, dt = dt)

   >>> Numeric.sum(accVar < -1e-10) == 0
   1
   
"""

__docformat__ = 'restructuredtext'

import Numeric

from fipy.variables.cellVariable import CellVariable
from surfactantEquation import SurfactantEquation
from fipy.terms.implicitSourceTerm import ImplicitSourceTerm
from fipy.solvers.linearPCGSolver import LinearPCGSolver

class AdsorptionCoeff(CellVariable):
    def __init__(self, distanceVar, bulkVar, rateConstant):
        CellVariable.__init__(self, mesh = distanceVar.getMesh())

        self.distanceVar = self.requires(distanceVar)
        self.bulkVar = self.requires(bulkVar)
        self.rateConstant = rateConstant
        self.dt = 0

    def _calcValue(self):
        self.value = self.dt * Numeric.array(self.bulkVar) * self.rateConstant * self.multiplier()

    def updateDt(self, dt):
        self.dt = dt
        self.markStale()

class AdsorptionCoeffInterfaceFlag(AdsorptionCoeff):
    def multiplier(self):
        return self.distanceVar.getCellInterfaceFlag()
    
class AdsorptionCoeffAreaOverVolume(AdsorptionCoeff):
    def multiplier(self):
        return self.distanceVar.getCellInterfaceAreas() / self.mesh.getCellVolumes()

class MaxCoeff(CellVariable):
    def __init__(self, distanceVar, vars = ()):
        CellVariable.__init__(self, mesh = distanceVar.getMesh())
        self.vars = vars
        for var in self.vars:
            self.requires(var)
        self.distanceVar = self.requires(distanceVar)

    def _calcMax(self):
        total = 0
        for var in self.vars:
            total += Numeric.array(var.getInterfaceVar())
        return Numeric.array(total > 1) * self.distanceVar.getCellInterfaceFlag()

class SpMaxCoeff(MaxCoeff):
    def _calcValue(self):
        self.value = 1e20 * self._calcMax()

class ScMaxCoeff(MaxCoeff):
    def _calcValue(self):
        val = self.distanceVar.getCellInterfaceAreas() / self.mesh.getCellVolumes()
        for var in self.vars[1:]:
            val -= self.distanceVar.getCellInterfaceFlag() * Numeric.array(var)

        self.value = 1e20 * self._calcMax() * Numeric.where(val < 0, 0, val)

class AdsorbingSurfactantEquation(SurfactantEquation):
    def __init__(self,
                 surfactantVar = None,
                 distanceVar = None,
                 bulkVar = None,
                 rateConstant = None,
                 otherVar = None,
                 otherBulkVar = None,
                 otherRateConstant = None,
                 consumptionCoeff = None):

        SurfactantEquation.__init__(self, distanceVar = distanceVar)

        spCoeff = AdsorptionCoeffInterfaceFlag(distanceVar, bulkVar, rateConstant)
        scCoeff = AdsorptionCoeffAreaOverVolume(distanceVar, bulkVar, rateConstant)

        self.eq += ImplicitSourceTerm(spCoeff) - scCoeff

        self.coeffs = (scCoeff, spCoeff)

        if otherVar is not None:
            otherSpCoeff = AdsorptionCoeffInterfaceFlag(distanceVar, otherBulkVar, otherRateConstant)
            otherScCoeff = AdsorptionCoeffAreaOverVolume(distanceVar, -bulkVar * otherVar.getInterfaceVar(), rateConstant)

            self.eq += ImplicitSourceTerm(otherSpCoeff) - otherScCoeff

            self.coeffs += (otherScCoeff,)
            self.coeffs += (otherSpCoeff,)

            vars = (surfactantVar, otherVar)
        else:
            vars = (surfactantVar,)

        spMaxCoeff = SpMaxCoeff(distanceVar, vars)
        scMaxCoeff = ScMaxCoeff(distanceVar, vars)

        self.eq += ImplicitSourceTerm(spMaxCoeff) - scMaxCoeff - 1e-40

        if consumptionCoeff is not None:
            self.eq += ImplicitSourceTerm(consumptionCoeff)

    def solve(self, var, boundaryConditions = (), solver = LinearPCGSolver(), dt = 1.):
        for coeff in self.coeffs:
            coeff.updateDt(dt)
        SurfactantEquation.solve(self, var, boundaryConditions = boundaryConditions, solver = solver, dt = dt)

def _test(): 
    import doctest
    return doctest.testmod()
    
if __name__ == "__main__": 
    _test() 

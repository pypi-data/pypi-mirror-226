from typing import List

from numpy import ndarray, zeros, eye, matmul
from numpy import linalg

from .Variable import Variable, FLOAT_DATA_TYPE, Arra2dToDict
from .Discipline import Discipline


class DerivativeAssembler():
    """

    Assemble derivative matrices for a set of disciplines.

    """

    def __init__(self,
                 _disciplines: List[Discipline],
                 _diffInputs: List[Variable],
                 _diffOutputs: List[Variable]):

        self.disciplines = _disciplines
        """ List of disciplines for which the coupled derivatives are to compyted """

        self.Ny = sum([disc.sizeOutputs for disc in self.disciplines])
        """ Total size of all discipline outputs """

        self.diffInputs = _diffInputs
        """ Variables w.r.t differentiate """

        self.Nx = sum([xi.size for xi in self.diffInputs])
        """ Total size of differentiated inputs """

        self.diffOutputs = _diffOutputs
        """ Variables to be differentiated """

        self.Nf = sum([Fi.size for Fi in self.diffOutputs])
        """ Total size of differentiated outputs """

    def __dRidYj(self,
                 disc_i: Discipline,
                 disc_j: Discipline) -> ndarray:
        """ 

        dRi/dYj 

        """

        if disc_i == disc_j:
            return eye(disc_i.sizeOutputs,
                       dtype=FLOAT_DATA_TYPE)

        _dRidYj = zeros((disc_i.sizeOutputs,
                         disc_j.sizeOutputs),
                        dtype=FLOAT_DATA_TYPE)

        r = 0

        for yi in disc_i.outputVars:

            c = 0

            for yj in disc_j.outputVars:

                if yj in disc_i.inputVars:

                    _dRidYj[r: r + yi.size, c: c + yj.size] = \
                        -disc_i.jac[yi.name][yj.name]

                c += yj.size

            r += yi.size

        return _dRidYj

    def dRdY(self):
        """ 

        dR/dY

        """

        _dRdY = zeros((self.Ny, self.Ny), dtype=FLOAT_DATA_TYPE)

        r = 0

        for disc_i in self.disciplines:

            c = 0

            for disc_j in self.disciplines:

                _dRdY[r: r + disc_i.sizeOutputs, c: c +
                      disc_j.sizeOutputs] = self.__dRidYj(disc_i, disc_j)

                c += disc_j.sizeOutputs

            r += disc_i.sizeOutputs

        return _dRdY

    def __dRidXj(self,
                 disc_i: Discipline,
                 Xj: Variable):
        """ 

        dRi/dXj 

        """

        _dRidXj = zeros((disc_i.sizeOutputs,
                         Xj.size),
                        FLOAT_DATA_TYPE)

        if Xj in disc_i.inputVars:

            r = 0

            for yi in disc_i.outputVars:

                _dRidXj[r: r + yi.size, :] = \
                    disc_i.jac[yi.name][Xj.name]

                r += yi.size

        return _dRidXj

    def dRdX(self):
        """ 

        dR/dX 

        """

        _dRdX = zeros((self.Ny, self.Nx), FLOAT_DATA_TYPE)

        c = 0

        for Xj in self.diffInputs:

            r = 0

            for disc_i in self.disciplines:

                _dRdX[r: r + disc_i.sizeOutputs,
                      c: c + Xj.size] = \
                    self.__dRidXj(disc_i, Xj)

                r += disc_i.sizeOutputs

            c += Xj.size

        return _dRdX

    def __dFidYj(self,
                 disc_j: Discipline,
                 Fi: Variable):
        """ 

        dFi/dYj 

        """

        _dFidYj = zeros((Fi.size,
                         disc_j.sizeOutputs))

        r = 0

        if Fi in disc_j.outputVars:

            for yj in disc_j.outputVars:

                if Fi == yj:

                    _dFidYj[r: r + Fi.size, r: r +
                            Fi.size] = eye(Fi.size,
                                           dtype=FLOAT_DATA_TYPE)

                r += yj.size

        return _dFidYj

    def dFdY(self):
        """ 

        dF/dY

        """

        _dFdY = zeros((self.Nf,
                       self.Ny),
                      dtype=FLOAT_DATA_TYPE)

        r = 0

        for Fi in self.diffOutputs:

            c = 0

            for disc_j in self.disciplines:

                _dFdY[r: r + Fi.size, c: c +
                      disc_j.sizeOutputs] = self.__dFidYj(disc_j, Fi)

                c += disc_j.sizeOutputs

            r += Fi.size

        return _dFdY

    def dFdX(self):
        """ 

        dF/dX 

        """

        _dFdX = zeros((self.Nf,
                       self.Nx),
                      FLOAT_DATA_TYPE)

        _dRdY = self.dRdY()

        _dRdX = self.dRdX()

        _dFdY = self.dFdY()

        if self.Nx >= self.Nf:
            """ Adjoint approach """
            _dFdX = matmul(linalg.solve(_dRdY.T,
                                        _dFdY.T).T,
                           _dRdX)

        else:
            """ Direct approach"""
            _dFdX = matmul(_dFdY,
                           linalg.solve(_dRdY,
                                        _dRdX))

        dFdX_Dict = Arra2dToDict(self.diffInputs,
                                 self.diffOutputs,
                                 _dFdX)

        return dFdX_Dict

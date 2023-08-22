from typing import Dict, List
from dataclasses import dataclass, field

from numpy import float64, complex128, inf, zeros, ndarray

FLOAT_DATA_TYPE = float64
""" Datatype for floating point arithmetic """

COMPLEX_FLOAT_DATA_TYPE = complex128 
""" Datatype for complex floating point arithmetic. 
    Needs to be twice the size of FLOAT_DATA_TYPE 
"""

@dataclass(frozen=True)
class Variable:

    name: str = field(default = None, hash=True)

    size: int = field(default = 1, hash=False)

    lb: float = field(default = -inf, hash=False)

    ub: float = field(default = inf, hash=False)

    keepFeasible: bool = field(default=True, hash=False)
    
    def normValues(self, _val: ndarray) -> ndarray:
        return (_val - self.lb) / (self.ub - self.lb)

    def normGrad(self, _grad: ndarray) -> ndarray:
        return _grad * (self.ub - self.lb)
    
    def deNormValues(self, _val: ndarray) -> ndarray:
        return _val * (self.ub - self.lb) + self.lb

    def deNormGrad(self, _grad: ndarray) -> ndarray:
        return _grad / (self.ub - self.lb)

def DictToArray(_vars: List[Variable], _dict: Dict[str, ndarray]) -> ndarray:

    nVars = sum([var.size for var in _vars])

    varArray = zeros(nVars, FLOAT_DATA_TYPE)

    r = 0

    for var in _vars:

        varArray[r: r + var.size] = _dict[var.name]

        r += var.size

    return varArray

def ArrayToDict(_vars: List[Variable], _array: ndarray) -> Dict[str, ndarray]:
    

    varDict = {}

    r = 0

    for var in _vars:

        varDict[var.name] = _array[r: r + var.size]

        r += var.size
    
    return varDict

def DictToArray2d(_inputVars: List[Variable],
               _outputVars: List[Variable],
               _dict: Dict[str, Dict[str, ndarray]]) -> ndarray:

        nInVars = sum([var.size for var in _inputVars])

        nOutVars = sum([var.size for var in _outputVars])

        varArray = zeros((nOutVars, nInVars), 
                            FLOAT_DATA_TYPE)
        
        r = 0 

        for Fi in _outputVars:

            c = 0

            for xj in _inputVars:

                varArray[r: r + Fi.size, 
                         c: c + xj.size] = _dict[Fi.name][xj.name]
                
                c += xj.size

            r += Fi.size
        
        return varArray
        
def Arra2dToDict(_inputVars: List[Variable],
                 _outputVars: List[Variable],
                 _array2d: ndarray) -> Dict[str, Dict[str, ndarray]]:
    
    varDict: Dict[str, Dict[str, ndarray]] = {}

    r = 0
    
    for Fi in _outputVars:

        c = 0

        varDict[Fi.name]: Dict[str, ndarray] = {}

        for xj in _inputVars:

            varDict[Fi.name][xj.name] = _array2d[r: r +
                                                         Fi.size, c: c + xj.size]
                
            c += xj.size

        r += Fi.size
    
    return varDict

def NormalizeDesignVector( _variables: List[Variable], 
                          _designVector: Dict[str, ndarray]) -> Dict[str, ndarray]:

    for var in _variables:

        _designVector[var.name] = var.normValues(_designVector[var.name])

    return _designVector

def deNormalizeDesignVector( _variables: List[Variable], 
                          _designVector: Dict[str, ndarray]) -> Dict[str, ndarray]:

    for var in _variables:

        _designVector[var.name] = var.deNormValues(_designVector[var.name])

    return _designVector

def NormalizeGradient(_inputVars: List[Variable],
                      _outputVars: List[Variable],
                      _grad: Dict[str, Dict[str, ndarray]]):
    
    for outVar in _outputVars:

        for inVar in _inputVars:

            _grad[outVar.name][inVar.name] = inVar.normGrad(_grad[outVar.name][inVar.name])


    return _grad

def deNormalizeGradient(_inputVars: List[Variable],
                      _outputVars: List[Variable],
                      _grad: Dict[str, Dict[str, ndarray]]):
    
    for outVar in _outputVars:

        for inVar in _inputVars:

            _grad[outVar.name][inVar.name] = inVar.deNormGrad(_grad[outVar.name][inVar.name])


    return _grad
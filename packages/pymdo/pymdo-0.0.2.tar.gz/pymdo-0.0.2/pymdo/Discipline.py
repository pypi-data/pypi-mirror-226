from typing import Dict, List, Tuple

from numpy import ndarray, zeros, imag

from .Variable import Variable, FLOAT_DATA_TYPE, COMPLEX_FLOAT_DATA_TYPE

class VariableMissingError(Exception):
    def __init__(self,
                 _var: Variable,
                 _discName: str,
                 _isInput: int = 0
                 ) -> None:
        self.var: Variable = _var
        self.varType: str = "input" if _isInput == 0 else "output"
        self.message = f"In {_discName}, {self.varType} {self.var.name} is missing"
        super().__init__(self.message)


class VariableSizeMisMatchError(Exception):
    def __init__(self,
                 _var: Variable,
                 _discName: str,
                 _wrongSize: int,
                 _isInput: int = 0
                 ) -> None:
        self.var: Variable = _var
        self.varType: str = "input" if _isInput == 0 else "output"
        self.message = f"In {_discName}, {self.varType} {self.var.name} (size: {self.var.size}) is passed with wrong size {_wrongSize}"
        super().__init__(self.message)


class JacobianEntryError(Exception):
    def __init__(self,
                 _outVar: Variable,
                 _inVar: Variable,
                 _discName: str,
                 _wrongSize: Tuple[int, int] = None
                 ) -> None:
        if _wrongSize == None:
            self.message = f"In {_discName}, jacobian entry ({_outVar}, {_inVar}) is missing"
        else:
            self.message = f"In {_discName}, jacobian entry ({_outVar}, {_inVar}) (size: ({_outVar.size}, {_inVar.size})) has wrong size ({_wrongSize})"
        super().__init__(self.message)


class Discipline:
    """

    Base discipline class

    """

    ANALYTIC = "Analytic"

    FINITE_DIFFERENCE = "FiniteDifference"

    COMPLEX_STEP = "ComplexStep"

    DIFF_METHODS = [ANALYTIC,
                    FINITE_DIFFERENCE,
                    COMPLEX_STEP]

    def __init__(self,
                 _name: str,
                 _inputVars: List[Variable],
                 _outputVars: List[Variable]):

        self.name: str = _name
        """ Discipline name by which it is accessed """

        self.nInputs: int = len(_inputVars)
        """ Number of input variables """

        self.sizeInputs: int = sum([var.size for var in _inputVars])
        """ Total size of input variables """

        self.inputVars: List[Variable] = _inputVars
        """ List of input variables """

        self.nOutputs: int = len(_outputVars)
        """ Number of output variables """

        self.sizeOutputs: int = sum([var.size for var in _outputVars])
        """ Total size of input variables """

        self.outputVars: List[Variable] = _outputVars
        """ List of discipline output variables """

        self.diffInputs: List[Variable] = list()
        """ List of variables w.r.t differentiate """

        self.diffOutputs: List[Variable] = list()
        """ List of variables to be differentiated """

        self.diffMethod: str = self.ANALYTIC
        """ Jacobian computation method """

        self.eps: float = 1e-4
        """ Jacobian approximation step (if needed) """

        self._floatDataType = FLOAT_DATA_TYPE
        """ Data type for floating point operations """

        self.defaultInputs: Dict[str, ndarray] = {}
        """ Default input values for evaluation """

        self.values: Dict[str, ndarray] = {}
        """ Latest evaluation input and output values """

        self.jac: Dict[str, Dict[str, ndarray]] = {}
        """ Latest evaluation jacobian """

        self.valueCache: Dict[str, ndarray] = {}
        """ Latest successful evaluation input and output values 
            or the default inputs for evaluation
        """

    def __repr__(self) -> str:
        return self.name

    def VerifyValues(self,
                     _values: Dict[str, ndarray],
                     _mode: int = 0) -> None:

        varList: List[Variable]

        if (_mode == 0):
            varList = self.inputVars
        else:
            varList = self.outputVars

        for var in varList:
            if var.name not in _values:
                raise VariableMissingError(var,
                                           self.name,
                                           _mode)
            if var.size != _values[var.name].size:
                raise VariableSizeMisMatchError(var,
                                                self.name,
                                                _values[var.name].size,
                                                _mode)

    def GetInputValues(self) -> Dict[str, ndarray]:
        return {var.name : self.values[var.name] for var in self.inputVars}

    def GetOutputValues(self) -> Dict[str, ndarray]:
        return {var.name : self.values[var.name] for var in self.outputVars}

    def SetDefaultInputValue(self, _values: Dict[str, ndarray]) -> None:
        self.defaultInputs.update(_values)

    def _UpdateCache(self, _values: Dict[str, ndarray] = None) -> None:

        if _values is None:
            self.valueCache.update(self.values)
        else:
            self.valueCache.update(_values)

    def _Eval(self) -> None:
        raise NotImplementedError

    def Eval(self,
             _inputValues: Dict[str, ndarray] = None,
             _checkValues: bool = True,
             _cacheValues: bool = False) -> Dict[str, ndarray]:
        """

        Execute discipline with the given _inputValues.

        If some input values are not passed in _inputValues,
        the default values will be used.

        If _checkValues is True, the input values provided, 
        and the output values computed will be checked to make sure
        no variable is missing or has a mismatched size.

        If _cacheValues is True, the the input values provided, 
        and the output values computed will be saved in the cache.

        """

        self.values = {}

        self.values.update(self.defaultInputs)
        """ Load the default inputs """

        if _inputValues is not None:
            self.values.update(_inputValues)
        """ Load the input values provided, overriding the default inputs """

        if _checkValues:
            self.VerifyValues(self.values, 0)

        self._Eval()

        if _checkValues:
            self.VerifyValues(self.values, 1)

        if _cacheValues:
            self._UpdateCache()

        return self.values

    def AddDiffInput(self, _diffInputs: List[Variable]) -> None:
        """

        Add variable(s) w.r.t to differentiate

        """

        for var in _diffInputs:

            if var not in self.inputVars:

                raise VariableMissingError(var,
                                           self.name,
                                           0)
            if var not in self.diffInputs:

                self.diffInputs.append(var)

    def AddDiffOutput(self, _diffOutputs: List[Variable]) -> None:
        """

        Add variable(s) to be differentiated

        """

        for var in _diffOutputs:

            if var not in self.outputVars:

                raise VariableMissingError(var,
                                           self.name,
                                           1)
            if var not in self.diffOutputs:

                self.diffOutputs.append(var)

    def SetJacApproximationMethod(self,
                                  _method: str = FINITE_DIFFERENCE,
                                  _eps: float = 1e-4) -> None:
        self.diffMethod = _method
        self.eps = _eps

    def _ApproximateJacobian(self) -> None:

        F = {outVar.name: self.values[outVar.name] for outVar in self.diffOutputs}

        X = {inVar.name: self.values[inVar.name] for inVar in self.diffInputs}

        self.jac = {outVar.name:
                    {inVar.name:
                     zeros(
                         (outVar.size, inVar.size), self._floatDataType)
                     for inVar in self.diffInputs}
                    for outVar in self.diffOutputs}

        if self.diffMethod == self.COMPLEX_STEP:                    
        
            self._floatDataType = COMPLEX_FLOAT_DATA_TYPE
            
            X = {name: values.astype(self._floatDataType)
                for name, values in X.items()}

            Eps = self.eps * 1j
        
        else:

            Eps = self.eps

        for inVar in self.diffInputs:

            for i in range(0, inVar.size):
          
                temp = X[inVar.name][i]

                X[inVar.name][i] += Eps

                Fp = self.Eval(X,
                               False,
                               False)

                for outVar in self.diffOutputs:
                    
                    if self.diffMethod == self.COMPLEX_STEP:

                        dF = imag(Fp[outVar.name])

                    else:

                        dF = Fp[outVar.name] - F[outVar.name] 

                    self.jac[outVar.name][inVar.name][:, i] = dF / self.eps

                X[inVar.name][i] = temp

        if self.diffMethod == self.COMPLEX_STEP:

            self._floatDataType = FLOAT_DATA_TYPE

            X = {name: values.real
                    for name, values in X.items()}

    def _Differentiate(self) -> None:
        raise NotImplementedError

    def Differentiate(self, _values: Dict[str, ndarray] = None) -> Dict[str, Dict[str, ndarray]]:
        """

        Differentiate the discipline for a given set of input values.

        If no values are provided, try to use the current values. 

        If differentiated inputs/outputs are not defined,
        all input/output variables are set as such.

        """

        if _values is not None:
            self.values.update(_values)

        self.jac = {}

        # TODO:
        # CHECK IF JAC FOR CURRENT VALUES IS CACHED
        # OR IF INPUTS ARE CURRENT VALUES
        # AND EXIT EARLY

        if not self.diffInputs:
            self.diffInputs = [var for var in self.inputVars]

        if not self.diffOutputs:
            self.diffOutputs = [var for var in self.outputVars]

        if (self.diffMethod == self.ANALYTIC):
            self._Differentiate()

        else:
            self._ApproximateJacobian()
        
        #self.VerifyJac()

        return self.jac

from typing import Dict, List, Tuple

from numpy import ndarray, zeros, ones, bool8
from scipy.optimize import minimize, Bounds
import matplotlib.pyplot as plt

from .Variable import Variable, FLOAT_DATA_TYPE
from .Variable import ArrayToDict, DictToArray, DictToArray2d
from .Variable import NormalizeDesignVector, deNormalizeDesignVector
from .Variable import NormalizeGradient
from .Discipline import Discipline
from .MDA import MDA, SmartMDA


class MDOptProblem:

    def __init__(self,
                 _disciplines: List[Discipline],
                 _designVariables: List[Variable],
                 _objective: Variable,
                 _maximizeObjective: bool = False,
                 _saveDesignVector: bool = False) -> None:

        self.disciplines: List[Discipline] = _disciplines
        """ List of disciplines modelling the problem """

        self.designVariables: List(Variable) = _designVariables
        """ List of design variables """

        self.nDesignVars: int = sum([var.size for var in self.designVariables])
        """ Number of design variables """

        self.sizeDesignVars: int = sum([var.size for var in self.designVariables])
        """ Total size of design variables """

        self.objective: Variable = _objective
        """ Optimization objective """

        self.maximizeObjective: bool = _maximizeObjective
        """ Whether to maximize the objective """

        self.constraints: List[Variable] = []
        """ List of constraints """

        self.designVector: Dict[str, ndarray] = {}
        """ Current design variables values """

        self.optLog: List[Dict[str, ndarray]] = []
        """ Optimization Log.
            By default saves the objective and constraint values
            for each optimization cycle.

            Set saveDesignVector to True to also save the design vector.
        """

        self.saveDesignVector: bool = _saveDesignVector
        """ Whether to save the design vector for each optimization cycle """

    def _GetDesignVariableBounds(self) -> Bounds:

        lb = zeros(self.sizeDesignVars, FLOAT_DATA_TYPE)

        ub = zeros(self.sizeDesignVars, FLOAT_DATA_TYPE)

        keepFeasible = zeros(self.sizeDesignVars, bool8)

        r = 0

        for var in self.designVariables: 

            lb[r : r + var.size] = 0.0 * ones(var.size, FLOAT_DATA_TYPE)

            ub[r : r + var.size] = 1.0 * ones(var.size, FLOAT_DATA_TYPE)

            keepFeasible[r : r + var.size] = var.keepFeasible * ones(var.size, bool8)

            r += var.size

        return Bounds(lb, 
                      ub, 
                      keepFeasible) 

    def Execute(self, _initialDesignVector: Dict[str, ndarray], 
                _algoName: str = "SLSQP", 
                **_options) -> Tuple[Dict[str, ndarray], float]:
        raise NotImplementedError
    
    def PlotOptimizationHistory(self):

        cycles = [i for i in range(len(self.optLog))]

        # Plot objective value history
        objLog = [self.optLog[i][self.objective.name] for i in cycles]

        plt.plot(cycles,
                 objLog)
        
        plt.xlabel(" Cycles ")
        plt.ylabel(f"{self.objective.name}")
        plt.grid()

        plt.show()
    
    def SaveOptHistory(self, 
                       _directory: str, 
                       _fullHistory: bool = False):
        pass
        




class MDF(MDOptProblem):

    def __init__(self, 
                 _disciplines: List[Discipline],
                 _designVariables: List[Variable],
                 _objective: Variable,
                 _maximizeObjective: bool = False) -> None:
        
        super().__init__(_disciplines,
                         _designVariables,
                         _objective,
                         _maximizeObjective)

        self.mda: SmartMDA = SmartMDA(self.disciplines)
        """ MDA used for converging the system to feasibility """
        
        self.mda.AddDiffInput(self.designVariables)

        self.mda.AddDiffOutput([self.objective])


    def Execute(self, _initialDesignVector: Dict[str, ndarray], 
                _algoName: str = "SLSQP", 
                _options = None) -> Tuple[Dict[str, ndarray], float]:

        def F(_designPointArray: ndarray) -> float:
            
            self.designVector = ArrayToDict(self.designVariables,
                                           _designPointArray)
            
            self.designVector = deNormalizeDesignVector(self.designVariables,
                                                       self.designVector)
                                    
            self.mda.Eval(self.designVector)

            obj = self.mda.values[self.objective.name]

            self.optLog.append({self.objective.name: obj})

            if self.saveDesignVector:
                self.optLog[-1].update(self.designVector)
            
            if self.maximizeObjective:

                return -obj

            else:

                return obj

        def dF(_designPointArray: ndarray) -> ndarray:
            
            self.mda.Differentiate()

            grad = NormalizeGradient(self.designVariables,
                              [self.objective],
                              self.mda.jac)

            grad = DictToArray2d(self.designVariables,
                                 [self.objective],
                                 grad)
            
            if self.maximizeObjective:

                return  -grad 
            
            else:

                return  grad
        
        x0 = NormalizeDesignVector(self.designVariables, 
                                   _initialDesignVector)
        
        x0 = DictToArray(self.designVariables,
                         x0)
        
        bnds = self._GetDesignVariableBounds()

        result = minimize(fun = F, 
                        x0 = x0,
                        method = _algoName, 
                        jac = dF, 
                        bounds = bnds,
                        options = _options)
        
        return (self.designVector, result.fun)


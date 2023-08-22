from typing import Dict, List, Tuple
from warnings import warn

from numpy import ndarray, zeros, abs, mean
from numpy import linalg 
import matplotlib.pyplot as plt
import networkx as nx

from .Variable import Variable
from .Discipline import Discipline
from .DerivativeAssembler import DerivativeAssembler

class MDANotEvaluatedError(Exception):
    def __init__(self, _mdaName: str) -> None:
        self.message = f"{_mdaName} is not yet evaluated"
        super().__init__(self.message)


class MDANotConverged(Warning):
    def __init__(self, _mdaName: str, _nMaxIter: int, _res: float, _relTol: float) -> None:
        self.message = f"{_mdaName} has not converged in {_nMaxIter} iterations, (residual) {_res} > (tolerance) {_relTol}"
        super().__init__(self.message)


def SeperateInputsAndOutputs(_disciplines: List[Discipline]) -> Tuple[List[Variable], List[Variable]]:
    """ 

    Find input and output variables from list of disciplines

    """
    outputVarDict: Dict[str, Variable] = {}
    for disc in _disciplines:
        for var in disc.outputVars:
            outputVarDict[var.name] = var

    inputVarDict: Dict[str, Variable] = {}
    for disc in _disciplines:
        for var in disc.inputVars:
            if var.name not in outputVarDict:
                inputVarDict[var.name] = var

    return (inputVarDict.values(), outputVarDict.values())


class MDA(Discipline):
    """

    Base MDA class 

    """

    MDA_SUCCESS = True

    MDA_FAIL = False

    MDA_STATUS = [MDA_SUCCESS,
                  MDA_FAIL]

    def __init__(self,
                 _disciplines: List[Discipline],
                 _name: str,
                 _nIterMax: int = 15,
                 _relaxFact: float = 0.9,
                 _relTol: float = 0.0001
                 ) -> None:

        self.disciplines: List[Discipline] = _disciplines
        """ Disciplines to be included in the analysis """

        self.nIterMax = _nIterMax
        """ Maximum number of iterations """

        self.relaxFact = _relaxFact
        """ Relaxation factor """

        self.relTol = _relTol
        """ Relative tolerance """

        self.residualLog: List[Dict[str, float]] = []
        """ Residual log from last evaluation """

        self.status: bool = self.MDA_FAIL
        """ Whether the last execution converged """

        inputVars, outputVars = SeperateInputsAndOutputs(self.disciplines)

        super().__init__(_name,
                         inputVars,
                         outputVars)

    def SetOptions(self,
                   _nIterMax: int = 15,
                   _relaxFact: float = 0.9,
                   _relTol: float = 0.0001) -> None:
        self.nIterMax = _nIterMax
        self.relaxFact = _relaxFact
        self.relTol = _relTol

    def _Eval(self) -> None:
        raise NotImplementedError

    def Eval(self,
             _inputValues: Dict[str, ndarray] = None,
             _checkValues: bool = True,
             _cacheValues: bool = True) -> Dict[str, ndarray]:
        """ 

        Evaluate the MDA with the given inputs.

        All inputs (and outputs) not provided are set to zero.
        If they are not provided directly, but set in default values,
        those values are used. Finally, the default MDA values are overriden
        by default discipline values, if they are set.

        """

        for varList in [self.inputVars, self.outputVars]:
            for var in varList:
                if var.name not in self.defaultInputs:
                    self.defaultInputs[var.name] = zeros(var.size,
                                                            self._floatDataType)

        for disc in self.disciplines:
            self.defaultInputs.update(disc.defaultInputs)

        return super().Eval(_inputValues,
                            _checkValues,
                            _cacheValues)

    def _Differentiate(self) -> None:

        for disc in self.disciplines:

            disc.Differentiate(self.values)

        assembler = DerivativeAssembler(self.disciplines,
                                        self.diffInputs,
                                        self.diffOutputs)

        self.jac = assembler.dFdX()

    def _ComputeResidual(self,
                         _curOutputValues: Dict[str, ndarray],
                         _prevOutputValues: Dict[str, ndarray]) -> ndarray:
        """
        
        Compute the residual namely the difference:
        
        _curOutputValues - _prevOutputValues

        for all coupling/output variables, and return it.

        The residual log is also updated, 
        but only a residual metric for each variable (and a total) is stored.

        The status is set to MDA_SUCCESS,
        if the total residual metric is below the specified tolerance.
        
        """

        residual: ndarray = zeros(self.sizeOutputs,
                                     self._floatDataType)
        
        residualMetric: Dict[str, float] = {}

        totalRes: float = 0.0

        r = 0

        for outVar in self.outputVars:

            residual[r: r + outVar.size] = _curOutputValues[outVar.name] - _prevOutputValues[outVar.name]

            residualMetric[outVar.name] = abs(mean(residual[r: r + outVar.size]) 
                                                 / mean(_curOutputValues[outVar.name]))

            totalRes += residualMetric[outVar.name]

            r += outVar.size

        residualMetric["total"] = totalRes

        self.residualLog.append(residualMetric)

        if totalRes <= self.relTol:
            self.status = self.MDA_SUCCESS

        return residual

    def PlotResidual(self,
                     _varNames: List[str]) -> None:
        """
        
        Plot the residual metric log for all provided variable names.

        Use the name "total", to plot the total MDA residual metric 

        """

        if not self.residualLog:
            raise MDANotEvaluatedError(self.name)

        for varName in _varNames:
            plt.plot([i for i in range(len(self.residualLog))],
                     [self.residualLog[i][varName]
                         for i in range(len(self.residualLog))],
                     label=varName)
            
        plt.title(f"{self.name} residual metric")
        plt.ylabel("Residual metric")
        plt.xlabel("Iterations")
        plt.legend()
        plt.show()

    def _TerminateCondition(self) -> bool:

        if self.status == self.MDA_SUCCESS:
            """ If converged, exit early """
            return True

        curIter: int = len(self.residualLog)
        """ Current iteration """

        curRes: float = 0.0 if not self.residualLog else self.residualLog[-1]["total"]
        """ Current (total) residual metric """


        if curIter == self.nIterMax:

            if self.status == self.MDA_FAIL:
                """ Iteration limit reached, and MDA has not converged """

                message = f"{self.name} has not converged in {self.nIterMax} iterations, (residual) {curRes} > (tolerance) {self.relTol}"
            
                warn(message)

            return True

        return False

class MDAJacobi(MDA):
    """
    
    This MDA sub-class implements the generalized 
    or non-linear Jacobi iteration:

    Yi^(k+1) = Yi(Xi^k),

    where Xi^k = [xi^k z^k y1i^k ... yni^k], j =/= i

    """

    def __init__(self,
                 _disciplines: List[Discipline],
                 _name: str = "MDAJacobi",
                 _nIterMax: int = 15,
                 _relaxFact: float = 0.9,
                 _relTol=0.0001) -> None:

        super().__init__(_disciplines,
                         _name,
                         _nIterMax,
                         _relaxFact,
                         _relTol)

    def _Eval(self) -> None:

        self.status = self.MDA_FAIL

        self.residualLog = []

        while self._TerminateCondition() == False:

            currentOutputs: Dict[str, ndarray] = {}

            for disc in self.disciplines:

                discInputs = {
                    var.name: self.values[var.name] for var in disc.inputVars}

                disc.Eval(discInputs,
                            _checkValues=True,
                            _cacheValues=False)
                
                currentOutputs.update({var.name: disc.values[var.name] for var in disc.outputVars})
                
            for var in self.outputVars:
                currentOutputs[var.name] = self.relaxFact * currentOutputs[var.name] + \
                    (1 - self.relaxFact) * self.values[var.name]
            
            self._ComputeResidual(currentOutputs,
                                  self.values)

            self.values.update(currentOutputs)

class MDAGaussSeidel(MDA):
    """
    
    This MDA sub-class implements the generalized 
    or non-linear Gauss-Seidel iteration:

    Yi^(k+1) = Yi(Xi^k),

    where Xi^k = [xi^(k+1) z^(k+1) y1i^(k+1) ... y(i-1)i^(k+1)  y(i+1)i^k yni^k]

    """

    def __init__(self,
                 _disciplines: List[Discipline],
                 _name: str = "MDAGaussSeidel",
                 _nIterMax: int = 15,
                 _relaxFact: float = 0.9,
                 _relTol=0.0001) -> None:

        super().__init__(_disciplines,
                         _name,
                         _nIterMax,
                         _relaxFact,
                         _relTol)

    def _Eval(self) -> None:

        self.status = self.MDA_FAIL

        self.residualLog = []

        while self._TerminateCondition() == False:

            currentOutputs: Dict[str, ndarray] = {}

            for disc in self.disciplines:

                discInputs = {var.name: self.values[var.name] if var.name not in currentOutputs
                              else currentOutputs[var.name] for var in disc.inputVars}

                discOutputs = disc.Eval(discInputs,
                                        _checkValues=True,
                                        _cacheValues=False)

                for var in disc.outputVars:

                    currentOutputs[var.name] = self.relaxFact * discOutputs[var.name] + \
                        (1 - self.relaxFact) * self.values[var.name]

            self._ComputeResidual(currentOutputs,
                                  self.values)

            self.values.update(currentOutputs)

class MDANewton(MDA):
    """

    This MDA sub-class uses the Newton iteration 
    for a system of non-linear equations:
    
    dR^k/dY * Ycorr^(k) = R^k

    Y^(k+1) = Y^k + Ycorr^k

    """

    def __init__(self,
                 _disciplines: List[Discipline],
                 _name: str = "MDANewton",
                 _nIterMax: int = 15,
                 _relTol=0.0001) -> None:

        super().__init__(_disciplines, 
                         _name, 
                         _nIterMax, 
                         _relTol = _relTol)

    def _Eval(self) -> None:

        self.status = self.MDA_FAIL

        self.residualLog = []

        while self._TerminateCondition() == False:

            currentOutputs: Dict[str, ndarray] = {}

            for disc in self.disciplines:

                disc.Eval(self.values,
                          _checkValues=True,
                          _cacheValues=False)
                
                disc.Differentiate()

                currentOutputs.update(disc.GetOutputValues())

            R = self._ComputeResidual(currentOutputs,
                                  self.values)

            assembler = DerivativeAssembler(self.disciplines,
                                            self.inputVars,
                                            self.outputVars)
            
            dRdY = assembler.dRdY()

            Ycorr = linalg.solve(dRdY, R)

            r = 0 

            for var in self.outputVars:

                self.values[var.name] = self.values[var.name] + Ycorr[r: r + var.size]

                r += var.size
            
       
class MDAHybrid(MDA):
    """
    
    A hybrid MDA consisting of a sequence of MDAs.

    By default a GaussSeidel MDA is followed by a
    Newton MDA. This combination uses the robust nature 
    of the former, with the fast convergence of the latter.

    Any user-defined sequence of MDAs can be used.

    """

    def __init__(self, 
                 _disciplines: List[Discipline],
                 _mdaSequence: List[MDA] = None, 
                 _name: str = "MDAHybrid") -> None:
        
        super().__init__(_disciplines,
                          _name)

        self.mdaSequence: List[MDA] 

        if _mdaSequence is None:

            self.mdaSequence = [MDAGaussSeidel(self.disciplines,
                                               _nIterMax = 2,
                                               _relaxFact = 0.8,
                                               _relTol = 10),
                                MDANewton(self.disciplines,)]
        else:
            self.mdaSequence = _mdaSequence
    
    def _Eval(self) -> None:
        
        self.residualLog = []

        for mda in self.mdaSequence:

            self.values.update(mda.Eval(self.values))

            self.residualLog.extend(mda.residualLog)

class SmartMDA(MDA):
    """
    
    This MDA sub-class creates an execution sequence for the disciplines,
    according to their inter-depedencies.

    This can reduce the execution time, by excluding weakly-coupled disciplines from
    MDA loops.

    By default, Gauss-Seidel MDAs are created to resolve couplings that might emerge. 
    The user can also specify which MDA algorithm to use.
    
    """

    def __init__(self,
                 _disciplines: List[Discipline],
                 _name: str = "SmartMDA"):

        super().__init__(_disciplines,
                         _name)

        self.groups: List[Dict[str, MDA]] = self._CreateGroups()

    def _CreateGroups(self) -> List[Dict[str, MDA]]:
        """

        Create discipline groups.

        Groups are split into levels. The groups in each level can execute in parallel.

        Each group is either a single discipline, or an MDA of coupled disciplines.

        """

        self.groups = []

        graph = nx.DiGraph()

        for disc_i in self.disciplines:

            for var_i in disc_i.outputVars:

                for disc_j in self.disciplines:

                    if var_i in disc_j.inputVars:

                        graph.add_edge(disc_i,
                                       disc_j)

        groupList: List[List[Discipline]] = []

        for group in sorted(nx.strongly_connected_components(graph)):

            groupList.append(list(group))

        graphCondensed = nx.condensation(
            graph, nx.strongly_connected_components(graph))

        execSeq = []

        while True:

            if len(graphCondensed.nodes) == 0:

                break

            currentLevel = []

            for groupIdx in graphCondensed:

                if graphCondensed.out_degree[groupIdx] == 0:

                    currentLevel.append(groupIdx)

            execSeq.append(currentLevel)

            for groupIdx in currentLevel:

                graphCondensed.remove_node(groupIdx)

        for level in execSeq[::-1]:

            curLevelGroups = {}

            for groupIdx in level:

                groupDisciplines = groupList[groupIdx]

                groupName = f"Group_{groupIdx}"

                if len(groupDisciplines) > 1:
                    curLevelGroups[groupName] = MDAGaussSeidel(
                        groupDisciplines, groupName)
                else:
                    curLevelGroups[groupName] = groupDisciplines[0]

            self.groups.append(curLevelGroups)

        return self.groups

    def _Eval(self) -> None:

        for lvl in self.groups:

            for group in lvl.values():

                self.values.update(group.Eval(self.values))

class InvalidMDAName(Exception):

    def __init__(self, _invalidMDAType: str) -> None:

        self.message = f"Invalid MDA type: {_invalidMDAType}. Available types are: MDAGaussSeidel, MDAJacobi, MDANewton, MDAHybrid"

        super().__init__(self.message)
        
def MDAFactory(_disciplines: List[Discipline],
                _mdaType: str = "MDAGaussSeidel",
                **kwargs) -> MDA:
    
    if _mdaType == "MDAGaussSeidel":

        return MDAGaussSeidel(_disciplines, **kwargs)
    
    if _mdaType == "MDAJacobi":

        return MDAJacobi(_disciplines, **kwargs)
    
    if _mdaType == "MDANewton":

        return MDANewton(_disciplines, **kwargs)
    
    if _mdaType == "MDAHybrid":

        name = "MDAHybrid" if "_name" not in kwargs else kwargs["_name"]

        mdaSequence: List[MDA] = None if "_mdaSequence" not in kwargs else kwargs["_mdaSequence"]

        return MDAHybrid(_disciplines, mdaSequence, name)

    else:
        raise InvalidMDAName(_mdaType)


    



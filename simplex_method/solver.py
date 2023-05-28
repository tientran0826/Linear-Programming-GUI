import sys
from typing import List

import numpy as np

from .exceptions import LinearlyDependentError
from .exceptions import SizeMismatchError
from .exceptions import UnsolvableError
from .tableau import Tableau


class SimplexSolver:
    """
    Solves a Linear Programming problem using Dantzig's Simplex Method
    by manipulating the `Tableau` class.

    Methods
    -------
    solve(max_iterations=100, use_blands_rule=False) : solves problem, yielding
    a`Solution` object

    """

    def __init__(self, obj_func: List[float], coeffs: List[List[float]], constraints: List[float]):
        """
        Assigns internal variables after performing basic checks.

        Parameters
        ----------
        obj_func: values af the objective function, in order. Must be of
           size *n* (n = number of variables).
        coeffs: values of technological coefficients (params), row-major.
          Must be size *m x n* (m = number of constraints)
        constraints: values of the constraint column-vector (right-hand
        side). Must be size *m*.
        """

        # validate dimensions
        m = len(constraints)  # rows
        n = len(obj_func)  # columns

        if len(coeffs) != m:
            raise SizeMismatchError
        for coeff in coeffs:
            if len(coeff) != n:
                raise SizeMismatchError

        # full rank assumption
        if m > n:
            raise LinearlyDependentError

        # create corresponding tableau
        self.tableau = Tableau(
            obj_func=obj_func,
            coeffs=coeffs,
            constraints=constraints
        )

    def solve(self, max_iterations=100, use_blands_rule=False, print_tableau=True, No_var=0, 
              check_min = 1, var_none =[], list_Var_positive = []):
        """
        Solves Linear Programming Problem. Returns `Solution` instance`.

        Parameters
        ----------
        max_iterations : int
           number of times to pivot before resorting to Bland's rule
        use_blands_rule : bool
           whether to use Bland's Rule for anti-cycling
        print_tableau : bool
           whether to print the tableau at every iteration
        """

        with self.tableau as t:
            iterations = 0
            steps = []
            steps.append(t.tab.copy())
            pivot_arounds = []
            # keep pivoting until exception is raised or max iterations
            while iterations < max_iterations:
                t.pivot(use_blands_rule=use_blands_rule)
                #print(f"[{iterations + 1}] Pivoted around "
                #            f"{t.pivot_idx[0] - 1, t.pivot_idx[1]}")  # log pivots
                #print("================")
                #print(f'{t}\n')  # log tableau
                steps.append(t.tab.copy())
                pivot_arounds.append((t.pivot_idx[0] - 1, t.pivot_idx[1]))
                iterations += 1
            steps.append(t.tab.copy())
            
            # use Bland's rule 
            if not use_blands_rule:
                return self.solve(use_blands_rule=True)

            # if no solution if found
            raise UnsolvableError(max_iterations)

        return pivot_arounds,steps,Solution(state=t.state, basis=t.basis, No_var = No_var, check_min = check_min, 
                        var_none = var_none,list_Var_positive = list_Var_positive,
                        solution=t.solution, obj_value=t.obj_value)


class Solution:
    """
    Converts Tableau parameters into a human-readable solution.
    """

    def __init__(self, state: str, obj_value: float,No_var : int, check_min: int, 
                 list_Var_positive: List[int],
                 var_none: List[int] ,basis: List[int], solution: List[float]):
        """
        Calculates objective value and basic solution.

        Parameters
        ----------
        state : final state of the tableau
        obj_value : final objective value of tableau
        basis : indices of the basis variables
        solution : raw solution from tableau
        """
        
        self.state = state
        self.check_min = check_min
        
        # objective value
        self.obj_value = {
            "Optimal": obj_value * check_min,
            "Unbounded": np.inf,
            "Infeasible": np.NaN
        }[self.state]

        # calculate solution if optimal
        if self.state == "Optimal":
            self.solution = [0.0] * (len(var_none) + No_var)  # start from zero vector
            for i, j in zip(basis, solution):
                if i < (len(var_none) + No_var):
                    self.solution[i] = j
                
            if len(var_none) != 0:
                for i in var_none:
                    self.solution[i] = self.solution[i] - self.solution[i + 1] 
                for i in var_none:
                    del self.solution[i+1] 
                    
            if (len(self.solution) >= No_var):
                self.solution = self.solution[:No_var]
                self.solution*=(list_Var_positive) 
        
        else:
            self.solution = None
       
    def __repr__(self):
        """
        Returns string representation of solution.
        """
        if self.check_min == -1:
            unbounded = "Bài toán không giới nội, Z = -Inf"
        else:
            unbounded  = "Bài toán không giới nội, Z = Inf"

        return {
            "Optimal": f"Giá trị tối ưu Z ={self.obj_value}, X = {self.solution}",
            "Unbounded": unbounded,
            "Infeasible": "Bài toán vô nghiệm."
        }[self.state]
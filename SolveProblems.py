from simplex_method.solver import SimplexSolver
from simplex_method.two_phase_simplex import two_phase_simplex
from Normalization import make_standard_form

def solve_problem(user_inputs):
    problem = make_standard_form(user_inputs)
    
    if (any(x < 0 for x in problem['constraints'])):
        check_min = 1
        if user_inputs['objective'] == 'maximize':
            check_min = -1
        # initialize object
        simx = two_phase_simplex()
        # get equations and standarize them
        simx.get_equations(problem)
        simx.standard_form()

        # call two-phase simplex method
        opt_point, opt_value = simx.two_phase()
        print(opt_value)
        if not opt_value:
            sol = f"{opt_point}"
        elif opt_value in ["Inf","-Inf"]:
            sol = f"{opt_point}, Gia tri Z = {opt_value}"
        else:
            sol = f"{opt_point}, Gia tri Z = {opt_value*check_min}"
        
        return problem,sol,None,None
    else:
        problem['obj_func']*= -1
        
        check_min = 1
        if user_inputs['objective'] == 'minimize':
            check_min = -1

        use_blands_rule = False

        if (any(x == 0 for x in problem['constraints'])):
            use_blands_rule = True
        # initialize solver
        solver = SimplexSolver(obj_func=problem['obj_func'],
                        coeffs=problem['coeffs'],
                        constraints=problem['constraints'])

        pivot_arounds,steps,sol = solver.solve(use_blands_rule=use_blands_rule,
                        print_tableau=True, 
                        No_var = problem['No_var'],
                        check_min = check_min, 
                        var_none = problem['var_none'],
                        list_Var_positive = problem['list_Var_positive'],)

        return problem,sol,steps,pivot_arounds
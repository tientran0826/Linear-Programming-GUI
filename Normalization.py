import numpy as np

def make_standard_form(user_inputs):
    objective = user_inputs['objective']
    c_coeff = np.array(user_inputs['c_coeff'])
    coeffs = user_inputs['coef_constraints']
    inequality = user_inputs['inequality_constraints']
    constraint = user_inputs['b_value']

    coef_inequality_constraints = user_inputs['coef_inequality_constraints']
    inequality_inequality_constraints = user_inputs['inequality_inequality_constraints']
    
    n = len(c_coeff)        # number of variables (excluding slack/excess)
    m = len(constraint)     # number of constraints (excluding non-negativity)
    X = ['X'+str(i+1) for i in range(len(c_coeff))]
    print(X)
    n_slack = 0             # number of slack/excess variables
    equality = 0
    for i in range(m):
            if inequality[i] == '<=':
                n_slack += 1
            elif inequality[i] == '>=':
                n_slack += 1
            elif  inequality[i] == '=':
                n_slack += 2
                equality+= 1
    # Convert to 'minimize' for standard form:            
    if objective == 'maximize':
        c_coeff = -1*c_coeff

    A = np.zeros([m+equality, n+m + equality])
    b = np.zeros([m + equality,1])
    c_coeff = np.hstack([c_coeff, np.zeros(m + equality)])
    i = 0
    j = 0
    var_none = []
    
    while i < (m + equality):
        if inequality[j] == '<=':
            A[i,n+i] = 1
            A[i,0:n] = np.array(coeffs[j])
            b[i,0] = constraint[j]

        # Ensure all inequalities are '<=':
        elif inequality[j] == '=':
            A[i,n+i] = 1
            A[i,0:n] = np.array(coeffs[j])
            b[i,0] = constraint[j]

            A[i+1,n+i + 1] = 1
            A[i + 1,0:n] = -1*np.array(coeffs[j])
            b[i + 1,0] = -1*constraint[j]
            
            i += 1
        # Ensure all inequalities are '<=':   
        elif inequality[j] == '>=':
            A[i,n+i] = 1
            A[i,0:n] = -1*np.array(coeffs[j])
            b[i,:] = -1*constraint[j]
        i+= 1 
        j+= 1
    k = 0
    list_var_positive = np.ones(n)
    for j in range(n):
        #tranfer <= to =>
        if inequality_inequality_constraints[j] == '<=':
            A[:,k] = A[:,k]*-1
            c_coeff[k] *= -1
            list_var_positive[j] = -1
        #tranfer x = u - v if x don't have constraint
        elif inequality_inequality_constraints[j] == 'None':
            A = np.insert(A, k +1, A[:,k]*-1, axis=1)
            X.insert(k+1, f"{X[k]}-")
            X[k] = f"{X[k]}+"
            c_coeff = np.insert(c_coeff, k+1, c_coeff[k] * -1)
            var_none.append(k)
            k+=1
        k+=1
            
    conversion = {}
    conversion['objective'] = objective
    conversion['X'] = X
    conversion['coeffs'] = A
    conversion['constraints'] = b
    conversion['obj_func'] = c_coeff
    conversion['No_var'] = n
    conversion['No_con'] = m
    conversion['n_slack'] = n_slack
    conversion['var_none'] = var_none
    conversion['list_Var_positive'] = list_var_positive
    return conversion


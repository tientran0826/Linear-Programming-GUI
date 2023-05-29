import numpy as np

class two_phase_simplex():
    '''Two Phase Simplex method operates on linear programs in standard form'''

    def __init__(self):
        self.table = None
        self.RHS = None
        self.var = None
        self.min_max = None
        self.constraint_count = None
        self.list_var = None  
        self.user_input = None
    def get_equations(self,user_input):
        self.user_input = user_input
        self.min_max = 'minimize'
        self.constraint_count = user_input['No_con']
        
        equations = list()
        RHS = list()

        # Get objective function
        self.var = len(user_input['obj_func']) - self.constraint_count

        
        equations = np.append(user_input['coeffs'][:,:self.var], [user_input['obj_func'][:self.var]], axis=0)
        RHS = np.append(user_input['constraints'], 0)

        self.table = equations
        self.RHS = RHS
        self.list_var = [(x+self.var) for x in range(self.constraint_count)]
        
    def pprint(self, table,list_var,pivot_col,pivot_row):
        '''Pretty print a table to check intermediate results'''
        pivot_around = None
        if(pivot_col != -1):
            print(f"[] Pivoted around "
                                f"{pivot_col, pivot_row}")
            pivot_around = (pivot_col, pivot_row)
        for i in range(len(table[-1]) - 1):
            print ('{:>4}x'.format(i+1),end ='')
        print ('{:>5}'.format('RHS'))        
        print('z  [',end='')
        tab_array = []
        temp = []
        for j in table[-1]:
            temp.append(round(j, 2))
            print(str(round(j, 2)) + ' ', end='')
        tab_array.append(temp)
        print(']')
        for i in range(len(table) - 1):
            print('{0}x ['.format(list_var[i] + 1),end='')
            temp = []
            for j in table[i]:
                temp.append(round(j, 2))
                print(str(round(j, 2)) + ' ', end='')
            tab_array.append(temp)
            print(']')
        print()

        return pivot_around, tab_array

    def final_results(self, opt_point):
        '''post-processing of results'''
        # change sign of optimal value if MAX problem
        
        opt_value = self.table[-1][-1]
        
        if self.min_max == 'maximize':
            opt_value *= -1.0

        # get values of optimal point
        final_opt_pnt = list()
        for i in [0, 1]:
            if i in opt_point:
                final_opt_pnt.append(self.table[opt_point.index(i)][-1])
            else:
                final_opt_pnt.append(0.0)
        if len(final_opt_pnt) < self.var:
            for i in range(self.var - len(final_opt_pnt)):
                final_opt_pnt.append(0.0)
    
        return final_opt_pnt, opt_value

    def standard_form(self):
        '''
        Convert the given equations into their standard forms by adding 
        slack variables. Also change sign of optimization function if 
        it is a minimization problem so as to solve for maximization.
        '''
        # # add slack variables
        # for eq in self.table:
        #     # zeros = np.zeros(self.constraint_count)  # Array of zeros
        #     # eq = np.concatenate((eq, zeros))  
        #     eq.extend([0] * self.constraint_count)
        # Convert self.table to a Python list
        table_list = self.table.tolist()

        # Add slack variables
        for eq in table_list:
            slack_variables = [0] * self.constraint_count  # Create a list of zeros
            eq.extend(slack_variables)

        # Convert table_list back to a NumPy array if needed
        self.table = np.array(table_list)
        for i, eq in enumerate(self.table[:-1]):
            if self.RHS[i] < 0:
                eq[i + self.var] = -1
            else:
                eq[i + self.var] = 1

        # convert minimization problem to maximization by changing sign
        self.table = np.array(self.table, dtype=float)
        if self.min_max == 'minimize':
            self.table[-1] = self.table[-1] * -1 + 0.0

        self.RHS = np.array(self.RHS)
        self.table = np.hstack((self.table, self.RHS[:, np.newaxis]))

    def add_artf(self):
        '''Add artificial variables if there is no initial
        basic feasible solution (BFS)'''
        bfs = True
        for i in range(self.var, self.var + self.constraint_count):
            if np.sum(self.table[:, i]) != 1:
                bfs = False
                art_var = np.zeros((self.constraint_count + 1, 1))
                art_var[i - self.var] = 1.0
                self.table = np.hstack((self.table, art_var))
                self.table[:, (-2, -1)] = self.table[:, (-1, -2)]

        return bfs

    def new_opt_fun(self):
        '''
        Create a new optimization function for the first phase and embed it
        into the table. Also keep track of the position of artificial variables.
        '''
        artf_vars = list()
        for i in range(self.var + self.constraint_count, self.table.shape[1] - 1):
            row_id = np.where(self.table[:, i] < 0)[0]
            if list(row_id):  # NOTE np.array([0]) considered None
                artf_vars.append(self.var + row_id[0])
                self.table[-1][self.var + row_id[0]] = -1
                self.table[-1] += self.table[row_id[0]]

        return artf_vars

    def simplex(self, opt_point):
        '''
        Loop until the optimal point is reached or we get an infeasible solution
        '''
        steps = []
        pivot_arounds = []
        pivot_around, table = self.pprint(self.table,self.list_var,-1,-1)
        
        steps.append(table)
        pivot_arounds.append(pivot_around)
        while not np.all(self.table[-1][:-1] <= 0):
            pivot_col = np.argmax(self.table[-1][:-1])
            # check for feasibility
            if np.all(self.table[:, pivot_col][:-1] <= 0) or \
                    np.any(self.table[:, pivot_col][:-1] == 0) or \
                    np.all(self.table[:, -1][:-1] < 0):
                opt = "-Inf"
                if self.user_input['objective'] == 'maximize':
                    opt = "Inf"
                return opt,pivot_around,steps
                
                
            theta = self.table[:, -1][:-1] / self.table[:, pivot_col][:-1]
            # check for feasibility
            if np.all(theta < 0):
                return None,pivot_around,steps
                
            # set negative ratios to some large number (+ infinity)
            theta[self.table[:, -1][:-1] < 0] = float('inf')
            theta[self.table[:, pivot_col][:-1] < 0] = float('inf')
            # get pivot and convert pivot row to 1 using row operation
            pivot_row = np.argmin(theta)
            self.table[pivot_row] /= self.table[pivot_row][pivot_col]
            # set Identity matrix using row operations
            for i in range(self.constraint_count + 1):
                if i == pivot_row:
                    continue
                self.table[i] = self.table[i]-(self.table[i][pivot_col]/ \
                        self.table[pivot_row][pivot_col])* \
                        self.table[pivot_row]
            self.list_var[pivot_row] = pivot_col
            #print(self.table)
            pivot_around,table = self.pprint(self.table,self.list_var,pivot_col,pivot_row)
                    
            steps.append(table)
            pivot_arounds.append(pivot_around)
            # keep a record of basic variables
            opt_point[pivot_row] = pivot_col

        return opt_point,pivot_around,steps

    def two_phase(self):
        '''
        Check for initial BFS. If there is an initial BFS, call Simplex else
        save the original OPT function, add artificial variables, get a new OPT
        function, and call the first phase of simplex. If an initial BFS is obtained,
        call the simplex second phase with the original OPT function.
        '''

        # save the original OP function
        Z = self.table[-1]
        bfs = self.add_artf()

        # initial BFS
        init_opt_pt = list(range(self.var, self.var + self.constraint_count))

        # if initial BFS
        if bfs:
            print("\nSimplex Method....")
            opt_point = self.simplex(init_opt_pt)
            return self.final_results(opt_point)

        # if no initial BFS
        # if any RHS is negative, change sign
        neg_RHS = self.table[:, -1] < 0
        self.table[neg_RHS] = self.table[neg_RHS] * -1.0 + 0.0

        # set new OP function with artificial variables
        self.table[-1] = np.zeros(self.table.shape[1])
        artf_vars = self.new_opt_fun()

        # call the first phase
        
        print("\n1st Phase....")

        opt_point,pivot_around,steps = self.simplex(init_opt_pt)
        if (( self.table[-1][self.var]) != -1) or \
            len([i for i in self.table[-1] if i == -1]) > 2  or \
            (len([i for i in self.table[-1] if i == -1]) == 2 and self.table[-1][self.var] != -1) or \
            self.RHS[-1] != 0:
            #opt_value = None
            return 'Bai toan vo nghiem',None,steps,pivot_around

        
        # remove artificial variable set original OP function
        self.table = np.delete(self.table, artf_vars, axis=1)
        self.table[-1] = Z
        

        
        # check for the identity matrix
        for row, col in enumerate(opt_point):
            if col >= len(self.table[-1]):
                #opt_value = None
                return 'Bai toan vo nghiem',None,steps,pivot_around
            if col < self.var:
                self.table[-1] -= self.table[-1][col] * self.table[row]

        # call 2nd phase
        print("\n2nd Phase....")
        opt_point,pivot_around,steps = self.simplex(opt_point)
        if opt_point in ['Inf','-Inf']:
            return 'Bai toan khong gioi noi',opt_point,steps,pivot_around
        elif opt_point is None:
            return 'Bai toan vo nghiem',opt_point,steps,pivot_around
        else:
            opt_point,opt_value = self.final_results(opt_point)
            return opt_point,opt_value,steps,pivot_around
    
    
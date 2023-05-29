import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from Settings import *
import numpy as np
from SolveProblems import solve_problem
from HelpFunctions import show_warning

class MatrixWidget:
    def __init__(self,root,num_var,num_con):
        self.root = root
        self.num_var = int(num_var)
        self.num_con = int(num_con)
        self.popup =  self.__create_popup()
        self.input_frame,self.result_box,self.objective,self.c_coeff,self.coef_constraints,self.inequality_constraints,self.b_values,self.inequality_inequality_constraints = self.__create_coefficient_entry()
        # Force the window to update its geometry
        self.popup.update_idletasks()
         # Get the width and height of the screen
        screen_width = self.popup.winfo_screenwidth()
        screen_height = self.popup.winfo_screenheight()

        popup_max_width = self.root.winfo_screenwidth()
        popup_max_height = self.root.winfo_screenheight()

        # Calculate the coordinates to center the window
        x = int((screen_width - self.popup.winfo_reqwidth()) / 2)
        y = int((screen_height - self.popup.winfo_reqheight()) / 2)

        # Set the position of the window
        self.popup.geometry("+{}+{}".format(x, y))
        #self.popup.maxsize(width=popup_max_width, height=popup_max_height)
        self.popup.resizable(False, False)
        self.popup.transient()
        self.popup.grab_set()
        self.popup.wait_window()


    def __create_popup(self):
        popup = tk.Toplevel(self.root,padx=30, pady=30)
        # Configure the window attributes
        popup.title(f"Nhập hệ số bài toán với {self.num_var} biến và {self.num_con} ràng buộc")
        app_icon = PhotoImage(file = os.path.join(PATH_IMAGES,'icon.png'))
        popup.iconphoto(False,app_icon)
        return popup

    def __show_solution_steps(self):
        self.__solve_problem()

        popup = tk.Toplevel(self.popup, padx=30, pady=30)
        popup.title(f"Chi tiết bước giải")
        app_icon = PhotoImage(file=os.path.join(PATH_IMAGES, 'icon.png'))
        popup.iconphoto(False, app_icon)
        popup.update_idletasks()

        # Disable resizing of the popup window
        popup.resizable(False, False)

        # Get the width and height of the screen
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()

        # Calculate the coordinates to center the window
        x = int((screen_width - popup.winfo_reqwidth()) / 2)
        y = int((screen_height - popup.winfo_reqheight()) / 2)

        # Set the position of the window
        popup.geometry("+{}+{}".format(x, y))

        st_box = ttk.LabelFrame(popup, text="Dạng chuẩn", padding=(20, 10))
        st_box.grid(row = 1 ,column = 0,columnspan=7)
        X = self.standard_form['X']
        constraints = self.standard_form['constraints']
        for i,x in enumerate(X):
            ttk.Label(st_box,text=x,width=10).grid(row = 0,column = i+1)
            for j in range(len(constraints)):
                ttk.Label(st_box,text=f"R.buộc {j+1}",width=10).grid(row = j+1,column = 0)
                ttk.Label(st_box,text=self.standard_form['coeffs'][j,i],width=10).grid(row = j+1,column = i+1)
                ttk.Label(st_box,text = "<=",width=10).grid(row = j+1,column = len(X) + 1)
                ttk.Label(st_box,text = constraints[j][0],width=10).grid(row = j+1,column = len(X) + 2)

            ttk.Label(st_box,text = "H.số b",width=10).grid(row = 0,column = len(X) + 2)
            Objective_Z = "MIN Z"
            if self.standard_form['objective'] == 'maximize':
                Objective_Z = "- MIN Z"
            ttk.Label(st_box,text=Objective_Z,width=10).grid(row = len(constraints)+1,column = 0)
            ttk.Label(st_box,text = -1*self.standard_form['obj_func'][i],width=10).grid(row = len(constraints)+1,column = i + 1)
            X_text = ", ".join(X)
            ttk.Label(st_box,text = f"{X_text} >= 0").grid(row = len(constraints)+2,column = 1,columnspan=len(constraints))

        step_box = ttk.LabelFrame(popup, text="Trình tự các bước giải", padding=(20, 10))
        step_box.grid(row = 2 ,column = 0,pady=10,columnspan=7)
        # Create a canvas inside the step_box
        canvas = tk.Canvas(step_box)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar for the canvas
        scrollbar = ttk.Scrollbar(step_box, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Create a frame inside the canvas to hold the step frames
        step_frame_container = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=step_frame_container, anchor='nw')

        if self.steps:
            print(np.array(self.steps[0]).shape[1] - len(X))
            for i in range(np.array(self.steps[0]).shape[1] - len(X) - 1):
                X.append(f"W{i+1}")
            X.append("RHS")
            for row,step in enumerate(self.steps):
                step_array = np.array(step)
                #step_frame =  ttk.Frame(step_box)
                #step_frame.grid(row = row,pady=5,padx=5)
                step_frame =  ttk.Frame(step_frame_container)
                step_frame.pack(side=tk.TOP, padx=5, pady=5)
                k = 0
                if row == 0:
                   k = 1
                   ttk.Label(step_frame,text = "Start",width = 10).grid(row = 0,column=0)
                elif row == len(self.steps) - 1:
                   k = 1
                   ttk.Label(step_frame,text = "End",width = 10).grid(row = 0,column=0)
                try:
                    pivot_row,pivot_col = self.pivot_arounds[row][0] + 1,self.pivot_arounds[row][1] + 1
                    ttk.Label(step_frame,text = f"Pivot:({pivot_row}, {pivot_col})",width = 10).grid(row = 1+k,column=0)
                except:
                    pass

                for i,x in enumerate(X):
                    ttk.Label(step_frame,text = x,width = 10,borderwidth=5,underline = 0).grid(row = 2+k,column=i+1)

                ttk.Label(step_frame,text = "Z",width = 10,borderwidth=1).grid(row = 3+k,column=0)
                for i in range(step_array.shape[0]):
                    for j in range(step_array.shape[1]):
                        ttk.Label(step_frame,text = round(step_array[i,j],4),width = 10,borderwidth=1).grid(row = i+3+k,column=j+1)
            
        # Update the canvas scrollable region
        canvas.update_idletasks()

        # Configure the canvas scrolling behavior
        canvas.configure(scrollregion=canvas.bbox('all'))

        # Bind the scrollbar to the canvas
        step_frame_container.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        # Set the width of the canvas to allow horizontal scrolling
        canvas.config(width=step_frame_container.winfo_reqwidth())

    def __solve_problem(self):
        try:
            objective = 'minimize'
            if self.objective.get() == 'MAX':
                objective = 'maximize'

            c_coeff_values = [float(c.get()) for c in self.c_coeff]
            coeff_values = []
            for i in range(self.num_con):
                c_value_each_contraint = []
                for j in range(self.num_var):
                    c_value_each_contraint.append(float(self.coef_constraints[j+self.num_var*i].get()))
                coeff_values.append(c_value_each_contraint)

            inequality_constraint_values = [inq_constraint.get() for inq_constraint in self.inequality_constraints]
            b_values = [float(b.get()) for b in self.b_values]
            inequality_inequality_constraints = []
            for c in self.inequality_inequality_constraints:
                if c.get() == '>=0':
                    inequality_inequality_constraints.append('>=')
                elif c.get() == '<=0':
                    inequality_inequality_constraints.append('<=')
                else: 
                    inequality_inequality_constraints.append('None')
            coef_inequality_constraints = np.identity(self.num_var, dtype=float)
            coef_inquality_constraints = np.zeros(self.num_var, dtype=float)

            user_inputs = {
                'objective': objective,
                'c_coeff':  c_coeff_values,
                'coef_constraints': coeff_values,
                'inequality_constraints': inequality_constraint_values,
                'b_value': b_values,
                'coef_inequality_constraints':coef_inequality_constraints,
                'inequality_inequality_constraints': inequality_inequality_constraints,
                'coef_inquality_constraints': coef_inquality_constraints
            }
            self.standard_form,self.solution,self.steps,self.pivot_arounds = solve_problem(user_inputs)

            for child in self.result_box.winfo_children():
                child.destroy()

            solution_box = ttk.Label(self.result_box,text=self.solution)
            solution_box.grid(row = 1,column = 1)

            #save_button = ttk.Button(self.result_box, text="Lưu", style="Accent.TButton", command=None,
            #                        compound=tk.CENTER)
            #save_button.grid(row = 2,column = 3, padx=5,pady=1)

            solution_step_button = ttk.Button(self.result_box, text="Bước giải", style="Accent.TButton", command=self.__show_solution_steps,
                                                compound=tk.CENTER)
            solution_step_button.grid(row = 2,column = 4, padx=5,pady=1)


        except Exception:
            show_warning()
            raise ValueError("Input format error !!!")

    def __del_input(self):
        self.objective.current(1)
        for c in self.c_coeff:
            c.delete(0,'end')
        
        for c in self.coef_constraints:
            c.delete(0,'end')

        for i in self.inequality_constraints:
            i.current(1)
        
        for b in self.b_values:
            b.delete(0,'end')

        for i in self.inequality_inequality_constraints:
            i.current(0)

        self.result_box.destroy()
        self.result_box = ttk.LabelFrame(self.popup, text="Kết quả bài toán", padding=(20, 10))
        self.result_box.grid(row = self.num_con + 3,column = 0,columnspan=7)

    def __create_coefficient_entry(self):
        frame = self.popup
        f_x_label = ttk.Label(frame,text="F(X)",width=10)
        f_x_label.grid(row = 1,column = 0,padx=5,pady=5)
        dk_x_label = ttk.Label(frame,text="Đ.kiện X",width=10)
        dk_x_label.grid(row = self.num_con+2,column = 0,padx=5,pady=5)

        for i in range(self.num_con):
            con_x_label = ttk.Label(frame,text="R.buộc " + str(i+1),width=10)
            con_x_label.grid(row = i + 2,column = 0,padx=5,pady=5)

        c_coeff = []
        inequality_inequality_constraints = []
        for i in range(1,self.num_var+1):
            entry = ttk.Label(frame,text="X"+str(i),width=7,anchor="center")
            entry.grid(row = 0,column = i,padx=5,pady=5)

            opti_entry = ttk.Entry(frame,width=7)
            opti_entry.grid(row = 1,column = i,padx=5,pady=1)
            c_coeff.append(opti_entry)

            choices = ['>=0', '<=0', 'None']
            combo = ttk.Combobox(frame, values=choices,width=5,state="readonly")
            combo.current(0)
            combo.grid(row = self.num_con+2,column = i,padx=5,pady=1)
            inequality_inequality_constraints.append(combo)

        ttk.Label(frame,text="Hệ số b",width=7,anchor="center").grid(row = 0,column = self.num_var+3,padx=5,pady=5)
        coef_constraints = []
        for j in range(self.num_con):
            for i in range(1,self.num_var+1):
                entry = ttk.Entry(frame,width=7)
                entry.grid(row = j + 2,column = i,padx=5,pady=1)
                coef_constraints.append(entry)

        choices = ['MAX','MIN']
        objective = ttk.Combobox(frame, values=choices,width=5,state="readonly")
        objective.current(1)
        objective.grid(row = 1 ,column = self.num_var+2,padx=5,pady=5)
    
        inequality_constraints = []
        b_values = []
        for j in range(self.num_con):
            choices = ['>=', '<=', '=']
            combo = ttk.Combobox(frame, values=choices,width=5,state="readonly")
            combo.current(1)
            combo.grid(row = j+2,column=self.num_var+2,padx=5,pady=1)

            entry = ttk.Entry(frame,width=7)
            entry.grid(row = j+2,column = self.num_var+3,padx=5,pady=1)
            b_values.append(entry)
            inequality_constraints.append(combo)

        del_button = ttk.Button(frame , text="Xoá",style="Accent.TButton", width = 8,
                        command=self.__del_input)
        del_button.grid(row = self.num_con + 2,column = self.num_var + 2, padx=5,pady=1)

        solve_button = ttk.Button(frame , text="Giải",style="Accent.TButton", width = 8,
                        command=self.__solve_problem)
        solve_button.grid(row = self.num_con + 2,column = self.num_var + 3, padx=5,pady=1)

        
        result_box = ttk.LabelFrame(self.popup, text="Kết quả bài toán", padding=(20, 10))
        result_box.grid(row = self.num_con + 3,column = 0,columnspan=7)
        return frame,result_box,objective,c_coeff,coef_constraints,inequality_constraints,b_values,inequality_inequality_constraints


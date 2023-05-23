import tkinter as tk
from tkinter import ttk,PhotoImage
import os
import PIL
from PIL import Image, ImageTk
from Settings import *
from HelpFunctions import show_warning,check_integer
from MatrixWidget import MatrixWidget

class InputWidget():
        def __init__(self,root):
            self.root = root
            self.input_box = self.__create_input_box()
            self.var_entry = self.__create_var_entry()
            self.con_entry = self.__create_con_entry()
            self.__create_button(self.input_box)
            self.__add_logo()

        def __on_entry_click(self,event, entry, placeholder):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(foreground='black') 

        def __on_focusout(self,event, entry, placeholder):
            if entry.get() == '':
                entry.insert(0, placeholder)
                entry.config(foreground='grey')

        def __create_input_box(self):
            input_box = ttk.LabelFrame(self.root, text="Khởi tạo bài toán", padding=(20, 10))
            input_box.place(anchor="c", relx=.5, rely=.6,relwidth=0.8)
            input_box.columnconfigure(0, weight=1)
            input_box.columnconfigure(1, weight=1)
            return input_box

        def __create_var_entry(self):
            # Create labels and input boxes for number of variables and constraints
            var_placeholder = "Số lượng biến"
            var_entry = ttk.Entry(self.input_box)
            var_entry.insert(0,var_placeholder)
            var_entry.bind('<FocusIn>', lambda event: self.__on_entry_click(event, var_entry, var_placeholder))
            var_entry.bind('<FocusOut>', lambda event: self.__on_focusout(event, var_entry, var_placeholder))
            var_entry.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
            return var_entry

        def __create_con_entry(self):
            con_placeholder = "Số lượng ràng buộc"
            con_entry = ttk.Entry(self.input_box)
            con_entry.insert(0,con_placeholder)
            con_entry.bind('<FocusIn>', lambda event: self.__on_entry_click(event, con_entry, con_placeholder))
            con_entry.bind('<FocusOut>', lambda event: self.__on_focusout(event, con_entry, con_placeholder))
            con_entry.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
            return con_entry

        def __submit_form(self):
                # Get the values from the entry fields
            var_value = self.var_entry.get()
            con_value = self.con_entry.get()

            if  check_integer(var_value) and check_integer(con_value) and int(var_value) > 0 and int(con_value) > 0:
                MatrixWidget(self.root,var_value,con_value)
            else:
                show_warning()
        

        def __clear_input(self):
            var_placeholder = "Số lượng biến"
            con_placeholder = "Số lượng ràng buộc"
            self.var_entry.delete(0, 'end')
            self.var_entry.insert(0,var_placeholder)
            self.var_entry.config(foreground='grey')

            self.con_entry.delete(0, 'end')
            self.con_entry.insert(0,con_placeholder)
            self.con_entry.config(foreground='grey')

        def __create_button(self,input_box):
            submit_button = ttk.Button(input_box , text="Nhập",style="Accent.TButton", padding=(5, 5),
                                            command=self.__submit_form)
            submit_button.grid(row = 3,column = 0, sticky='e',padx=5)

            cancel_button = ttk.Button(input_box , text="Xoá",style="Accent.TButton", padding=(5, 5),
                                            command=self.__clear_input)
            cancel_button.grid(row = 3,column = 1, sticky='w',padx=5)

        def __add_logo(self):
            # Load logo image
            logo_path = os.path.join(PATH_IMAGES, 'KHTN_logo.png')
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((200, 200)) 
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            logo_widget = tk.Label(self.root, image=self.logo_photo)
            logo_widget.place(relx=0.5, rely=0.2, anchor="center")


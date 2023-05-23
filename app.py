import tkinter as tk
from tkinter import *
from tkinter import ttk,font
from Settings import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style(self)
        self.resizable(False, False)
        self.tk.call("source", os.path.join(PATH_THEME,"forest-light.tcl"))
        #self.tk.call("source", os.path.join(PATH_THEME,"forest-dark.tcl"))
        self.style.theme_use("forest-light")

        # Set the font for all widgets in the application
        font = ('Verdana', 10)
        self.option_add('*Font', font)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = screen_width/2 - WINDOW_WIDTH/2
        y = screen_height/2 - WINDOW_HEIGHT/2

        self.geometry("{}x{}+{}+{}".format(WINDOW_WIDTH,WINDOW_HEIGHT,int(x),int(y)))
        self.title("OptiSolver - Linear Programing Solver")
        app_icon = PhotoImage(file = os.path.join(PATH_IMAGES,'icon.png'))
        self.iconphoto(False,app_icon)

    def __create_main_screen(self):
        pass
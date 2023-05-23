import tkinter as tk
from tkinter import *
from Menu import *
from Settings import *
from app import App
from InputFormWidget import *
from MatrixWidget import*

if __name__ == '__main__':
    # Initialize application
    root = App()
    # Create a menu bar
    menu = MenuBar(root)
    # Create a problem initialization form
    input_widge = InputWidget(root)

    root.mainloop()
    
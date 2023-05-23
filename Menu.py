from tkinter import Menu
import tkinter


def show_about():
    app_name = "OptiSolver - Linear Programing Solver"
    about = "The software is a project for the course of Linear Programming at HCMUS, not for profit purposes."
    version = "1.0"
    author = " 20280053 - Cao Huynh Anh Khoa \n  20280099 - Tran Minh Tien"
    license_info = "Copyright (c) 2023"
    message = f"{app_name} version {version}\n\n"\
              f"{about}\n\n"\
              f"Authors:\n {author}\n\n"\
              f"{license_info}"
    tkinter.messagebox.showinfo("About", message)


class MenuBar():
    def __init__(self,root):
        self.root = root
        # Create a menubar
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        self.__create_file_menu()
        self.__create_help_menu()

    def __create_file_menu(self):
        # Create a menu
        file_menu = Menu(self.menubar,tearoff=False)
        # add a menu item to the menu
        #file_menu.add_command(
            #label = 'Open'
        #)
        #file_menu.add_command(
            #label = 'Save'
        #)
        file_menu.add_separator()
        file_menu.add_command(
            label = 'Exit',
            command=self.root.destroy,
        )
        # add the File menu to the menubar
        self.menubar.add_cascade(
            label="File",
            menu=file_menu,
            underline=0
        )

    def __create_help_menu(self):
        help_menu = Menu(self.menubar,tearoff=False)
        help_menu.add_separator()
        help_menu.add_command(label = 'About',command=show_about)
        self.menubar.add_cascade(
            label="Help",
            menu=help_menu,
            underline=0
        )

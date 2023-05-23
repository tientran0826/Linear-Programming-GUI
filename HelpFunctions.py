from tkinter import messagebox

def show_warning():
    messagebox.showinfo("Warning",  "Giá trị nhập vào không hợp lệ !!!")

def check_integer(value):
    try:
        if int(value) == float(value):
            return True
    except:
            return False

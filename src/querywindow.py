import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *


class QueryWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('SQL Query')
        self.geometry('500x600+100+100')
        self.resizable(False, False)
        self.configure(background='#e8f4f8')

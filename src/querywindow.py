import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *

from common import ToplevelWindow


class QueryWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('SQL Query')
        self.geometry('500x600+100+100')

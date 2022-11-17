import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *

from common import ToplevelWindow


class DescribeWindow(tk.Toplevel):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.title('Describe')
        self.geometry('500x600+100+100')

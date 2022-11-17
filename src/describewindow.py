import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *

from common import ToplevelWindow


class SourceFrame(ttk.LabelFrame):
    def __init__(self, *args, text='Source', **kwargs):
        super().__init__(*args, text=text, **kwargs)
        

    def pack(self, fill=BOTH, expand=True, side=TOP):
        super().pack(fill=fill, expand=expand, side=side)


class DescribeWindow(tk.Toplevel):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.title('Description')
        self.geometry('500x600+100+100')

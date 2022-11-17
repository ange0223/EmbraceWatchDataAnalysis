import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *

from common import ToplevelWindow


class ExportWindow(tk.Toplevel):
    def __init__(self, on_submit=None):
        super().__init__()
        self.on_submit = on_submit
        self.title('Describe')
        self.geometry('500x600+100+100')

    def submit(self):
        options = {} # placeholder options, get options instead
        self.on_submit(options)

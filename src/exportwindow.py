import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askdirectory
from data import *

from common import ToplevelWindow


class ExportWindow(tk.Toplevel):
    def __init__(self, on_submit=None):
        super().__init__()
        self.submit_callback = on_submit
        #self.title('Describe')
        #self.geometry('500x600+100+100')

    def submit(self):
        options = {} # placeholder options, get options instead
        self.on_submit(options)

    def save_file(self):
        #save_prompt = asksaveasfile(initialfile = 'Untitled.txt', defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        save_path = asksaveasfile(mode='a', initialfile = 'untitled.csv', defaultextension=".csv")
        self.submit_callback.to_csv(save_path.name)


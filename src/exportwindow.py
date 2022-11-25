import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askdirectory
from data import *

from common import ToplevelWindow

def open_save_dialog(df):
    save_path = asksaveasfile(mode='a', filetypes=[('CSV', '*.csv')],
                              initialfile='untitled.csv',
                              defaultextension=".csv")
    if save_path:
        df.to_csv(save_path.name, index=False)


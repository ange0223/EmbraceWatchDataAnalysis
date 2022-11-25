import tkinter as tk
from tkinter import ttk
import datetime


DATE_FMT = '%Y-%m-%d %H:%M:%S'


def str_to_datetime(string):
    return datetime.strptime(string, DATE_FMT)


class ToplevelWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resizable(False, False)
        self.configure(background='#e8f4f8')


class ScrollableLabelFrame(ttk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        # Configure event triggered anytime the window is changed or mouse
        # clicked
        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(
                # set canvas scroll region to the bounding box of all items
                # within the canvas
                scrollregion=canvas.bbox('all')
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

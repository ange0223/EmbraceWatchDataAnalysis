import tkinter as tk
from tkinter import ttk


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


class Checkbutton(ttk.Checkbutton):
    def __init__(self, parent, **kwargs):
        self._var = tk.IntVar()
        super().__init__(parent, variable=self._var,
                       **kwargs)

    def get(self):
        return self._var.get()

    def set(self, val):
        self._var.set(val)

    def toggle(self):
        self.set(1 - self.get())

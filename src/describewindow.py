import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *

from common import ToplevelWindow


class Label(ttk.Label):
    def __init__(self, parent, *args, background='#e8f4f8',
                 font_family='Helvetica', font_size=14, **kwargs):
        super().__init__(parent, *args, background=background,
                         font=(font_family, font_size))

    def pack(self, side=LEFT, **kwargs):
        super().pack(side=side, **kwargs)


class SourceFrame(ttk.LabelFrame):
    def __init__(self, *args, text='Source', **kwargs):
        super().__init__(*args, text=text, **kwargs)
        top_frame = ttk.Frame(self)
        Label(top_frame, text='Series: ').pack()
        self.series_lbl = Label(top_frame, text='series')
        self.series_lbl.pack()
        Label(top_frame, text='Aggregate by: ').pack()
        self.agg_by_lbl = Label(top_frame, text='aggregate by')
        self.agg_by_lbl.pack()
        Label(top_frame, text='Aggregate metric: ').pack()
        self.agg_metric_lbl = Label(top_frame, text='aggregate metric')
        self.agg_metric_lbl.pack()
        self.refresh_btn = ttk.Button(
            top_frame,
            text='Refresh',
            command=self.refresh
        )
        self.refresh_btn.pack(side=LEFT)

    def refresh(self):
        print('SourceFrame.refresh()')

    def pack(self, fill=BOTH, expand=True, side=TOP):
        super().pack(fill=fill, expand=expand, side=side)


class DescriptionFrame(ttk.LabelFrame):
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

        self.source_frame = SourceFrame(self)
        self.source_frame.pack(fill=BOTH, expand=True, side=TOP)

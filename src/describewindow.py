import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *

from common import ToplevelWindow


class Label(ttk.Label):
    def __init__(self, parent, background='#e8f4f8', font_family='Helvetica',
                 font_size=14, font_bold=False, **kwargs):
        font = '{family} {size}{bold}'.format(
            family=font_family,
            size=font_size,
            bold=' bold' if font_bold else ''
        )
        super().__init__(parent, background=background, font=font, **kwargs)

    def pack(self, expand=False, fill=None, side=LEFT, ipady=5,
             **kwargs):
        super().pack(expand=expand, fill=fill, side=side, ipady=ipady, **kwargs)


class NameLabel(Label):
    def __init__(self, parent, font_size=16, font_bold=True, **kwargs):
        super().__init__(parent, font_size=font_size, font_bold=font_bold,
                         **kwargs)


class ValueLabel(Label):
    def pack(self, padx=(0, 30), **kwargs):
        super().pack(padx=padx, **kwargs)


class SourceFrame(ttk.LabelFrame):
    def __init__(self, *args, text='Source', **kwargs):
        super().__init__(*args, text=text, **kwargs)
        top_frame = ttk.Frame(self)
        NameLabel(top_frame, text='Series: ').pack()
        self.series_lbl = ValueLabel(top_frame, text='series')
        self.series_lbl.pack()
        NameLabel(top_frame, text='Aggregate by: ').pack()
        self.agg_by_lbl = ValueLabel(top_frame, text='aggregate by')
        self.agg_by_lbl.pack()
        NameLabel(top_frame, text='Aggregate metric: ').pack()
        self.agg_metric_lbl = ValueLabel(top_frame, text='aggregate metric')
        self.agg_metric_lbl.pack()
        self.refresh_btn = ttk.Button(
            top_frame,
            text='Refresh',
            command=self.refresh
        )
        self.refresh_btn.pack(side=LEFT)
        top_frame.pack(expand=True, fill=BOTH, side=LEFT)
        bottom_frame = ttk.Frame(self)
        NameLabel(bottom_frame, text='Data: ').pack()
        # TODO - configure different options for data dropdown
        self.data_drop = ttk.OptionMenu(
            bottom_frame,
            tk.StringVar(),
            'all',
            ['all']
        )
        self.data_drop.pack(expand=True, fill=BOTH, side=LEFT)
        NameLabel(bottom_frame, text='Groupby: ').pack()
        # TODO - configure different options for groupby dropdown
        self.groupby_drop = ttk.OptionMenu(
            bottom_frame,
            tk.StringVar(),
            '',
            ['']
        )
        self.groupby_drop.pack(expand=True, fill=BOTH, side=LEFT)
        bottom_frame.pack(expand=True, fill=BOTH, side=TOP)

    def refresh(self):
        print('SourceFrame.refresh()')

    def pack(self, expand=True, fill=BOTH, side=TOP):
        super().pack(fill=fill, expand=expand, side=side)


class DescriptionFrame(ttk.LabelFrame):
    def __init__(self, *args, text='Description', **kwargs):
        super().__init__(*args, text=text, **kwargs)

    def pack(self, expand=True, fill=BOTH, side=TOP):
        super().pack(expand=expand, fill=fill, side=side)


class DescribeWindow(tk.Toplevel):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.title('Description')
        self.geometry('900x600+100+100')
        self.source_frame = SourceFrame(self)
        self.source_frame.pack()
        self.description_frame = DescriptionFrame(self)
        self.description_frame.pack()



if __name__ == '__main__':
    dw = DescribeWindow(None)
    dw.mainloop()

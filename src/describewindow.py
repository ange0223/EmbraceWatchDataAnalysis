'''
describewindow.py

Pandas offset aliases: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
'''
import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

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

    def pack(self, expand=False, fill=X, side=LEFT, ipady=5,
             **kwargs):
        super().pack(expand=expand, fill=fill, side=side, ipady=ipady, **kwargs)


class NameLabel(Label):
    def __init__(self, parent, font_size=16, font_bold=True, **kwargs):
        super().__init__(parent, font_size=font_size, font_bold=font_bold,
                         **kwargs)


class ValueLabel(Label):
    def pack(self, padx=(0, 30), **kwargs):
        super().pack(padx=padx, **kwargs)


class DropDown(ttk.OptionMenu):
    def __init__(self, parent, tkvar, default, *options):
        super().__init__(parent, tkvar, default, *options)
        self._var = tkvar

    def get(self):
        return self._var.get()

    def pack(self, expand=False, fill=None, side=LEFT, padx=(0, 30), **kwargs):
        super().pack(expand=expand, fill=fill, side=side, padx=padx, **kwargs)


class SourceFrame(ttk.LabelFrame):
    def __init__(self, parent, series, interval, agg_metric, text='Source',
                 **kwargs):
        super().__init__(parent, text=text, **kwargs)
        top_frame = ttk.Frame(self)
        NameLabel(top_frame, text='Series: ').pack()
        self.series_lbl = ValueLabel(top_frame, text=series)
        self.series_lbl.pack()
        NameLabel(top_frame, text='Aggregate by: ').pack()
        self.agg_by_lbl = ValueLabel(top_frame, text=interval)
        self.agg_by_lbl.pack()
        NameLabel(top_frame, text='Aggregate metric: ').pack()
        self.agg_metric_lbl = ValueLabel(top_frame, text=agg_metric)
        self.agg_metric_lbl.pack()
        self.refresh_btn = ttk.Button(
            top_frame,
            text='Refresh',
            command=self.refresh
        )
        self.refresh_btn.pack(side=LEFT)
        top_frame.pack(expand=False, fill=X, side=TOP)
        bottom_frame = ttk.Frame(self)
        NameLabel(bottom_frame, text='Data: ').pack()
        # TODO - configure different options for data dropdown
        self.data_drop = DropDown(
            bottom_frame,
            tk.StringVar(),
            'all',
            ['all']
        )
        self.data_drop.pack()
        NameLabel(bottom_frame, text='Groupby: ').pack()
        # TODO - configure different options for groupby dropdown
        self.groupby_drop = DropDown(
            bottom_frame,
            tk.StringVar(),
            'None',
            ['None']
        )
        self.groupby_drop.pack()
        bottom_frame.pack(expand=False, fill=BOTH, side=TOP)

    def refresh(self):
        print('SourceFrame.refresh()')

    def pack(self, expand=False, fill=X, side=TOP):
        super().pack(fill=fill, expand=expand, side=side)


class TableCell(ttk.Label):
    def __init__(self, parent, anchor=W, borderwidth=1, font_bold=False,
                 font_family='Helvetica', font_size=12, relief='solid',
                 **kwargs):
        font = '{family} {size}{bold}'.format(
            family=font_family,
            size=font_size,
            bold=' bold' if font_bold else ''
        )
        super().__init__(parent, anchor=anchor, borderwidth=borderwidth,
                         font=font, relief=relief, **kwargs)

    def grid(self, sticky='nsew', **kwargs):
        super().grid(sticky=sticky, **kwargs)


class DescriptionTable(ttk.Frame):
    def __init__(self, parent, series, **kwargs):
        super().__init__(parent, **kwargs)
        self.series = series
        self.data = None
        self.cells = []
        self._populate()

    def update(self, data):
        self.data = data
        self._clear()
        self._populate()

    def _clear(self):
        for cell in self.cells:
            cell.destroy()

    def _populate(self):
        if self.data is None:
            return
        max_width = max(len(series), 5)
        header = TableCell(self, background='#333333', foreground='#f0f0f0',
                           text=self.series, width=6+max_width)
        header.grid(column=0, row=0, columnspan=2)
        self.cells.append(header)
        for row, (index, value) in enumerate(self.data.items(), start=1):
            label_cell = TableCell(self, background='#dddddd', text=index,
                                   width=6)
            label_cell.grid(column=0, row=row)
            self.cells.append(label_cell)
            str_value = '{:.3f}'.format(value)
            value_cell = TableCell(self, text=str_value, width=max_width)
            value_cell.grid(column=1, row=row)
            self.cells.append(value_cell)

    def pack(self, expand=True, fill=Y, side=LEFT, padx=20, pady=20, **kwargs):
        super().pack(expand=expand, fill=fill, side=side, padx=padx, pady=pady,
                     **kwargs)


class PlotFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._plot = None

    def pack(self, expand=True, fill=Y, side=LEFT, **kwargs):
        super().pack(expand=expand, fill=fill, side=side, **kwargs)

    def clear(self):
        if self._plot is None:
            return
        self._plot.get_tk_widget().destroy()

    def plot(self, data, figsize=(7,4), fig_dpi=100):
        fig = Figure(figsize=figsize, dpi=fig_dpi)
        self._plot = FigureCanvasTkAgg(fig, master=self)
        self._plot.get_tk_widget().pack(fill=BOTH, expand=True)
        ax = fig.add_subplot()
        data.plot(kind='bar', ax=ax)


class DescriptionFrame(ttk.LabelFrame):
    def __init__(self, parent, data, series, text='Description', **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.data = data
        self.series = series
        self.plot_frame = PlotFrame(self)
        self.plot_frame.plot(self.data)
        self.plot_frame.pack()
        self.table_frame = DescriptionTable(self, series)
        self.table_frame.pack()
        self._populate()

    def pack(self, expand=False, fill=Y, side=TOP):
        super().pack(expand=expand, fill=fill, side=side)

    def update(self, data):
        self.data = data
        self.plot_frame.clear()
        self.plot_frame.plot(self.data)
        self._populate()

    def _populate(self):
        # TODO: Add additional stats to summary data
        summary_data = self.data[self.series].describe()
        self.table_frame.update(summary_data)


class DescribeWindow(tk.Toplevel):
    def __init__(self, data, series, interval, agg_metric, time_min, time_max):
        super().__init__()
        self.data = data
        self.series = series
        self.interval = interval
        self.agg_metric = agg_metric
        self.time_min = time_min
        self.time_max = time_max
        self.title('Description')
        self.geometry('900x600+100+100')
        self.source_frame = SourceFrame(self, series, interval, agg_metric)
        self.source_frame.pack()
        self.description_frame = DescriptionFrame(self, data, series)
        self.description_frame.pack()
        self._update_source()
        self._update_description()

    def _update_source(self):
        # TODO
        pass

    def _update_description(self):
        # TODO: Use self.agg_metric instead of assuming 'mean()'
        data = self.data[['Datetime', self.series]]
        data = data[
            (data['Datetime'] > self.time_min)
            & (data['Datetime'] < self.time_max)
        ]
        data = data.set_index('Datetime')
        data = data.resample(rule=self.interval).mean()
        self.description_frame.update(data)

    def update_time(self, time_min, time_max):
        self.time_min = time_min
        self.time_max = time_max
        self._update_source()
        self._update_description()



if __name__ == '__main__':
    from data import load_data
    data = load_data('Dataset', users=310, start_time=None, end_time=None,
                     utc_mode=False, show_acc=True, show_eda=False,
                     show_temp=False, show_movement=False, show_step=False,
                     show_rest=False, show_wrist=False)
    series = 'Acc magnitude avg'
    interval = '5H'
    agg_metric = 'mean'
    time_min = min(data['Datetime'])
    time_max = max(data['Datetime'])
    dw = DescribeWindow(data, series, interval, agg_metric, time_min, time_max)
    dw.mainloop()

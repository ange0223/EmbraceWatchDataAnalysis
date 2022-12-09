"""
describewindow.py

Pandas offset aliases: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
"""
import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
matplotlib.use('TkAgg')


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
    def __init__(self, parent, text='Source',
                 **kwargs):
        super().__init__(parent, text=text, **kwargs)
        top_frame = ttk.Frame(self)
        NameLabel(top_frame, text='Series: ').pack()
        self.series_lbl = ValueLabel(top_frame, text='series')
        self.series_lbl.pack()
        NameLabel(top_frame, text='Aggregate by: ').pack()
        self.agg_by_lbl = ValueLabel(top_frame, text='interval')
        self.agg_by_lbl.pack()
        NameLabel(top_frame, text='Aggregate metric: ').pack()
        self.agg_metric_lbl = ValueLabel(top_frame, text='agg_metric')
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
        # NOTE - configure different options for data dropdown
        self.data_drop = DropDown(
            bottom_frame,
            tk.StringVar(),
            'all',
            ['all']
        )
        self.data_drop.pack()
        NameLabel(bottom_frame, text='Groupby: ').pack()
        # NOTE - configure different options for groupby dropdown
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

    def update_info(self, series, interval, agg_metric):
        self.series_lbl.config(text=series)
        self.agg_by_lbl.config(text=interval)
        self.agg_metric_lbl.config(text=agg_metric)

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
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.cells = []

    def clear(self):
        for cell in self.cells:
            cell.destroy()

    def populate(self, data, header_text):
        max_width = max(len(header_text), 5)
        header = TableCell(self, background='#333333', foreground='#f0f0f0',
                           text=header_text, width=6+max_width)
        header.grid(column=0, row=0, columnspan=2)
        self.cells.append(header)
        for row, (index, value) in enumerate(data.items(), start=1):
            label_cell = TableCell(self, background='#dddddd', text=index,
                                   width=6)
            label_cell.grid(column=0, row=row)
            self.cells.append(label_cell)
            # Leave off decimal points if they're zero
            if value == int(value):
                str_value = '{}'.format(int(value))
            else:
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

    def pack(self, expand=True, fill=BOTH, side=LEFT, padx=5, pady=5, **kwargs):
        super().pack(expand=expand, fill=fill, side=side, padx=padx, pady=pady,
                     **kwargs)

    def clear(self):
        if self._plot is None:
            return
        self._plot.get_tk_widget().destroy()

    def plot(self, data, series, figsize=(7,5), fig_dpi=100):
        fig = Figure(figsize=figsize, dpi=fig_dpi)
        self._plot = FigureCanvasTkAgg(fig, master=self)
        self._plot.get_tk_widget().pack(fill=BOTH, expand=False)
        ax = fig.add_subplot()
        ax.set_xlabel(series)
        ax.set_ylabel('probability')
        data.plot(kind='bar', ax=ax)
        fig.tight_layout()


class DescriptionFrame(ttk.LabelFrame):
    def __init__(self, parent, text='Description', **kwargs):
        super().__init__(parent, text=text, **kwargs)
        self.plot_frame = PlotFrame(self)
        self.plot_frame.pack()
        self.table_frame = DescriptionTable(self)
        self.table_frame.pack()

    def pack(self, expand=True, fill=Y, side=TOP):
        super().pack(expand=expand, fill=fill, side=side)

    def update_info(self, data, series, bins=30):
        plot_data = data.copy()
        # NOTE - Allow for user-specified bin size
        plot_data['bin'] = pd.qcut(plot_data[series], bins, duplicates='drop')
        plot_data = plot_data['bin'].value_counts()/len(plot_data['bin'])
        # NOTE - Add additional stats to summary data
        summary_data = pd.Series({
            'count': data[series].count(),
            'mean': data[series].mean(),
            'std': data[series].std(),
            'min': data[series].min(),
            '0.2%': data[series].quantile(0.002),
            '2.5%': data[series].quantile(0.025),
            '25%': data[series].quantile(0.25),
            '50%': data[series].quantile(0.975),
            '75%': data[series].quantile(0.75),
            '99.9%': data[series].quantile(0.999),
            'max': data[series].max(),
            'kurt': data[series].kurt(),
            'skew': data[series].skew()
        })
        self.plot_frame.clear()
        self.table_frame.clear()
        self.plot_frame.plot(plot_data, series)
        self.table_frame.populate(summary_data, series)


class DescribeWindow(tk.Toplevel):
    def __init__(self, series):
        super().__init__()
        self.title('Description')
        self.geometry('900x600+100+100')
        self.series = series
        self.source_frame = SourceFrame(self)
        self.source_frame.pack()
        self.description_frame = DescriptionFrame(self)
        self.description_frame.pack()

    def update_info(self, data, interval, agg_metric='mean'):
        self.source_frame.update_info(self.series, interval, agg_metric)
        self.description_frame.update_info(data, self.series)


if __name__ == '__main__':
    from data import load_data
    data = load_data('Dataset', users=310, start_time=None, end_time=None,
                     utc_mode=False, show_acc=True, show_eda=True,
                     show_temp=True, show_movement=True, show_step=True,
                     show_rest=True, show_wrist=True)

    series = 'Movement intensity'
    interval = '30min'
    dt_min = min(data['Datetime'])
    dt_max = max(data['Datetime'])
    dw_data = data[['Datetime', series]]
    dw_data.index = dw_data['Datetime']
    dw_data = dw_data.drop('Datetime', axis=1)
    dw_data = dw_data[(dw_data.index > dt_min) & (dw_data.index < dt_max)]
    dw_data = dw_data.set_index('Datetime')
    dw_data = dw_data.resample(rule=interval).mean()
    dw = DescribeWindow()
    dw.update_info(dw_data, series, interval)
    dw.mainloop()

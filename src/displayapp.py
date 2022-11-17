import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from datetime import datetime

from data import load_data, get_subject_ids
from importwindow import ImportWindow
from common import ScrollableLabelFrame

DEFAULT_DATA_PATH = 'Dataset'


class DataMenu(Menu):
    def __init__(self, parent, on_import=None, on_export=None, on_clear=None):
        super().__init__(parent)
        self.add_command(label='Import', command=on_import)
        self.add_command(label='Export', command=on_export)
        self.add_command(label='Clear', command=on_clear)


class TimeSeriesMenu(Menu):
    def __init__(self, parent, on_placeholder=None):
        super().__init__(parent)
        self.add_command(label='Placeholder', command=on_placeholder)


class AnalysisMenu(Menu):
    def __init__(self, parent, on_placeholder=None):
        super().__init__(parent)
        self.add_command(label='Placeholder', command=on_placeholder)


class TimeEntry(ttk.Entry):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


class TimeRangeSelector(ttk.Frame):
    def __init__(self, parent, *args, on_apply=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_callback = on_apply
        self.time_min_entry = TimeEntry(self)
        self.time_min_entry.insert(0, '')
        self.time_min_entry.pack(side=LEFT)
        self.time_max_entry = TimeEntry(self)
        self.time_max_entry.insert(0, '')
        self.time_max_entry.pack(side=LEFT)
        time_apply_btn = ttk.Button(
            self,
            text='Apply',
            command=self.apply
        )
        time_apply_btn.pack(side=LEFT)

    def apply(self):
        if not self.apply_callback:
            return
        print(self.apply_callback)
        self.apply_callback(self.time_min_entry.get(), self.time_max_entry.get())

    def get(self):
        return self.time_min_entry.get(), self.time_max_entry.get()

    def set(self, time_min, time_max):
        self.time_min_entry.insert(0, str(time_min))
        self.time_max_entry.insert(0, str(time_max))

    def pack(self):
        super().pack(fill=BOTH, side=TOP)


class DisplayApp(tk.Tk):
    def __init__(self, data_path=DEFAULT_DATA_PATH):
        super().__init__()
        # Use provided data_path and data options to load data
        self.data_path = data_path
        self.subject_ids = sorted(list(get_subject_ids(data_path)))
        self.data = None
        self.plots = [] # used to easily reference displayed plots
        self._active_data = None
        self.describe_window = None
        self.title('Data Analyzer')
        self.geometry('900x600+50+50')
        self.resizable(True, True)
        self.configure(background='#e8f4f8')

        menubar = Menu(self)
        data_menu = DataMenu(
            menubar,
            on_import=self.open_import_window,
            on_export=lambda : print('Data > Export pressed'),
            on_clear=self.clear
        )
        time_series_menu = TimeSeriesMenu(
            menubar,
            on_placeholder=lambda : print('Time Series > Placeholder pressed')
        )
        analysis_menu = AnalysisMenu(
            menubar,
            on_placeholder=lambda : print('Analysis > Placeholder pressed')
        )
        menubar.add_cascade(label='Data', menu=data_menu)
        menubar.add_cascade(label='Time Series', menu=time_series_menu)
        menubar.add_cascade(label='Analysis', menu=analysis_menu)
        self.config(menu=menubar)

        self.time_selector = TimeRangeSelector(
            self,
            on_apply=self.on_time_apply
        )
        self.time_selector.pack()

        self.frame = ScrollableLabelFrame(self, text='')
        self.frame.pack(fill=BOTH, expand=True, side=BOTTOM)

    @property
    def active_data(self):
        return self._active_data

    @active_data.setter
    def active_data(self, data):
        '''
        Need to update several different things when active data changes
        '''
        self._active_data = data
        self.clear()
        self.load_plots()
        self.update_describe_window()

    def on_time_apply(self, time_min, time_max):
        print('DisplayApp.on_time_apply()')
        if self.data is None:
            return
        self.active_data = self.data[
            (self.data['Datetime'] > time_min)
            & (self.data['Datetime'] < time_max)
        ]

    def update_describe_window(self):
        if self.describe_window is None:
            return
        # TODO
        #self.describe_window.update_time(time_min, time_max)
        # or
        #self.describe_window.update_data(self.active_data)

    def open_import_window(self):
        print('DisplayApp.open_import_window()')
        top = ImportWindow(self.subject_ids, on_submit=self.on_import_submit)
        top.lift()
        top.mainloop()

    def on_import_submit(self, options):
        print('DisplayApp.on_import_submit()')
        self.data = load_data(self.data_path, **options)
        time_min = min(self.data['Datetime'])
        time_max = max(self.data['Datetime'])
        self.time_selector.set(time_min, time_max)
        self.on_time_apply(time_min, time_max)
        self.clear()
        self.load_plots()

    def clear(self):
        print('DisplayApp.clear()')
        for plot in self.plots:
            plot.get_tk_widget().destroy()
        self.plots = []

    def load_plots(self):
        print('DisplayApp.load_plots()')
        # Get column names to show
        figure_cols = set(self.active_data.columns)
        ignore_cols = {'Datetime', 'Timezone (minutes)',
                'Unix Timestamp (UTC)', 'subject_id'}
        figure_cols = figure_cols - ignore_cols

        subject_id = self.active_data['subject_id'].unique()[0]
        subject = self.active_data[self.active_data['subject_id'] == subject_id]

        fig_size = (9, 4)
        fig_dpi = 100
        for col_name in sorted(figure_cols):
            fig = Figure(figsize=fig_size, dpi=fig_dpi)
            ax = fig.add_subplot(111)
            subject.plot(x='Datetime', y=col_name, ax=ax)
            data_plot = FigureCanvasTkAgg(fig,
                    master=self.frame.scrollable_frame)
            self.plots.append(data_plot)
            data_plot.draw()
            data_plot.get_tk_widget().pack(fill=X, expand=True)



if __name__ == '__main__':
    date_fmt = '%Y-%m-%d %H:%M:%S'
    options = {
        'users': [310, 311],
        'start_time': datetime.strptime('2020-01-17 23:48:00', date_fmt),
        'end_time': datetime.strptime('2022-01-17 23:48:00', date_fmt),
        'utc_mode': 1,
        'show_acc': 1,
        'show_eda': 1,
        'show_movement': 1,
        'show_step': 1,
        'show_wrist': 1
    }
    app = DisplayApp(options)
    print('\napp.data.info():')
    print(app.data.info())
    print('\napp.data.iloc[0]:')
    print(app.data.iloc[0])
    app.mainloop()

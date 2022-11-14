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
from importapp import ImportApp

DEFAULT_DATA_PATH = 'Dataset'


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


class DisplayApp(tk.Tk):
    def __init__(self, data_path=DEFAULT_DATA_PATH):
        super().__init__()
        # Use provided data_path and data options to load data
        self.data_path = data_path
        self.subject_ids = sorted(list(get_subject_ids(data_path)))
        self.data = None
        self.plots = [] # used to easily reference displayed plots
        self.title('Data Analyzer')
        self.geometry('900x600+50+50')
        self.resizable(True, True)
        self.configure(background='#e8f4f8')

        menubar = Menu(self)
        data_menu = DataMenu(
            menubar,
            on_import=self.open_import_app,
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

        # Todo: range selector
        range_frame = ttk.Frame(self)
        range_frame.pack(fill=BOTH, side=TOP)
        btn = ttk.Button(range_frame, text='Placeholder')
        btn.pack()

        self.frame = ScrollableLabelFrame(self, text='2020-01-01 to 2021-01-01')
        self.frame.pack(fill=BOTH, expand=True, side=BOTTOM)

    def open_import_app(self):
        print('DisplayApp.open_import_app()')
        top = ImportApp(self.subject_ids, on_submit=self.on_import_submit)
        top.lift()
        top.mainloop()

    def on_import_submit(self, options):
        print('DisplayApp.on_import_submit()')
        self.data = load_data(self.data_path, **options)
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
        figure_cols = set(self.data.columns)
        ignore_cols = {'Datetime', 'Timezone (minutes)',
                'Unix Timestamp (UTC)', 'subject_id'}
        figure_cols = figure_cols - ignore_cols

        subject_id = self.data['subject_id'].unique()[0]
        subject = self.data[self.data['subject_id'] == subject_id]

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

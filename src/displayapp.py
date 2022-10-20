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

from data import load_data

DEFAULT_DATA_PATH = 'Dataset'


class ScrollableLabelFrame(ttk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class DisplayApp(tk.Tk):

    def __init__(self, options, data_path=DEFAULT_DATA_PATH):
        super().__init__()
        # Use provided data_path and data options to load data
        self.data = load_data(data_path, **options)
        self.title('Data Analyzer')
        self.geometry('900x600+50+50')
        self.resizable(True, True)
        self.configure(background='#e8f4f8')

        menubar = Menu(self)
        self.config(menu=menubar)
        data_menu = Menu(menubar)
        data_menu.add_command(
            label='Placeholder',
            command=lambda : print('data menu'))
        time_series_menu = Menu(menubar)
        time_series_menu.add_command(
            label='Placeholder',
            command=lambda : print('time series menu')
        )
        analysis_menu = Menu(menubar)
        analysis_menu.add_command(
            label='Placeholder',
            command=lambda : print('analysis menu')
        )
        menubar.add_cascade(label="Data", menu=data_menu)
        menubar.add_cascade(label='Time Series', menu=time_series_menu)
        menubar.add_cascade(label='Analysis', menu=analysis_menu)

        # Todo: range selector
        range_frame = ttk.Frame(self)
        range_frame.pack(fill=BOTH, side=TOP)
        btn = ttk.Button(range_frame, text='Placeholder')
        btn.pack()

        frame = ScrollableLabelFrame(self, text='2020-01-01 to 2021-01-01')
        frame.pack(fill=BOTH, expand=True, side=BOTTOM)

        # Get column names to show
        figure_cols = set(self.data.columns)
        ignore_cols = {'Datetime (UTC)', 'Timezone (minutes)',
                'Unix Timestamp (UTC)', 'subject_id'}
        figure_cols = figure_cols - ignore_cols

        # Only displaying figures for first subject for now
        subject_id = self.data['subject_id'].unique()[0]
        subject = self.data[self.data['subject_id'] == subject_id]

        fig_size = (9, 4)
        fig_dpi = 100
        for col_name in sorted(figure_cols):
            fig = Figure(figsize=fig_size, dpi=fig_dpi)
            ax = fig.add_subplot(111)
            subject.plot(x='Datetime (UTC)', y=col_name, ax=ax)
            data_plot = FigureCanvasTkAgg(fig, master=frame.scrollable_frame)
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

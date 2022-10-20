import tkinter as tk
from tkinter import ttk, Menu
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from datetime import datetime

from data import load_data

DEFAULT_DATA_PATH = 'Dataset'


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

        # placeholder graph
        lf = ttk.Labelframe(self, text='2020-01-22 to 2020-02-22')
        lf.grid(row=1, column=0, sticky='nwes', padx=5, pady=5)
        f = Figure(figsize=(5,4), dpi=100)
        a = f.add_subplot(111)
        t = np.arange(0.0, 2.0, 0.01)
        s = np.sin(2*np.pi*t)
        a.plot(t, s)
        data_plot = FigureCanvasTkAgg(f, master=lf)
        #data_plot.show()
        data_plot.draw()
        data_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)




if __name__ == '__main__':
    date_fmt = '%Y-%m-%d %H:%M:%S'
    options = {
        'users': [310, 311],
        'start_time': datetime.strptime('2020-01-17 23:48:00', date_fmt),
        'end_time': datetime.strptime('2022-01-17 23:48:00', date_fmt),
        'utc_mode': 0,
        'show_acc': 0,
        'show_eda': 0,
        'show_movement': 0,
        'show_step': 0,
        'show_wrist': 0
    }
    app = DisplayApp(options)
    print('\napp.data.info():')
    print(app.data.info())
    print('\napp.data.iloc[0]:')
    print(app.data.iloc[0])
    app.mainloop()

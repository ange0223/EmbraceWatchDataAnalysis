import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *
from tkinter import messagebox
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import pandasql as ps

from data import load_data, get_subject_ids
from exportwindow import open_save_dialog
from importwindow import ImportWindow
from describewindow import DescribeWindow
from querywindow import QueryWindow
from common import Checkbutton, ScrollableLabelFrame
from util import str_to_datetime, save_figure


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
        self._var = tk.StringVar()
        super().__init__(parent, *args, textvariable=self._var, **kwargs)

    def get(self):
        return self._var.get()

    def set(self, val):
        self._var.set(val)


class TimeRangeSelector(ttk.Frame):
    def __init__(self, parent, *args, on_apply=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_callback = on_apply
        self.time_min_entry = TimeEntry(self)
        self.time_min_entry.set('')
        self.time_min_entry.pack(side=LEFT, padx=5, pady=5)
        self.time_max_entry = TimeEntry(self)
        self.time_max_entry.set('')
        self.time_max_entry.pack(side=LEFT, padx=5, pady=5)
        time_apply_btn = ttk.Button(
            self,
            text='Apply',
            command=self.apply
        )
        time_apply_btn.pack(side=LEFT, padx=5, pady=5)

    def apply(self):
        if not self.apply_callback:
            return
        time_min = str_to_datetime(self.time_min_entry.get())
        time_max = str_to_datetime(self.time_max_entry.get())
        self.apply_callback(time_min, time_max)

    def get(self):
        return self.time_min_entry.get(), self.time_max_entry.get()

    def get_min(self):
        return self.time_min_entry.get()

    def get_max(self):
        return self.time_max_entry.get()

    def set(self, time_min, time_max):
        self.time_min_entry.set(time_min)
        self.time_max_entry.set(time_max)

    def pack(self, fill=BOTH, side=TOP, **kwargs):
        super().pack(fill=BOTH, side=TOP, **kwargs)


class DisplayApp(tk.Tk):
    def __init__(self, data_path=DEFAULT_DATA_PATH):
        super().__init__()
        # Use provided data_path and data options to load data
        self.data_path = data_path
        self.subject_ids = sorted(list(get_subject_ids(data_path)))
        self.data = None # Fully loaded data
        self.plots = [] # used to easily reference displayed plots
        self._active_data_bak = None # used for undoing queries
        self._active_data = None # Subset of data which is plotted and described
        self.describe_window = None
        self.query_window = None
        self.interval = '1min'
        self.title('Data Analyzer')
        self.geometry('900x600+50+50')
        self.resizable(True, True)
        self.configure(background='#e8f4f8')
        self.utc_mode = False
        self.tz_offset = None

        menubar = Menu(self)
        data_menu = DataMenu(
            menubar,
            on_import=self.open_import_window,
            on_export=self.open_export_dialog,
            on_clear=self.clear_all
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
        time_frame = ttk.Frame(self)
        self.time_selector = TimeRangeSelector(
            time_frame,
            on_apply=self.on_time_apply
        )
        self.time_selector.pack(fill=Y, side=LEFT, padx=5, pady=5)
        ttk.Label(time_frame, text='UTC:').pack(expand=False, fill=Y,
                                                side=LEFT, padx=5, pady=5)
        self.utc_checkbtn = Checkbutton(time_frame, command=self.toggle_utc)
        self.utc_checkbtn.pack(side=LEFT, padx=5, pady=5)

        self.frame = ScrollableLabelFrame(self, text='')
        self.frame.pack(fill=BOTH, expand=True, side=BOTTOM)
        time_frame.pack(fill=X, side=TOP, padx=5, pady=5)

    @property
    def active_data(self):
        return self._active_data

    @active_data.setter
    def active_data(self, data):
        '''
        Need to update several different things when active data changes
        '''
        self._active_data = data
        self.clear_plots()
        self.load_plots()
        self.update_describe_window()

    @property
    def datetime_col(self):
        return 'Datetime (UTC)' if self.utc_mode else 'Datetime'

    def toggle_utc(self):
        print('DisplayApp.toggle_utc()')
        self.utc_mode = not self.utc_mode
        time_min = str_to_datetime(self.time_selector.get_min())
        time_max = str_to_datetime(self.time_selector.get_max())
        if self.utc_mode:
            time_min -= self.tz_offset
            time_max -= self.tz_offset
        else:
            time_min += self.tz_offset
            time_max += self.tz_offset
        self.time_selector.set(str(time_min), str(time_max))
        self.on_time_apply(time_min, time_max)
        self.clear_plots()
        self.load_plots()

    def on_time_apply(self, time_min, time_max):
        print('DisplayApp.on_time_apply()')
        if self.data is None:
            return
        self.active_data = self.data[
            (self.data[self.datetime_col] > time_min)
            & (self.data[self.datetime_col] < time_max)
        ]

    def update_describe_window(self):
        print('DisplayApp.update_describe_window()')
        if self.describe_window is None:
            return
        self.describe_window.update(self._active_data, self.interval)

    def open_describe_window(self, series):
        print('DisplayApp.open_describe_window()')
        if self.describe_window:
            self.describe_window.destroy()
        self.describe_window = DescribeWindow(series)
        self.describe_window.update(self._active_data, self.interval)

    def open_import_window(self):
        print('DisplayApp.open_import_window()')
        top = ImportWindow(self.subject_ids, on_submit=self.on_import_submit)
        top.lift()
        top.mainloop()

    def open_export_dialog(self):
        print('DisplayApp.open_export_window()')
        if self.active_data is None:
            messagebox.showerror('CSV Error', 'Error: No data to export')
        else:
            open_save_dialog(self.active_data)

    def on_import_submit(self, options):
        print('DisplayApp.on_import_submit()')
        self.data = load_data(self.data_path, **options)
        self.tz_offset = timedelta(
            minutes=int(self.data['Timezone (minutes)'].iloc[0]))
        self.utc_mode = options['utc_mode']
        self.utc_checkbtn.set(self.utc_mode)
        time_min = min(self.data[self.datetime_col])
        time_max = max(self.data[self.datetime_col])
        self.time_selector.set(str(time_min), str(time_max))
        self.on_time_apply(time_min, time_max) # will set active_data property
        #self.load_plots() # this call not needed, because of above line

    def clear_all(self):
        print('DisplayApp.clear_all()')
        self.clear_data()
        self.clear_plots()

    def clear_data(self):
        print('DisplayApp.clear_data()')
        self.data = None
        # Don't use active_data property, otherwise infinite recursion
        self._active_data = None
        if self.describe_window:
            self.describe_window.destroy()
            self.describe_window = None

    def clear_plots(self):
        print('DisplayApp.clear_plots()')
        for plot in self.plots:
            plot.get_tk_widget().destroy()
        self.plots = []

    def on_delete_submit(self, col_name):
        print('DisplayApp.on_delete_submit()')
        self.active_data = self.active_data.drop(col_name, axis=1)
        self.clear_plots()
        self.load_plots()

    def open_query_window(self):
        print('DisplayApp.open_query_window()')
        if self.query_window:
            self.query_window.destroy()
        self.query_window = QueryWindow(
            on_apply=self.on_query_apply,
            on_undo=self.on_query_undo
        )
        self.query_window.update_result("")

    def on_query_apply(self, query):
        print('DisplayApp.on_query_apply()')
        print(f'query: {query}')
        # create a backup of active data for undo
        self._active_data_bak = self.active_data
        # Need to reserve datetime cols
        #dt_utc = self.active_data['Datetime (UTC)']
        #dt = self.active_data['Datetime']
        def pysqldf(data, q):
            # Enforce inclusion of UTC and local datetime columns
            if 'SELECT' in q:
                if 'Datetime' not in q:
                    q = q.replace('SELECT ', 'SELECT `Datetime`, ')
                if 'Datetime (UTC)' not in q:
                    q = q.replace('SELECT ', 'SELECT `Datetime (UTC)`, ')
            print(f'Final query: {q}')
            return ps.sqldf(q, locals())
        # For locals right
        #pysqldf = lambda df, q, local=locals(): ps.sqldf(q, local)
        try:
            df = pysqldf(self.active_data, query)
        except Exception as e:
            err_msg = 'Query failed to execute:\n'
            err_msg += str(e)
            self.query_window.update_result(err_msg)
        else:
            self.active_data = df
            self.query_window.update_result('Query ran successfully')

    def on_query_undo(self):
        print('DisplayApp.on_query_undo()')
        if self._active_data_bak is not None:
            self.active_data = self._active_data_bak
            self.query_window.update_result('Changes reverted')
            self._active_data_bak = None
        else:
            self.query_window.update_result('No changes have been made')

    def load_plots(self):
        print('DisplayApp.load_plots()')
        if self.data is None:
            return
        # Get column names to show
        figure_cols = set(self.active_data.columns)
        ignore_cols = {'Datetime', 'Datetime (UTC)', 'Timezone (minutes)',
                       'Unix Timestamp (UTC)', 'subject_id'}
        figure_cols = figure_cols - ignore_cols

        subject = self.active_data
        #subject_id = self.active_data['subject_id'].unique()[0]
        #subject = self.active_data[self.active_data['subject_id'] == subject_id]

        fig_size = (9, 4)
        fig_dpi = 100
        for col_name in sorted(figure_cols):
            fig = Figure(figsize=fig_size, dpi=fig_dpi)
            ax = fig.add_subplot(111)
            subject.plot(x=self.datetime_col, y=col_name, ax=ax)
            data_plot = FigureCanvasTkAgg(fig,
                    master=self.frame.scrollable_frame)
            self.plots.append(data_plot)
            data_plot.draw()
            plot_widget = data_plot.get_tk_widget()
            context_menu = SeriesContextMenu(
                self.frame.scrollable_frame,
                on_aggregate=lambda x: print('on_aggregate({})'.format(x)),
                on_describe=lambda c=col_name: self.open_describe_window(c),
                on_query=lambda : self.open_query_window(),
                on_save_figure=lambda c=col_name, f=fig: save_figure(f, c),
                on_draw=lambda : print('on_draw()'),
                on_delete=lambda c=col_name: self.on_delete_submit(c)
            )
            plot_widget.bind('<Button-3>', context_menu.popup)
            plot_widget.pack(fill=X, expand=True)


class SeriesContextMenu(tk.Menu):
    def __init__(self, parent, on_aggregate=None, on_describe=None,
                 on_query=None, on_save_figure=None, on_draw=None,
                 on_delete=None, tearoff=0, **kwargs):
        super().__init__(parent, tearoff=tearoff, **kwargs)
        intervals = ('1ms', '5ms', '50ms', '500ms', '1S', '1min', '30min', '1H',
                     '3H', '6H', 'D', 'W')
        agg_menu = tk.Menu(self)
        for interval in intervals:
            # Must set interval=interval at lambda definition time to overcome
            # issue of value of interval being captured at runtime (all the
            # same final value 'W')
            agg_menu.add_command(
                label=interval,
                command=lambda interval=interval: on_aggregate(interval)
            )
        self.add_cascade(
            label='Aggregate',
            menu=agg_menu
        )
        self.add_command(
            label='Describe',
            command=on_describe
        )
        self.add_command(
            label='Query',
            command=on_query
        )
        self.add_separator()
        self.add_command(
            label='Save figure',
            command=on_save_figure
        )
        self.add_command(
            label='Draw',
            command=on_draw
        )
        self.add_separator()
        self.add_command(
            label='Delete',
            command=on_delete
        )

    def popup(self, event):
        try:
            self.tk_popup(event.x_root, event.y_root)
        finally:
            self.grab_release()



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

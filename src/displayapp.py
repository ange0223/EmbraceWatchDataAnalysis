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

from exportwindow import open_save_dialog
from importwindow import ImportWindow
from describewindow import DescribeWindow
from querywindow import QueryWindow
import common
from util import str_to_datetime, valid_agg_intervals, save_figure


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
    def __init__(self, parent, *args, var=None, on_apply=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_callback = on_apply
        self.var = var
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
        dt_min = str_to_datetime(self.time_min_entry.get())
        dt_max = str_to_datetime(self.time_max_entry.get())
        if self.var:
            var = (dt_min, dt_max)
        if self.apply_callback:
            self.apply_callback(dt_min, dt_max)

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


class Checkbutton(common.Checkbutton):
    def pack(self, side=LEFT, ipadx=5, ipady=5):
        super().pack(side=side, ipadx=ipadx, ipady=ipady)


class ScrollableLabelFrame(common.ScrollableLabelFrame):
    def pack(self, fill=BOTH, expand=True, side=BOTTOM):
        super().pack(expand=expand, fill=fill, side=side)


class UTCLabel(ttk.Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, text='UTC: ', **kwargs)

    def pack(self, expand=False, fill=Y, side=LEFT, ipadx=5, ipady=5):
        super().pack(expand=expand, fill=fill, side=side, ipadx=ipadx,
                     ipady=ipady)


class DisplayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Use provided data_path and data options to load data
        #self.data_path = data_path
        #self.subject_ids = sorted(list(get_subject_ids(data_path)))
        self.data = None # Fully loaded data
        self.plots = [] # used to easily reference displayed plots
        self._active_data_bak = None # used for undoing queries
        self._active_data = None # Subset of data which is plotted and described
        self.describe_window = None
        self.query_window = None
        self.title('Data Analyzer')
        self.geometry('900x600+50+50')
        self.resizable(True, True)
        self.configure(background='#e8f4f8')
        self.utc_mode = False
        self.tz_offset = None
        # These members have a direct effect on the value of active_data.
        # Every time one of their values changes self.update_active_data() will
        # be called, which will apply their values to active_data.
        self._active_datetime_range = None
        self._active_query = None
        self._active_agg_interval = None
        self._active_deleted_cols = None
        self.default_interval = '1min'

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
            var=self.active_datetime_range
            #on_apply=lambda dtr, p=self.active_datetime_range: p=dtr
        )
        self.time_selector.pack(fill=Y, side=LEFT, padx=5, pady=5)
        UTCLabel(time_frame).pack()

        self.utc_checkbtn = Checkbutton(time_frame, command=self.toggle_utc)
        self.utc_checkbtn.pack()

        self.frame = ScrollableLabelFrame(self, text='')
        self.frame.pack()
        time_frame.pack(fill=X, side=TOP, padx=5, pady=5)

    @property
    def active_data(self):
        return self._active_data

    @property
    def active_query(self):
        return self._active_query

    @active_query.setter
    def active_query(self, query):
        old_active_query = self._active_query
        self._active_query = query
        # New query resets deleted columns
        self._active_deleted_cols = None
        # New query resets datetime range
        # Setting active_datetime_range to None does not trigger a call to
        #  update_active_data
        self.active_datetime_range = None
        self.update_active_data()
        if self.query_window:
            # If query existed and was just set to None (undo)
            if old_active_query and query is None:
                self.query_window.update_result('Changes reverted')
            # If query did not exist before and was set to None (undo nothing)
            if not old_active_query and not query:
                self.query_window.update_result('Nothing to undo')

    @property
    def active_datetime_range(self):
        return self._active_datetime_range

    @active_datetime_range.setter
    def active_datetime_range(self, dt_range):
        if dt_range is None:
            self._active_datetime_range = None
            return
        dt_min, dt_max = dt_range
        if dt_max < dt_min:
            print('DisplayApp.active_datetime_range.setter(): ', end='')
            print('  ERROR: min datetime must be less than max datetime')
            return
        self._active_datetime_range = dt_range
        self.update_active_data()

    @property
    def active_deleted_cols(self):
        return self._active_deleted_cols

    @active_deleted_cols.setter
    def active_deleted_cols(self, cols):
        self._active_deleted_cols = cols
        self.update_active_data()

    @property
    def active_agg_interval(self):
        return self._active_agg_interval

    @active_agg_interval.setter
    def active_agg_interval(self, interval):
        if interval not in valid_agg_intervals():
            print('DisplayApp.active_agg_interval.setter(): ', end='')
            print(f'  ERROR: invalid agg interval provided: "{interval}"')
            return
        # Set to None so resampling isn't performed at all
        if interval == self.default_interval:
            self._active_agg_interval = None
        self._active_agg_interval = interval
        self.update_active_data()

    def _query_data(self, df=None):
        if df is None:
            df = self.data
        query = self.active_query
        # Enforce inclusion of UTC and local datetime columns
        if 'SELECT' in query:
            if 'Datetime' not in query:
                query = query.replace('SELECT ', 'SELECT `Datetime`, ')
            if 'Datetime (UTC)' not in query:
                query = query.replace('SELECT ',
                                      'SELECT `Datetime (UTC)`, ')
        try:
            def pysqldf(data, q):
                return ps.sqldf(q, locals())

            df_queried = pysqldf(df, query)
        except Exception as e:
            result = f'Query failed to execute:\n{str(e)}'
        else:
            df = df_queried
            result = 'Query ran successfully'
        finally:
            # Update query window if present
            # NOTE - should set to None if window closed (?)
            if self.query_window:
                self.query_window.update_result(result)
                # Lift query window to front
                self.query_window.wm_transient(self)
        return df

    def update_active_data(self):
        print('DisplayApp.update_active_data()')
        if self.data is None:
            self._active_data = None
            return
        df = self.data.copy()
        # Set index as current datetime column (tz local or UTC)
        df.index = df[self.datetime_col]
        # Remove unecessary datetime columns
        df = df.drop(['Datetime', 'Datetime (UTC)'], axis=1)
        print('DisplayApp.update_active_data(): initial value of df:')
        print(df.head())
        # Apply active query if defined
        if self.active_query:
            df = self._query_data(df)
        # Apply active_datetime_range if defined
        if self.active_datetime_range:
            dt_min, dt_max = self.active_datetime_range
            dt_col = self.datetime_col
            #df = df[(df[dt_col] > dt_min) & (df[dt_col] < dt_max)]
            df = df[((df.index >= dt_min) & (df.index <= dt_max))]
        # Otherwise, use derived range of df
        else:
            #dt_min = min(df[self.datetime_col])
            #dt_max = max(df[self.datetime_col])
            dt_min = min(df.index)
            dt_max = max(df.index)
            # Directly accessing _active_datetime_range here to avoid triggering
            #  an additional call to update_active_data
            self._active_datetime_range = (dt_min, dt_max)
        # Update GUI to show current datetime range
        self.time_selector.set(str(dt_min), str(dt_max))
        # Apply (remove) any actively deleted columns if defined
        if self.active_deleted_cols:
            for col_name in self.active_deleted_cols:
                if col_name not in df.columns:
                    continue
                df = df.drop(col_name, axis=1)
        # Apply active aggregation interval if defined
        if self.active_agg_interval:
            valid_intervals = valid_agg_intervals()
            default_index = valid_intervals.index(self.default_interval)
            active_index = valid_intervals.index(self.active_agg_interval)
            if active_index < default_index: # upsampling
                # This can potentially result in an array that is too large to
                #  allocate sufficient space for
                try:
                    df_agg = df.resample(self.active_agg_interval).ffill()
                except Exception as err:
                    print('Could not allocate enough memory for upsampling')
                    print('TODO: Popup to user about memory error')
                    self._active_agg_interval = self.default_interval
                else:
                    df = df_agg
            elif active_index > default_index: # downsampling
                df = df.resample(self.active_agg_interval).mean()
            print('DisplayApp.update_active_data(): resampled df:')
            print(df.head())
            # otherwise: matching - no need to resample
        # Finally, update active data and refresh everything
        self._active_data = df
        self.clear_plots()
        self.load_plots()
        self.update_describe_window()

    @property
    def datetime_col(self):
        return 'Datetime (UTC)' if self.utc_mode else 'Datetime'

    def toggle_utc(self):
        print('DisplayApp.toggle_utc()')
        self.utc_mode = not self.utc_mode
        # NOTE - should just use active_datetime_range
        dt_min = str_to_datetime(self.time_selector.get_min())
        dt_max = str_to_datetime(self.time_selector.get_max())
        if self.utc_mode:
            dt_min -= self.tz_offset
            dt_max -= self.tz_offset
        else:
            dt_min += self.tz_offset
            dt_max += self.tz_offset
        # This will trigger an update to active_data
        self.active_datetime_range = (dt_min, dt_max)

    def open_import_window(self):
        print('DisplayApp.open_import_window()')
        top = ImportWindow(on_submit=self.on_import_submit)
        top.lift()
        top.mainloop()

    def on_import_submit(self, data, options):
        print('DisplayApp.on_import_submit()')
        #self.data = load_data(self.data_path, **options)
        self.data = data
        self.tz_offset = timedelta(
            minutes=int(self.data['Timezone (minutes)'].iloc[0]))
        self.utc_mode = options['utc_mode']
        self.utc_checkbtn.set(self.utc_mode)
        # This will NOT trigger a call to update_active_data()
        self.active_datetime_range = None
        # active_datetime_range will be full range of active data after this
        self.update_active_data()

    def open_export_dialog(self):
        print('DisplayApp.open_export_window()')
        if self.active_data is None:
            messagebox.showerror('CSV Error', 'Error: No data to export')
        else:
            open_save_dialog(self.active_data)

    def clear_all(self):
        print('DisplayApp.clear_all()')
        self.clear_data()
        self.clear_plots()

    def clear_data(self):
        print('DisplayApp.clear_data()')
        self.data = None
        # Don't use active_data property, otherwise infinite recursion
        if self.describe_window:
            self.describe_window.destroy()
            self.describe_window = None
        self.update_active_data()

    def clear_plots(self):
        print('DisplayApp.clear_plots()')
        for plot in self.plots:
            plot.get_tk_widget().destroy()
        self.plots = []

    def load_plots(self):
        print('DisplayApp.load_plots()')
        if self.active_data is None:
            return
        # Get column names to show
        figure_cols = set(self.active_data.columns)
        ignore_cols = {'Datetime', 'Datetime (UTC)', 'Timezone (minutes)',
                       'Unix Timestamp (UTC)', 'subject_id'}
        figure_cols = figure_cols - ignore_cols
        fig_size = (9, 4)
        fig_dpi = 100
        for col_name in sorted(figure_cols):
            fig = Figure(figsize=fig_size, dpi=fig_dpi)
            ax = fig.add_subplot(111)
            # Using index as x-axis
            self.active_data.plot(y=col_name, ax=ax)
            data_plot = FigureCanvasTkAgg(fig,
                    master=self.frame.scrollable_frame)
            self.plots.append(data_plot)
            data_plot.draw()
            plot_widget = data_plot.get_tk_widget()
            context_menu = SeriesContextMenu(
                self.frame.scrollable_frame,
                on_aggregate=self.aggregate,
                on_describe=lambda c=col_name: self.open_describe_window(c),
                on_query=lambda : self.open_query_window(),
                on_save_figure=lambda c=col_name, f=fig: save_figure(f, c),
                on_draw=lambda : print('on_draw()'),
                on_delete=lambda c=col_name: self.delete_series(c)
            )
            plot_widget.bind('<Button-3>', context_menu.popup)
            plot_widget.pack(fill=X, expand=True)

    def open_describe_window(self, series):
        print('DisplayApp.open_describe_window()')
        if self.describe_window:
            self.describe_window.destroy()
        self.describe_window = DescribeWindow(series)
        self.update_describe_window()

    def update_describe_window(self):
        print('DisplayApp.update_describe_window()')
        if self.describe_window is None:
            return
        # Check if series used by describe window has been removed (e.g. query)
        if self.describe_window.series not in self.active_data.columns:
            # Kill describe window if no longer has attachment to this data
            # self.describe_window.destroy()
            # Choosing to instead just leave it open in case user wants to
            # briefly check query result that excludes describe window series
            # before then undoing the query and getting the series back
            return
        self.describe_window.update_info(self.active_data,
                                         self.active_agg_interval)

    def delete_series(self, col_name):
        print(f'DisplayApp.delete_series(): {col_name}')
        if self.active_deleted_cols:
            del_cols = {col_name} | self.active_deleted_cols
            self.active_deleted_cols = del_cols
        else:
            self.active_deleted_cols = {col_name}

    def open_query_window(self):
        print('DisplayApp.open_query_window()')
        if self.query_window:
            self.query_window.destroy()
        self.query_window = QueryWindow(
            on_apply=self.apply_query,
            on_undo=self.undo_query
        )
        self.query_window.update_result("")

    def apply_query(self, query):
        print(f'DisplayApp.apply_query():', query.replace("\n", " "))
        # This will trigger a call to update_active_data()
        self.active_query = query

    def undo_query(self):
        print('DisplayApp.undo_query()')
        # This will trigger a call to update_active_data()
        self.active_query = None

    def aggregate(self, interval):
        print(f'DisplayApp.aggregate(): {interval}')
        # This will trigger a call to update_active_data()
        self.active_agg_interval = interval


class SeriesContextMenu(tk.Menu):
    def __init__(self, parent, on_aggregate=None, on_describe=None,
                 on_query=None, on_save_figure=None, on_draw=None,
                 on_delete=None, tearoff=0, **kwargs):
        super().__init__(parent, tearoff=tearoff, **kwargs)
        intervals = valid_agg_intervals()
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
    from data import load_data
    import os
    data_path = os.path.join(os.getcwd(), 'Dataset')
    date_fmt = '%Y-%m-%d %H:%M:%S'
    options = {
        'users': 310,
        'start_time': datetime.strptime('2020-01-17 23:48:00', date_fmt),
        'end_time': datetime.strptime('2022-01-17 23:48:00', date_fmt),
        'utc_mode': False,
        'show_acc': True,
        'show_eda': True,
        'show_temp': True,
        'show_movement': True,
        'show_step': True,
        'show_rest': True,
        'show_wrist': True
    }
    data = load_data(data_path, **options)
    app = DisplayApp()
    # Manually call import submit callback to pass data
    app.on_import_submit(data, options)
    app.mainloop()

import pandas as pd
import random
from datetime import datetime
import tkinter as tk
from tkinter.constants import *
from tkinter import ttk, Menu
import os

from . import common
from .data import get_subject_ids, load_data
from .util import str_to_datetime


class Label(ttk.Label):
    def __init__(self, parent, font_family='Helvetica', font_size=14,
                background='#e8f4f8', **kwargs):
        super().__init__(parent, background='#e8f4f8',
                         font=(font_family, font_size), **kwargs)

    def grid(self, column=0, row=0, sticky=tk.W, padx=5, pady=5, **kwargs):
        super().grid(column=column, row=row, sticky=sticky, padx=padx,
                     pady=pady, **kwargs)


class Header(Label):
    def __init__(self, parent, font_size=24, **kwargs):
        super().__init__(parent, font_size=font_size, **kwargs)


class Entry(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def grid(self, column=1, row=0, sticky=tk.W, padx=5, pady=5, **kwargs):
        super().grid(column=column, row=row, sticky=sticky, padx=padx,
                     pady=pady, **kwargs)


class DataPathEntry(Entry):
    def __init__(self, parent, on_change=None, **kwargs):
        self.tk_var = tk.StringVar()
        super().__init__(parent, textvariable=self.tk_var, **kwargs)
        if on_change is None:
            def placeholder_callback(var, index, mode):
                print('DataPathEntry.tk_var.trace callback: ', end='')
                print(f'tk_var value="{self.tk_var.get()}"')
            on_change = placeholder_callback
        self.tk_var.trace_add('write', on_change)

    def get(self):
        return self.tk_var.get()

    def set(self, value):
        self.tk_var.set(value)


class Checkbutton(common.Checkbutton):
    def grid(self, column=1, row=0, sticky=tk.W, padx=5, pady=5, **kwargs):
        super().grid(column=column, row=row, sticky=sticky, padx=padx,
                     pady=pady, **kwargs)


class DropDown(ttk.OptionMenu):
    def __init__(self, parent, tkvar, default, *options, row=None):
        super().__init__(parent, tkvar, default, *options)
        self._var = tkvar
        self.row = row

    def get(self):
        return self._var.get()

    def grid(self, column=1, row=0, sticky=tk.W, padx=5, pady=5, **kwargs):
        super().grid(column=column, row=row, sticky=sticky, padx=padx,
                     pady=pady, **kwargs)


class NullDropDown(DropDown):
    def __init__(self, parent, row=None):
        options = [-1]
        super().__init__(parent, tk.IntVar(), options[0], *options, row=row)


class InvalidDataPathLabel(Label):
    def __init__(self, parent, text='Please enter a valid data path', row=None):
        super().__init__(parent, text=text)
        self.row = row


class SubmitButton(ttk.Button):
    def __init__(self, parent, text='Submit', **kwargs):
        super().__init__(parent, text=text, **kwargs)

    def grid(self, column=1, row=0, sticky=tk.E, padx=5, pady=5, **kwargs):
        super().grid(column=column, row=row, stick=sticky, padx=padx,
                     pady=pady, **kwargs)


# GUI for Our project
class ImportWindow(tk.Toplevel):
    def __init__(self, on_submit=None):
        super().__init__()
        self.resizable(False, False)
        self.configure(background='#e8f4f8')
        self.submit_callback = on_submit
        self.title('EmbraceWatch Data Analysis')
        self.geometry('500x600+100+100')

        # create a menubar
        menubar = Menu(self)
        self.config(menu=menubar)

        # create a menu
        file_menu = Menu(menubar)

        # add the File menu to the menubar
        menubar.add_cascade(label='File', menu=file_menu)

        # add a menu item to the menu
        file_menu.add_command(label='Exit', command=self.destroy)

        # use for convenience of changing options such that widget order is
        # changed or a new widget is inserted before any other
        curr_row = 0

        options_label = Header(self, text='Options')
        options_label.grid(row=curr_row)
        curr_row += 1

        # NOTE: replace this with usage of tk.tkFileDialog.askdirectory()
        path_label = Label(self, text='Data path:')
        path_label.grid(row=curr_row)
        self.path_entry = DataPathEntry(self, on_change=self.on_path_changed)
        # Default path set below definition of self.user_drop, because it
        # the path on_change callback requires it to exist, and calling
        # self.path_entry.set() when setting the default path will trigger that
        # callback.
        self.path_entry.grid(row=curr_row)
        curr_row += 1

        users_label = Label(self, text='EmbraceWatch User ID(s):')
        users_label.grid(row=curr_row)
        # Initially no subject_ids available
        self.user_drop = InvalidDataPathLabel(self, row=curr_row)
        self.user_drop.grid(column=1, row=curr_row)
        #self.user_drop = NullDropDown(self, row=curr_row)
        #self.user_drop.grid(row=curr_row)
        curr_row += 1

        start_label = Label(self, text='Date Start:')
        start_label.grid(row=curr_row)
        self.start_entry = Entry(self)
        self.start_entry.insert(0, '2020-01-17 23:48:00')
        self.start_entry.grid(row=curr_row)
        curr_row += 1

        end_label = Label(self, text='Date End:')
        end_label.grid(row=curr_row)
        self.end_entry = Entry(self)
        self.end_entry.insert(0, '2022-01-17 23:48:00')
        self.end_entry.grid(row=curr_row)
        curr_row += 1

        utc_label = Label(self, text='UTC:')
        utc_label.grid(row=curr_row)
        self.utc_checkbtn = Checkbutton(self)
        self.utc_checkbtn.grid(row=curr_row)
        curr_row += 1

        display_label = Header(self, text='Fields to Display')
        display_label.grid(row=curr_row)
        curr_row += 1

        acc_label = Label(self, text='ACC Avg Magnitude:')
        acc_label.grid(row=curr_row)
        self.acc_checkbtn = Checkbutton(self)
        self.acc_checkbtn.grid(row=curr_row)
        curr_row += 1

        eda_label = Label(self, text='EDA Avg:')
        eda_label.grid(row=curr_row)
        self.eda_checkbtn = Checkbutton(self)
        self.eda_checkbtn.grid(row=curr_row)
        curr_row += 1

        temp_label = Label(self, text='Temperature Avg:')
        temp_label.grid(row=curr_row)
        self.temp_checkbtn = Checkbutton(self)
        self.temp_checkbtn.grid(row=curr_row)
        curr_row += 1

        movement_label = Label(self, text='Movement Intensity:')
        movement_label.grid(row=curr_row)
        self.movement_checkbtn = Checkbutton(self)
        self.movement_checkbtn.grid(row=curr_row)
        curr_row += 1

        step_label = Label(self, text='Steps:')
        step_label.grid(row=curr_row)
        self.step_checkbtn = Checkbutton(self)
        self.step_checkbtn.grid(row=curr_row)
        curr_row += 1

        rest_label = Label(self, text='Rest:')
        rest_label.grid(row=curr_row)
        self.rest_checkbtn = Checkbutton(self)
        self.rest_checkbtn.grid(row=curr_row)
        curr_row += 1

        wrist_label = Label(self, text='On Wrist:')
        wrist_label.grid(row=curr_row)
        self.wrist_checkbtn = Checkbutton(self)
        self.wrist_checkbtn.grid(row=curr_row)
        curr_row += 1

        toggle_all_label = Label(self, text='Toggle All:')
        toggle_all_label.grid(row=curr_row)
        self.toggle_all_checkbtn = Checkbutton(
            self,
            command=self.toggle_all_display_fields)
        self.toggle_all_checkbtn.grid(row=curr_row)
        curr_row += 1

        self.submit_btn = SubmitButton(self, command=self.submit)
        self.submit_btn['state'] = DISABLED
        self.submit_btn.grid(row=curr_row)
        curr_row += 1

        # Set path_entry text to default path ('./Dataset')
        # This will trigger the callback self.on_path_changed(),
        #  which will update subject ID options (self.user_drop).
        # This will also affect the self.submit_btn state.
        # Because of these reasons, this needs to come after those objects
        #  are defined.
        default_path = os.path.join(os.getcwd(), 'Dataset')
        self.path_entry.set(default_path)

    def on_path_changed(self, *args):
        path = self.path_entry.get()
        # Get grid row of old user_drop
        row = self.user_drop.row
        # Destory old user_drop
        self.user_drop.destroy()
        try:
            if not os.path.exists(path):
                raise Exception('Path does not exist')
            if not os.path.isdir(path):
                raise Exception('Path is not a dir')
            try:
                subject_ids = sorted(list(get_subject_ids(path)))
            except ValueError as err:
                print('Data path exception occurred: ', end='')
                print(err)
                raise Exception('Path has no data')
        # Path might not exist at all
        # Path might exist, but not be a directory
        # Path might be a directory, but not have structured data
        except Exception as err:
            print('Data path exception occurred: ', end='')
            print(err)
            print('TODO: show user popup telling them it\'s invalid')
            #self.user_drop = NullDropDown(self, row=row)
            #self.user_drop.grid(row=row)
            self.user_drop = InvalidDataPathLabel(self, text=str(err), row=row)
            self.user_drop.grid(column=1, row=row)
            # Disable submit button
            self.submit_btn['state'] = DISABLED
            return
        print(f'subject_ids: {subject_ids}')
        # Create new user_drop
        self.user_drop = DropDown(self, tk.IntVar(),
                                  subject_ids[0], *subject_ids, row=row)
        self.user_drop.grid(row=row)
        # Enable submit button
        self.submit_btn['state'] = NORMAL

    def get_options(self):
        user_input = {
            #'users': map(int, self.users_entry.get().split(',')),
            'users': self.user_drop.get(),
            'start_time': str_to_datetime(self.start_entry.get()),
            'end_time': str_to_datetime(self.end_entry.get()),
            'utc_mode': self.utc_checkbtn.get(),
            'show_acc': self.acc_checkbtn.get(),
            'show_eda': self.eda_checkbtn.get(),
            'show_temp': self.temp_checkbtn.get(),
            'show_movement': self.movement_checkbtn.get(),
            'show_step': self.step_checkbtn.get(),
            'show_rest': self.rest_checkbtn.get(),
            'show_wrist': self.wrist_checkbtn.get()
        }
        return user_input

    def submit(self):
        self.submit_btn['state'] = DISABLED
        options = self.get_options()
        data_path = self.path_entry.get()
        data = load_data(data_path, **options)
        if self.submit_callback:
            self.submit_callback(data, options)
        self.destroy()

    def toggle_all_display_fields(self):
        toggle_state = self.toggle_all_checkbtn.get()
        self.acc_checkbtn.set(toggle_state)
        self.acc_checkbtn.set(toggle_state)
        self.eda_checkbtn.set(toggle_state)
        self.temp_checkbtn.set(toggle_state)
        self.movement_checkbtn.set(toggle_state)
        self.step_checkbtn.set(toggle_state)
        self.rest_checkbtn.set(toggle_state)
        self.wrist_checkbtn.set(toggle_state)


if __name__ == '__main__':
    import tkinter as tk

    class App(tk.Tk):
        def __init__(self, subject_ids, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.subject_ids = subject_ids
            tk.Button(self, text='Import', command=self.open_import).pack()

        def open_import(self):
            subject_ids = [310, 311, 312]
            iw = ImportWindow(subject_ids, on_submit=self.iw_callback)
            iw.lift()
            iw.mainloop()

        def iw_callback(self, import_options):
            # Do something, anything, with import options -- printing them
            self.print_import_options(import_options)

        @staticmethod
        def print_import_options(import_options):
            print('Received import options via callback from ImportWindow:')
            # Formatting key length as max key length plus 1 (for ':')
            key_len = max((len(key) for key in import_options)) + 1
            for key, val in import_options.items():
                print('  {: <{fill}} {:}'.format(key+':', val, fill=key_len))

    subject_ids = [310, 311, 312]
    app = App(subject_ids)
    app.mainloop()


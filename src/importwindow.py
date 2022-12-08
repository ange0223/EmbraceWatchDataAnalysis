import pandas as pd
import random
from datetime import datetime
import tkinter as tk
from tkinter import ttk, Menu

from common import Checkbutton
from util import str_to_datetime


class CommonLabel(ttk.Label):
    def __init__(self, parent, font_family='Helvetica', font_size=14,
                background='#e8f4f8', **kwargs):
        super().__init__(parent, background='#e8f4f8',
                         font=(font_family, font_size), **kwargs)

    def grid(self, column=0, row=0, sticky=tk.W, padx=5, pady=5, **kwargs):
        super().grid(column=column, row=row, sticky=sticky, padx=padx,
                     pady=pady, **kwargs)


class CommonHeader(CommonLabel):
    def __init__(self, parent, font_size=24, **kwargs):
        super().__init__(parent, font_size=font_size, **kwargs)


class CommonEntry(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def grid(self, column=1, row=0, sticky=tk.W, padx=5, pady=5, **kwargs):
        super().grid(column=column, row=row, sticky=sticky, padx=padx,
                     pady=pady, **kwargs)


class CommonCheckbutton(Checkbutton):
    def grid(self, column=1, row=0, sticky=tk.W, padx=5, pady=5, **kwargs):
        super().grid(column=column, row=row, sticky=sticky, padx=padx,
                     pady=pady, **kwargs)


class CommonDropDown(ttk.OptionMenu):
    def __init__(self, parent, tkvar, default, *options):
        super().__init__(parent, tkvar, default, *options)
        self._var = tkvar

    def get(self):
        return self._var.get()

    def grid(self, column=1, row=0, sticky=tk.W, padx=5, pady=5, **kwargs):
        super().grid(column=column, row=row, sticky=sticky, padx=padx,
                     pady=pady, **kwargs)


class CommonSubmitButton(ttk.Button):
    def __init__(self, parent, text='Submit', **kwargs):
        super().__init__(parent, text=text, **kwargs)

    def grid(self, column=1, row=0, sticky=tk.E, padx=5, pady=5, **kwargs):
        super().grid(column=column, row=row, stick=sticky, padx=padx,
                     pady=pady, **kwargs)


# GUI for Our project
class ImportWindow(tk.Toplevel):
    def __init__(self, subject_ids, on_submit=None):
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
        menubar.add_cascade(
            label='File',
            menu=file_menu
        )

        # add a menu item to the menu
        file_menu.add_command(
            label='Exit',
            command=self.destroy
        )

        options_label = CommonHeader(self, text='Options')
        options_label.grid(row=0)

        users_label = CommonLabel(self, text='EmbraceWatch User ID(s):')
        users_label.grid(row=1)
        self.user_drop = CommonDropDown(self, tk.IntVar(), subject_ids[0], *subject_ids)
        self.user_drop.grid(row=1)

        start_label = CommonLabel(self, text='Date Start:')
        start_label.grid(row=2)
        self.start_entry = CommonEntry(self)
        self.start_entry.insert(0, '2020-01-17 23:48:00')
        self.start_entry.grid(row=2)

        end_label = CommonLabel(self, text='Date End:')
        end_label.grid(row=3)
        self.end_entry = CommonEntry(self)
        self.end_entry.insert(0, '2022-01-17 23:48:00')
        self.end_entry.grid(row=3)

        utc_label = CommonLabel(self, text='UTC:')
        utc_label.grid(row=4)
        self.utc_checkbtn = CommonCheckbutton(self)
        self.utc_checkbtn.grid(row=4)

        display_label = CommonHeader(self, text='Fields to Display')
        display_label.grid(row=5)

        acc_label = CommonLabel(self, text='ACC Avg Magnitude:')
        acc_label.grid(row=6)
        self.acc_checkbtn = CommonCheckbutton(self)
        self.acc_checkbtn.grid(row=6)

        eda_label = CommonLabel(self, text='EDA Avg:')
        eda_label.grid(row=7)
        self.eda_checkbtn = CommonCheckbutton(self)
        self.eda_checkbtn.grid(row=7)

        temp_label = CommonLabel(self, text='Temperature Avg:')
        temp_label.grid(row=8)
        self.temp_checkbtn = CommonCheckbutton(self)
        self.temp_checkbtn.grid(row=8)

        movement_label = CommonLabel(self, text='Movement Intensity:')
        movement_label.grid(row=9)
        self.movement_checkbtn = CommonCheckbutton(self)
        self.movement_checkbtn.grid(row=9)

        step_label = CommonLabel(self, text='Steps:')
        step_label.grid(row=10)
        self.step_checkbtn = CommonCheckbutton(self)
        self.step_checkbtn.grid(row=10)

        rest_label = CommonLabel(self, text='Rest:')
        rest_label.grid(row=11)
        self.rest_checkbtn = CommonCheckbutton(self)
        self.rest_checkbtn.grid(row=11)

        wrist_label = CommonLabel(self, text='On Wrist:')
        wrist_label.grid(row=12)
        self.wrist_checkbtn = CommonCheckbutton(self)
        self.wrist_checkbtn.grid(row=12)

        toggle_all_label = CommonLabel(self, text='Toggle All:')
        toggle_all_label.grid(row=13)
        self.toggle_all_checkbtn = CommonCheckbutton(self,
                command=self.toggle_all_display_fields)
        self.toggle_all_checkbtn.grid(row=13)

        submit_btn = CommonSubmitButton(self, command=self.submit)
        submit_btn.grid(row=14)

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
        options = self.get_options()
        if self.submit_callback:
            self.submit_callback(options)
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


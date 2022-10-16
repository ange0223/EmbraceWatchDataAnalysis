import pandas as pd
import random
from datetime import datetime
#from pytz import timezone
import tkinter as tk
from tkinter import ttk, Menu

from displayapp import DisplayApp

DATE_FMT = "%Y-%m-%d %H:%M:%S"

# Classes from SRS document

class Person:
    def _init_(self, id, default_time_zone):
        self.id = random.random()

class WatchData:
    def _init_(self, id, person_id, date_time_utc, current_time_zone,
                avg_magnitude, avg_eda, avg_temp, movement_intensity,
                steps, rest, on_wrist):
        self.id = random.random()
        self.person_id = person_id
        self.date_time_utc = date_time_utc
        self.current_time_zone = current_time_zone
        self.avg_magnitude = avg_magnitude
        self.avg_eda = avg_eda
        self.avg_temp = avg_temp
        self.movement_intensity = movement_intensity
        self.steps = steps
        self.rest = rest
        self.on_wrist = on_wrist

    # def GetBtwn(date_time_start, date_time_end):
        # Returns data between two DateTimes. If no arguments given, returns the entire dataset.

    # def GetPersonData(person_id):
        # Returns data from a specific Person

    # def GetPeopleData(id_arr):
        # Returns data from several people

    # def UpdateDisplayTimeZone(self, timezone):
        # Updates Display Timezone field with the currently selected timezone.

    # def GraphData():
        # Graphs the data to a line graph.

    # def Analyze():
        # Readies the user selected data for viewing in the Analysis window

class User:
    def _init_(self):
        self.id = random.random()
        # self.local_time_zone =

    # def GetLocalTimeZone():
        # Gets the local time zone for the current user based on the system the software is currently running on.

class MenuLabel(ttk.Label):
    def __init__(self, parent, font_family='Helvetica', font_size=14,
                background='#e8f4f8', **kwargs):
        super().__init__(parent, background='#e8f4f8',
                         font=(font_family, font_size), **kwargs)

    def grid(self, column=0, row=0, sticky=tk.W, padx=5, pady=5,
             **kwargs):
        super().grid(column=column, row=row, sticky=sticky, padx=padx,
                     pady=pady, **kwargs)


class MenuHeader(MenuLabel):
    def __init__(self, parent, font_size=24, **kwargs):
        super().__init__(parent, font_size=font_size, **kwargs)


class MenuEntry(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def grid(self, column=1, row=0, sticky=tk.W, padx=5, pady=5,
             **kwargs):
        super().grid(column=column, row=row, sticky=sticky, padx=padx,
                     pady=pady, **kwargs)


class MenuCheckbutton(ttk.Checkbutton):
    def __init__(self, parent, **kwargs):
        self._var = tk.IntVar()
        super().__init__(parent, variable=self._var,
                       **kwargs)

    def get(self):
        return self._var.get()

    def grid(self, column=1, row=0, sticky=tk.W, padx=5, pady=5,
             **kwargs):
        super().grid(column=column, row=row, sticky=sticky, padx=padx,
                     pady=pady, **kwargs)


class MenuSubmitButton(ttk.Button):
    def __init__(self, parent, text='Submit', **kwargs):
        super().__init__(parent, text=text, **kwargs)

    def grid(self, column=1, row=0, sticky=tk.E, padx=5, pady=5,
             **kwargs):
        super().grid(column=column, row=row, stick=sticky, padx=padx,
                     pady=pady, **kwargs)


# GUI for Our project
class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("EmbraceWatch Data Analysis")
        self.geometry('900x600+50+50')
        self.resizable(False, False)
        self.configure(background='#e8f4f8')

        # create a menubar
        menubar = Menu(self)
        self.config(menu=menubar)

        # create a menu
        file_menu = Menu(menubar)

        # add the File menu to the menubar
        menubar.add_cascade(
            label="File",
            menu=file_menu
        )

        # add a menu item to the menu
        file_menu.add_command(
            label='Exit',
            command=self.destroy
        )

        options_label = MenuHeader(self, text='Options')
        options_label.grid(row=0)

        users_label = MenuLabel(self, text="EmbraceWatch User ID(s):")
        users_label.grid(row=1)

        self.users_entry = MenuEntry(self)
        self.users_entry.insert(0, '310,311')
        self.users_entry.grid(row=1)

        start_label = MenuLabel(self, text="Date Start:")
        start_label.grid(row=2)

        self.start_entry = MenuEntry(self)
        self.start_entry.insert(0, '2020-01-17 23:48:00')
        self.start_entry.grid(row=2)

        end_label = MenuLabel(self, text="Date End:")
        end_label.grid(row=3)

        self.end_entry = MenuEntry(self)
        self.end_entry.insert(0, '2022-01-17 23:48:00')
        self.end_entry.grid(row=3)

        utc_label = MenuLabel(self, text="UTC:")
        utc_label.grid(row=4)

        self.utc_checkbtn = MenuCheckbutton(self)
        self.utc_checkbtn.grid(row=4)

        display_label = MenuHeader(self, text="Fields to Display")
        display_label.grid(row=5)

        acc_label = MenuLabel(self, text="ACC Avg Magnitude:")
        acc_label.grid(row=6)

        self.acc_checkbtn = MenuCheckbutton(self)
        self.acc_checkbtn.grid(row=6)

        eda_label = MenuLabel(self, text="EDA Avg:")
        eda_label.grid(row=7)

        self.eda_checkbtn = MenuCheckbutton(self)
        self.eda_checkbtn.grid(row=7)

        movement_label = MenuLabel(self, text="Movement Intensity:")
        movement_label.grid(row=8)

        self.movement_checkbtn = MenuCheckbutton(self)
        self.movement_checkbtn.grid(row=8)

        step_label = MenuLabel(self, text="Steps:")
        step_label.grid(row=9)

        self.step_checkbtn = MenuCheckbutton(self)
        self.step_checkbtn.grid(row=9)

        wrist_label = MenuLabel(self, text="On Wrist:")
        wrist_label.grid(row=10)

        self.wrist_checkbtn = MenuCheckbutton(self)
        self.wrist_checkbtn.grid(row=10)

        submit_btn = MenuSubmitButton(self, command=self.open_display_app)
        submit_btn.grid(row=11)

    def get_options(self):
        user_input = {
            'users': map(int, self.users_entry.get().split(',')),
            'start_time': datetime.strptime(self.start_entry.get(), DATE_FMT),
            'end_time': datetime.strptime(self.end_entry.get(), DATE_FMT),
            'utc_mode': self.utc_checkbtn.get(),
            'show_acc': self.acc_checkbtn.get(),
            'show_eda': self.eda_checkbtn.get(),
            'show_movement': self.movement_checkbtn.get(),
            'show_step': self.step_checkbtn.get(),
            'show_wrist': self.wrist_checkbtn.get()
        }
        return user_input

    def open_display_app(self):
        options = self.get_options()
        top = DisplayApp(options)
        top.geometry('180x100')
        top.title('toplevel')
        top.mainloop()

    def print_entries(self):
        '''
        Simple function to use as placeholder submit command.
        Also stands as an example of how to retrieve input.

        This function isn't really necessary anymore. Should be removed at end
        '''
        print('\nusers_entry: "{}"'.format(self.users_entry.get()))
        print('start_entry: "{}"'.format(self.start_entry.get()))
        print('end_entry: "{}"'.format(self.end_entry.get()))
        print('utc_checkbtn: {}'.format(self.utc_checkbtn.get()))
        print('acc_checkbtn: {}'.format(self.acc_checkbtn.get()))
        print('eda_checkbtn: {}'.format(self.eda_checkbtn.get()))
        print('movement_checkbtn: {}'.format(self.movement_checkbtn.get()))
        print('step_checkbtn: {}'.format(self.step_checkbtn.get()))
        print('wrist_checkbtn: {}'.format(self.wrist_checkbtn.get()))


#ttk.Label(root, text='Themed Label').pack()
#ttk.Button(root, text='Themed Label').pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()

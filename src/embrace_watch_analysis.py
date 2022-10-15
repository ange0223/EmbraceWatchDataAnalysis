import pandas as pd
import random
#from datetime import datetime
#from pytz import timezone
import tkinter as tk
from tkinter import ttk
from tkinter import Menu

fmt = "%Y-%m-%d %H:%M:%S"

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

        options_label = MenuHeader(self, text='Options')
        options_label.grid(row=0)

        users_label = MenuLabel(self, text="EmbraceWatch User ID(s):")
        users_label.grid(row=1)

        start_label = MenuLabel(self, text="Date Start:")
        start_label.grid(row=2)

        end_label = MenuLabel(self, text="Date End:")
        end_label.grid(row=3)

        utc_label = MenuLabel(self, text="UTC:")
        utc_label.grid(row=4)

        display_label = MenuHeader(self, text="Fields to Display:")
        display_label.grid(row=5)

        acc_label = MenuLabel(self, text="ACC Avg Magnitude:")
        acc_label.grid(row=6)

        eda_label = MenuLabel(self, text="EDA Avg:")
        eda_label.grid(row=7)

        movement_label = MenuLabel(self, text="Movement Intensity:")
        movement_label.grid(row=8)

        step_label = MenuLabel(self, text="Steps:")
        step_label.grid(row=9)

        wrist_label = MenuLabel(self, text="On Wrist:")
        wrist_label.grid(row=10)


#ttk.Label(root, text='Themed Label').pack()
#ttk.Button(root, text='Themed Label').pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()

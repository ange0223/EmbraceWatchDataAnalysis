#import pandas
#import random
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
    def _init_(self, id, person_id, date_time_utc, current_time_zone, avg_magnitude, avg_eda, avg_temp, movement_intensity, steps, rest, on_wrist):
        self.id = random.random()

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

        self.create_menubar
    
    def create_menubar(self):
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
            command=root.destroy
        )

# specifics of what is shown
#ttk.Label(root, text='Themed Label').pack()
#ttk.Button(root, text='Themed Label').pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()

import pandas as pd
import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime
from pytz import timezone

fmt = "%Y-%m-%d %H:%M:%S"

# Classes from SRS document

class Person:
    def _init_(self, id, default_time_zone):
        self.id = random.random()

class WatchData:
    def _init_(self, id, person_id, date_time_utc, current_time_zone, avg_magnitude, avg_eda, avg_temp, movement_intensity, steps, rest, on_wrist):
        self.id = random.random()

    def GetBtwn(date_time_start, date_time_end):
        # Returns data between two DateTimes. If no arguments given, returns the entire dataset.

    def GetPersonData(id):
        # Returns data from a specific Person 
    
    def GetPeopleData(id_arr):
        # Returns data from several people 

    def UpdateDisplayTimeZone(self, timezone):
        # Updates Display Timezone field with the currently selected timezone.

    def GraphData():
        # Graphs the data to a line graph. 
    
    def Analyze():
        # Readies the user selected data for viewing in the Analysis window

class User:
    def _init_(self):
        self.id = random.random()
        self.local_time_zone =

    def GetLocalTimeZone():
        # Gets the local time zone for the current user based on the system the software is currently running on.

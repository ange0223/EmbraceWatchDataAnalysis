import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *


class CommonTextBox(tk.Text):
    def __init__(self, parent, width=20, height=5, *args, **kwargs):
        super().__init__(*args, **kwargs)


class QueryWindow(tk.Toplevel):
    def __init__(self, on_apply=None, on_undo=None):
        super().__init__()
        self.on_apply = on_apply
        self.on_undo = on_undo
        self.title('SQL Query')
        self.geometry('500x600+100+100')

        entry_frame = ttk.Frame(self)
        entry_frame.pack(side=tk.TOP)

        self.query_entry = CommonTextBox(self)
        self.query_entry.pack()

        self.result_entry = CommonTextBox(self)
        self.result_entry.pack()

        btn_frame = ttk.Frame(self)
        btn_frame.pack()

        self.undo_btn = ttk.Button(btn_frame, text='Undo', command=self.undo)
        self.undo_btn.pack(side=tk.LEFT)

        self.apply_btn = ttk.Button(btn_frame, text='Apply', command=self.apply)
        self.apply_btn.pack(side=tk.RIGHT)

    def apply(self):
        query = self.query_entry.get()
        self.on_apply(query)

    def undo(self):
        self.on_undo()


if __name__ == '__main__':
    print('Button frame not currently showing')
    qw = QueryWindow(
        on_apply=lambda query : print('QueryWindow.apply(): query={}'.format(
                query)),
        on_undo=lambda : print('QueryWindow.undo()')
    )
    qw.lift()
    qw.mainloop()

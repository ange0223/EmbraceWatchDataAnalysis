import tkinter as tk
from tkinter import ttk, Menu
from tkinter.constants import *


class TextBox(tk.Text):
    def __init__(self, parent, width=80, height=15, *args, **kwargs):
        super().__init__(parent, *args, width=width, height=height, **kwargs)


class Button(ttk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def pack(self, padx=20, pady=20, **kwargs):
        super().pack(padx=padx, pady=pady, **kwargs)


class QueryWindow(tk.Toplevel):
    def __init__(self, on_apply=None, on_undo=None, on_quit=None):
        super().__init__()
        self.on_apply = on_apply
        self.on_undo = on_undo
        self.on_quit = on_quit
        self.title('Query')
        self.geometry('500x600+100+100')

        entry_frame = ttk.Frame(self)
        entry_frame.pack(side=tk.TOP)

        self.query_entry = TextBox(entry_frame)
        self.query_entry.pack()
        self.query_entry.insert(1.0, "SELECT `Steps count`\nFROM data;")

        self.result_entry = TextBox(entry_frame)
        self.result_entry.pack()

        btn_frame = ttk.Frame(self)
        btn_frame.pack()

        self.undo_btn = Button(btn_frame, text='Undo',
                               command=self.undo)
        self.undo_btn.pack(side=tk.LEFT)

        self.apply_btn = Button(btn_frame, text='Apply',
                                command=self.apply)
        self.apply_btn.pack(side=tk.RIGHT)
        self.protocol('WM_DELETE_WINDOW', self.on_quit)

    def apply(self):
        query = self.query_entry.get('1.0', 'end-1c')
        self.on_apply(query)

    def update_result(self, string):
        self.result_entry.delete('1.0', "end")
        self.result_entry.insert('1.0', string)

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

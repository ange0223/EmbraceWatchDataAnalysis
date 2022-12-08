from datetime import datetime
from tkinter.filedialog import asksaveasfile


DATE_FMT = '%Y-%m-%d %H:%M:%S'


def str_to_datetime(string):
    return datetime.strptime(string, DATE_FMT)


def save_figure(figure, init_filename='untitled.png'):
    print('save_figure()')
    save_path = asksaveasfile(mode='a', filetypes=[('PNG image', '*.png')],
                              initialfile=init_filename,
                              defaultextension=".png")
    if save_path:
        figure.savefig(save_path.name)
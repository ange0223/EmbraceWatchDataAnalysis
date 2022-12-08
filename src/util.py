from datetime import datetime
from tkinter.filedialog import asksaveasfile


def str_to_datetime(string, date_fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(string, date_fmt)


def save_figure(figure, init_filename='untitled.png'):
    print('save_figure()')
    save_path = asksaveasfile(mode='a', filetypes=[('PNG image', '*.png')],
                              initialfile=init_filename,
                              defaultextension=".png")
    if save_path:
        figure.savefig(save_path.name)
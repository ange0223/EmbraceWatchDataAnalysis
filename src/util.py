from datetime import datetime
from tkinter.filedialog import asksaveasfile


def str_to_datetime(string, dt_fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(string, dt_fmt)


def datetime_to_str(dt, dt_fmt='%Y-%m-%d %H:%M:%S'):
    return dt.strftime(dt_fmt)


def valid_agg_intervals():
    return ('1ms', '5ms', '50ms', '500ms', '1S', '1min', '30min', '1H',
            '3H', '6H', 'D', 'W')


def save_figure(figure, init_filename='untitled.png'):
    save_path = asksaveasfile(
        mode='a',
        filetypes=[('PNG image', '*.png')],
        initialfile=init_filename,
        defaultextension=".png")
    if save_path:
        figure.savefig(save_path.name)
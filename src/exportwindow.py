from tkinter.filedialog import asksaveasfile


def open_save_dialog(df):
    save_path = asksaveasfile(mode='a', filetypes=[('CSV', '*.csv')],
                              initialfile='untitled.csv',
                              defaultextension=".csv")
    if save_path:
        df.to_csv(save_path.name, index=False)


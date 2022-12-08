from datetime import datetime


DATE_FMT = '%Y-%m-%d %H:%M:%S'


def str_to_datetime(string):
    return datetime.strptime(string, DATE_FMT)
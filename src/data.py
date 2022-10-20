import pandas as pd
import os
import sys


def load_summary(csv_path):
    '''
    Load data from summary.csv file for a single day/subject and
    return result as a pandas dataframe.
    Note that the returned dataframe does not have any subject ID column.
    Args:
        csv_path: path to the 'summary.csv' file to load
    '''
    df = pd.read_csv(csv_path)
    df = df.astype({
        'Datetime (UTC)': 'datetime64',
        'Timezone (minutes)': 'int',
        'Unix Timestamp (UTC)': 'int64',
        'Acc magnitude avg': 'float64',
        'Eda avg': 'float64',
        'Temp avg': 'float64',
        'Movement intensity': 'int64',
        'Steps count': 'int64',
        'Rest': 'int64',
        'On Wrist': 'bool'
    })
    return df


def load_data(data_path, subs=None):
    #print(len(subs))

    '''
    Load data from `data_path` for given `subs` (subjects -- all if not set)
    and return as pandas dataframe.
    Args:
        data_path: path to root level of dataset directory
        subs: list of subjects (default: None -- include all)
    '''
    try:
        day_dirs = os.listdir(data_path)
    except FileNotFoundError as e:
        print('Data path "{}" not found.'.format(data_path))
        return None
    # Empty dataframe to store accumulated data
    data = pd.DataFrame()
    for day_dir in day_dirs:
        day_path = os.path.join(data_path, day_dir)
        for sub_dir in os.listdir(day_path):
            # Only care if sub is one that was requested
            if subs is not None and int(sub_dir) not in subs:
                continue
            sub_path = os.path.join(day_path, sub_dir)
            summary_path = os.path.join(sub_path, 'summary.csv')
            # Skip if dir doesn't have summary.csv
            if not os.path.exists(summary_path):
                continue
            day_subject = load_summary(summary_path)
            # Add subject column
            day_subject['subject_id'] = int(sub_dir)
            # Add to data dataframe
            data = pd.concat([data, day_subject])
    return data


if __name__ == '__main__':
    usage_msg = 'Usage: "{} [-q]"'.format(sys.argv[0])
    # Simple sanity check test
    if len(sys.argv) == 1:
        quick_check = False
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg in {'-q', '--quick'}:
            quick_check = True
        else:
            print('Unknown arg "{}" passed.'.format(arg))
            print(usage_msg)
            sys.exit(1)
    else:
        print('Invalid number of arguments passed.')
        print(usage_msg)
        sys.exit(1)
    if quick_check:
        data_path = ''
        subs = '310'
    else:
        data_path = input('Please enter data path (blank: Dataset): ')
        subs = input('Please enter subjects (blank: all) (Ex: 310,311): ')
    if len(data_path) == 0: data_path = 'Dataset'
    print('data_path: "{}"'.format(data_path))
    print('subs: "{}"'.format(subs))
    if subs:
        subs = list(map(int, subs.split(',')))
        data = load_data(data_path, subs=subs)
    else: data = load_data(data_path)
    print('\ndata.head():')
    print(data.head())
    print('\ndata.info: ')
    print(data.info())
    print('\ndata[\'subject_id\'].unique(): ')
    print(data['subject_id'].unique())
    print('\ndata.iloc[0]:')
    print(data.iloc[0])

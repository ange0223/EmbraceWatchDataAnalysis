import os
from datetime import datetime
import time

from src.displayapp import DisplayApp
from src.data import load_data


def pause_for_review(t=2):
    #time.sleep(t)
    pass


if __name__ == '__main__':
    app = DisplayApp()
    # Load initial data as if if import window called back
    print('Performing initial data load')
    data_path = os.path.join(os.getcwd(), 'Dataset')
    date_fmt = '%Y-%m-%d %H:%M:%S'
    options = {
        'users': 310,
        'start_time': datetime.strptime('2020-01-17 23:48:00', date_fmt),
        'end_time': datetime.strptime('2022-01-17 23:48:00', date_fmt),
        'utc_mode': False,
        'show_acc': True,
        'show_eda': True,
        'show_temp': True,
        'show_movement': True,
        'show_step': True,
        'show_rest': True,
        'show_wrist': True
    }
    data = load_data(data_path, **options)
    app.on_import_submit(data, options)
    print('Data submitted via app.on_import_submit()')
    pause_for_review()

    dt_min, dt_max = '2020-01-17 23:49:00', '2020-01-18 19:06:00'
    print(f'Applying time range selection: ({dt_min}, {dt_max})')
    app.time_selector.set(dt_min, dt_max)
    app.on_time_range_selector_apply(dt_min, dt_min)
    pause_for_review()

    # Delete all but one series
    print('Deleting all but one series:', end='')
    ignore_cols = {'Datetime', 'Datetime (UTC)', 'Timezone (minutes)',
                   'Unix Timestamp (UTC)', 'subject_id'}
    cols = sorted(list(set(app.active_data.columns) - ignore_cols))
    print(f'"{cols[0]}"')
    done = set()
    for col in cols:
        if len(done) == len(cols)-1:
            break
        app.delete_series(col)
        done.add(col)
    print(f'app.active_data.columns: ({len(app.active_data.columns)}) {set(app.active_data.columns)}')
    print(f'app.figure_cols: ({len(app.figure_cols)}) {app.figure_cols}')
    print(f'app.figure_kinds: ({len(app.figure_kinds)}) {app.figure_kinds}')
    print(f'done: ({len(done)}) {done}')
    assert(len(set(app.active_data.columns) & done) == 0) # no removed figure cols
    assert(len(set(app.active_data.columns) & set(cols)) == 1) # only 1 figure col
    assert(len(app.figure_cols) == 1)
    assert(len(app.figure_kinds) == 1)
    print(' PASS')
    pause_for_review()

    # Try to apply an invalid time range -- an error popup should be shown
    # and changes to the time range (dt_max < dt_min)
    print('Attempting to apply an invalid time range')
    dt_min, dt_max = '2020-01-27 23:49:00', dt_max
    app.time_selector.set_min(dt_min)
    app.on_time_range_selector_apply(dt_min, dt_max)
    pause_for_review()

    # Set time range to something more reasonable
    print('Setting time range to something reasonable')
    dt_min, dt_max = '2020-01-17 23:49:00', '2020-01-19 00:00:00'
    app.time_selector.set(dt_min, dt_max)
    app.on_time_range_selector_apply(dt_min, dt_max)
    pause_for_review()

    # Import data, override existing data
    print('Reimporting data and options')
    app.on_import_submit(data, options)
    pause_for_review()

    # Move bottom figure up to top and top figure down to bottom
    print('Moving bottom figure to top and top figure to bottom')
    print(f'app.figure_cols: {app.figure_cols}')
    top_col = app.figure_cols[0]
    print(f'  top_col: "{top_col}"')
    bottom_col = app.figure_cols[-1]
    print(f'  bottom_col: "{bottom_col}"')
    required_moves = len(app.figure_cols) - 1
    moves_count = 0
    while app.figure_cols[0] != bottom_col and app.figure_cols[-1] != top_col:
        if app.figure_cols[0] != bottom_col:
            app.move_figure_up(bottom_col)
        if app.figure_cols[-1] != top_col:
            app.move_figure_down(top_col)
        assert(moves_count <= required_moves)
        moves_count += 1
    pause_for_review()

    print('Aggregating data')
    # Aggregate to 6H (6 hours)
    print('Aggregating to 6H')
    app.aggregate('6H')
    pause_for_review()
    # Then to 1D (1 day)
    print('Aggregating to 6H')
    app.aggregate('1D')
    pause_for_review()
    # Then to 1S (1 second)
    print('Aggregating to 6H')
    app.aggregate('1S')
    pause_for_review()
    # Then back to 1min (1 minute)
    print('Aggregating to 6H')
    app.aggregate('1min')
    pause_for_review()

    # Change draw style of first three figures
    cols = app.figure_cols
    print(f'Setting draw style of first column "{cols[0]}" to "bar"')
    app.set_draw_style(cols[0], 'bar')
    pause_for_review()
    print(f'Setting draw style of second column "{cols[1]}" to "scatter"')
    app.set_draw_style(cols[1], 'scatter')
    pause_for_review()
    print(f'Setting draw style of third column "{cols[2]} to "barh"')
    app.set_draw_style(cols[2], 'barh')
    pause_for_review()

    # Open query window and manually apply a query
    cols_prev = set(app.active_data.columns)
    print('Opening query window')
    app.open_query_window()
    pause_for_review()
    query = 'SELECT `Steps count` FROM data;'
    print(f'Applying the following query: "{query}"')
    app.apply_query(query)
    pause_for_review()
    print(f' Checking | only queried columns remain:', end='')
    cols = set(app.active_data.columns) - ignore_cols
    assert(cols == {'Steps count'})
    print(' PASS')
    print(f'Undoing query')
    dt_min_bak = app.time_selector.time_min_bak
    dt_max_bak = app.time_selector.time_max_bak
    dt_min_prev, dt_min_prev = app.time_selector.get()
    app.undo_query()
    print(f' Checking | time range reset after undoing query:', end='')
    assert(app.time_selector.get_min() == dt_min_bak)
    assert(app.time_selector.get_max() == dt_max_bak)
    print('PASS')
    print(f' Checking | deleted cols return after undoing query:', end='')
    assert(set(app.active_data.columns) == cols_prev)
    print('PASS')
    pause_for_review()

    # Open describe window for 'Movement intensity' column
    print(f'Opening describe window for "Movement intensity"')
    app.open_describe_window('Movement intensity')
    pause_for_review()
    print(f'Setting time range to affect describe window')
    dt_min, dt_max = '2020-01-17 23:49:00', '2020-01-21 00:00:00'
    app.time_selector.set(dt_min, dt_max)
    app.on_time_range_selector_apply(dt_min, dt_max)
    pause_for_review()
    print(f'Toggling UTC mode to affect describe window')
    app.toggle_utc()
    pause_for_review()
    print(f'Toggling UTC mode back to affect describe window')
    app.toggle_utc()
    pause_for_review()
    print('Aggregating to 6H to affect describe window')
    app.aggregate('6H')
    pause_for_review()
    print('Aggregating back to 1min')
    app.aggregate('1min')
    pause_for_review()
    print('Querying on data (removing described series)')
    app.apply_query(query)
    pause_for_review()
    print('Undoing query')
    app.undo_query()
    pause_for_review()
    print('Querying on data (modifying described series)')
    query = """SELECT `Movement intensity`
FROM data
WHERE `Movement intensity` < 60;"""
    print(' query={}'.format(query.replace('\n', '')))
    app.query_window.query_entry.insert(1.0, query)
    app.apply_query(query)
    pause_for_review()
    print('Undoing query')
    app.undo_query()
    pause_for_review()

    # Clear all
    print('Clearing all data and plots')
    app.clear_all()
    pause_for_review()

    # Reimport data
    print('Reloading data')
    app.on_import_submit(data, options)
    pause_for_review()

    # Export data
    export_path = os.path.join(os.getcwd(), '../src', 'tmp', 'untitled.csv')
    print(f'Export data. Save to "{export_path}" for validation:', end='')
    app.open_export_dialog()
    assert(os.path.exists(export_path))
    assert(os.path.isfile(export_path))
    export_size = os.path.getsize(export_path)
    assert(export_size > 0)
    print(' PASS')
    print(f'Exported file size: {export_size} bytes')
    pause_for_review()

    # Save figure
    print('Save a figure')
    save_path = os.path.join(os.getcwd(), '../src', 'tmp',
                             'Movement intensity.png')
    print('Please wait. Moving "Movement intensity" figure to top...', end='')
    # First, move 'Movement intensity' to top
    assert('Movement intensity' in app.figure_cols)
    while app.figure_cols[0] != 'Movement intensity':
        app.move_figure_up('Movement intensity')
    print(' Done')
    print(f'Please save "Movement intensity" figure to "{save_path}"', end='')
    print(' for validation:')
    assert (os.path.exists(save_path))
    assert (os.path.isfile(save_path))
    saved_size = os.path.getsize(save_path)
    assert (saved_size > 0)
    print(' PASS')
    print(f'Saved image file size: {saved_size} bytes')
    pause_for_review()
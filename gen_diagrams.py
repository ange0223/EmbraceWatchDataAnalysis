import subprocess
import os
import shutil
from zipfile import ZipFile
from datetime import datetime


DATETIME_FMT = '%Y%m%dT%H%M%S'


def is_module(path):
    if not os.path.isfile(path):
        return False
    if not path.endswith('.py'):
        return False
    return True


def get_modules(src_dir, ignore=set()):
    is_valid = lambda f: is_module(os.path.join(src_dir, f)) and f not in ignore
    return [f for f in os.listdir(src_dir) if is_valid(f)]


datetime_str = datetime.now().strftime(DATETIME_FMT)
overwrite = True
compress = True
discard_out_dir = True # after compression
out_dir = 'diagrams_' + datetime_str
src_dir = 'src'
zip_file_name = out_dir + '.zip'

# Delete old out_dir if exists and overwrite set
if os.path.exists(out_dir):
    if not overwrite:
        print('Out directory already exists and overwrite=False')
        exit()
    shutil.rmtree(out_dir)

# Create new empty out_dir
os.mkdir(out_dir)

# Base command from which others are derived
base_cmd = 'pyreverse -o png -A -a0 -S -d {out_dir}'.format(out_dir=out_dir)

# Nothing useful produced by these (literally blank)
ignore = {'__init__.py', 'data.py', 'exportwindow.py', 'main.py'}
modules = get_modules(src_dir, ignore=ignore)
paths = list(map(lambda name: os.path.join(src_dir, name), modules))
cmd_fmt = base_cmd + ' -p {out_base_name} {module}'
# Output one for each module
for name, path in zip(modules, paths):
    subprocess.run(cmd_fmt.format(
        out_base_name='src.{0}_{1}'.format(name, datetime_str),
        module=path))
    

# Finally, generate one of everything
cmd_fmt = base_cmd + ' {src_dir}'
# Will come out as two images: classes.png and packages.png
subprocess.run(cmd_fmt.format(src_dir=src_dir))

# Compress out_dir into a zip_file
with ZipFile(zip_file_name, 'w') as zf:
    for path, directories, files in os.walk(out_dir):
        for file in files:
            file_path = os.path.join(path, file)
            zf.write(file_path)

# Destroy out_dir is discard_out_dir set
if discard_out_dir:
    shutil.rmtree(out_dir)

from cx_Freeze import setup, Executable
import os

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))

os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# Dependencies are automatically detected, but it might need
# fine tuning.

buildVersion = 0.1

buildOptions = dict(packages = ["os"], 
                    include_files = [
                    os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll')
                    ,os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')  
                    ],
                    includes= ["tkinter","email","http","tkinter.ttk","secrets"],
                    excludes = [
                    'PIL',  
                    'distutils',  
                    'future', 
                    'pydoc_data',
                    'setuptools', 
                    'test', 
                    'tests', 
                    'test', 
                    "colorama",
                    "curses",
                    "email",
                    "jinja2",
                    "markupsafe",
                    "scipy",
                    "numba",
                    "numpy.core._dotblas",
                    "PIL",
                    "pycparser",
                    "PyQt4.QtNetwork",
                    "PyQt4.QtScript",
                    "PyQt4.QtSql",
                    "PyQt5",
                    "pytz",
                    "scipy.lib.lapack.flapack",
                    "sqlite3",
                    "test",
                    'dbm',
                    'http',
                    'llvmlite',
                    'matplotlib',
                    'sklearn',
                    'multiprocessing',
                    'test',
                    'unittest',
                    'xmlrpc',
                    ])


base = "console"

executables = [
Executable('infiniteclipboard.py', base=base)
]

setup(name='InfiniteClipboard',
      version = '1.1',
      description = 'UI and Automation to generate high quality VP8 webms',
      options = dict(build_exe = buildOptions),
      executables = executables)

# The Uppercase name is detected first in a failed Queue import and
# doesn't get lowercased again (possibly only with case insensitive paths)
# this renames Tkinter->tkinter.
import os
import glob

for buildPath in glob.glob(os.path.join('build','*')):
  os.chdir(buildPath)
  finalZipLocation = os.path.join('.','infiniteclipboard-win64-{}.zip'.format(buildVersion))
  print(finalZipLocation)
  print(buildPath)
  z7cmd = '"C:\\Program Files\\7-Zip\\7z" a -mm=Deflate -mfb=258 -mpass=15 -r {} {}'.format(finalZipLocation,'.')
  print(z7cmd)
  os.system(z7cmd)
  break

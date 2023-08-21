# Monkey patch for subprocess to use 8.3 filenames - Windows only (no dependencies)

## Tested against Windows 10 / Python 3.10 / Anaconda

## pip install subprocessmonkey

The module automatically converts long paths to their short 8.3 equivalents


```python
import subprocess
from subprocessmonkey import patch_subprocess,subprocconfig
subprocconfig.minlen = None # minimum path length - calculated automatically if None
subprocconfig.convert_to_abs_path = True # \Windows to c:\\Windows
patch_subprocess() # updates subprocess.list2cmdline and subprocess.Popen._execute_child 


# Works like a charm :)

subprocess.Popen(r"ffplay C:\Users\hansc\Videos\sdf dsf sdf .mkv")

subprocess.Popen(r'cat C:\Users\hansc\Downloads\hosts (1)')

subprocess.run('ls C:\\Program Files')
```
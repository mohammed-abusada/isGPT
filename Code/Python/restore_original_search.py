import os
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

if os.path.exists("reproduce_baseline.py.backup2"):
    shutil.copy("reproduce_baseline.py.backup2", "reproduce_baseline.py")
    print("Original search space restored!")
else:
    print("Backup not found. Please restore manually.")

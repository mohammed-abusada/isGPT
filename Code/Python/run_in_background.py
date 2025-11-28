"""
Run baseline reproduction in the background.
Results will be saved to log files.
"""

import os
import sys
import subprocess
from datetime import datetime

# Change to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

configurations = [
    {
        "name": "Independent Test (SMOTE, Regression)",
        "balancing": "_SMOTED",
        "use_cv": False,
        "n_folds": 10,
        "regression": True,
        "log_file": "logs_independent_test.log"
    },
    {
        "name": "10-Fold CV (SMOTE, Regression)",
        "balancing": "_SMOTED",
        "use_cv": True,
        "n_folds": 10,
        "regression": True,
        "log_file": "logs_10fold_cv.log"
    },
    {
        "name": "Jackknife (SMOTE, Regression)",
        "balancing": "_SMOTED",
        "use_cv": True,
        "n_folds": -1,
        "regression": True,
        "log_file": "logs_jackknife.log"
    }
]

# Create logs directory
os.makedirs("logs", exist_ok=True)

print("="*70)
print("BACKGROUND EXECUTION SETUP")
print("="*70)
print(f"Started at: {datetime.now()}\n")

for config in configurations:
    log_path = os.path.join("logs", config["log_file"])
    
    print(f"Starting: {config['name']}")
    print(f"  Log file: {log_path}")
    
    # Build command
    cmd = [
        sys.executable, "reproduce_baseline.py",
        "--balancing", config["balancing"],
        "--use_cv", str(config["use_cv"]),
        "--n_folds", str(config["n_folds"]),
        "--regression", str(config["regression"])
    ]
    
    # Start process in background
    with open(log_path, "w") as log_file:
        process = subprocess.Popen(
            cmd,
            stdout=log_file,
            stderr=subprocess.STDOUT,
            text=True
        )
    
    print(f"  Process ID: {process.pid}")
    print(f"  Status: Running in background")
    print()

print("="*70)
print("All processes started in background!")
print("="*70)
print("\nTo check progress:")
print("  - Windows PowerShell: Get-Content logs\\logs_jackknife.log -Wait -Tail 20")
print("  - Linux/Mac: tail -f logs/logs_jackknife.log")
print("\nTo check if processes are running:")
print("  - Windows: Get-Process python")
print("  - Linux/Mac: ps aux | grep python")
print("\nTo stop a process:")
print("  - Windows: Stop-Process -Id <PID>")
print("  - Linux/Mac: kill <PID>")
print("="*70)


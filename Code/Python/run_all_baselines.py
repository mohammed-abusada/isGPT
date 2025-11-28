"""
Run all baseline configurations and collect results.
"""

import os
import sys
import subprocess
import pandas as pd
from datetime import datetime

# Change to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

configurations = [
    {"name": "Independent Test (SMOTE, Regression)", "balancing": "_SMOTED", "use_cv": False, "n_folds": 10, "regression": True},
    {"name": "10-Fold CV (SMOTE, Regression)", "balancing": "_SMOTED", "use_cv": True, "n_folds": 10, "regression": True},
    {"name": "Jackknife (SMOTE, Regression)", "balancing": "_SMOTED", "use_cv": True, "n_folds": -1, "regression": True},
]

def modify_and_run(config):
    """Run script with command line arguments."""
    print(f"\n{'='*70}")
    print(f"Running: {config['name']}")
    print(f"{'='*70}")
    
    # Build command
    cmd = [sys.executable, "reproduce_baseline.py",
           "--balancing", config["balancing"],
           "--use_cv", str(config["use_cv"]),
           "--n_folds", str(config["n_folds"]),
           "--regression", str(config.get("regression", False))]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

# No need to restore config when using command line args

# Run all configurations
print("="*70)
print("RUNNING ALL BASELINE CONFIGURATIONS")
print("="*70)

results = []
for i, config in enumerate(configurations, 1):
    print(f"\n[{i}/{len(configurations)}] {config['name']}")
    
    # Check if SMOTE file exists
    if config["balancing"] == "_SMOTED":
        smote_file = "../R/featurized_comb_SMOTED.rds"
        if not os.path.exists(smote_file):
            print(f"  SKIPPED: {smote_file} not found")
            results.append({"Configuration": config['name'], "Status": "SKIPPED"})
            continue
    
    success = modify_and_run(config)
    results.append({"Configuration": config['name'], "Status": "SUCCESS" if success else "FAILED"})

# Print summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)
for r in results:
    status_symbol = "[OK]" if r['Status'] == 'SUCCESS' else "[FAIL]" if r['Status'] == 'FAILED' else "[SKIP]"
    print(f"{status_symbol} {r['Configuration']}: {r['Status']}")

print("\n" + "="*70)
print("Results saved in baseline_out_*.csv files")
print("="*70)


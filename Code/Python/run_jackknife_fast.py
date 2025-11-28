"""
Fast Jackknife CV using best parameters from 10-fold CV.
This avoids the expensive parameter search by using pre-determined optimal values.
"""

import os
import sys
import subprocess
from datetime import datetime

# Change to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("="*70)
print("FAST JACKKNIFE CV - Using Best Parameters")
print("="*70)

# Best parameters from 10-fold CV (you can update these after running 10-fold CV)
# These will be automatically extracted from the results file if available
BEST_FEATURES = 2800  # Will be updated from results
BEST_C = 30  # Will be updated from results

# Try to read best parameters from 10-fold CV results
try:
    import pandas as pd
    cv_results_file = "../R/baseline_out_comb_SMOTED.csv"
    if os.path.exists(cv_results_file):
        df = pd.read_csv(cv_results_file)
        if 'MCC' in df.columns:
            best_idx = df['MCC'].idxmax()
            BEST_FEATURES = int(df.loc[best_idx, 'FeatureCount'])
            BEST_C = float(df.loc[best_idx, 'SVMCost'])
            print(f"Found best parameters from CV results:")
            print(f"  Features: {BEST_FEATURES}")
            print(f"  C: {BEST_C}")
            print(f"  MCC: {df.loc[best_idx, 'MCC']:.4f}")
        else:
            print("Using default parameters (best from independent test)")
    else:
        print("CV results file not found. Using default parameters.")
except Exception as e:
    print(f"Could not read CV results: {e}")
    print("Using default parameters.")

print("\n" + "="*70)
print(f"Running Jackknife CV with fixed parameters:")
print(f"  Features: {BEST_FEATURES}")
print(f"  C: {BEST_C}")
print("="*70)

# Modify the script temporarily to use fixed parameters
script_content = None
with open("reproduce_baseline.py", "r", encoding="utf-8") as f:
    script_content = f.read()

# Save original
with open("reproduce_baseline.py.backup", "w", encoding="utf-8") as f:
    f.write(script_content)

# Modify to use fixed parameters
modified_content = script_content
# Replace feature count list
if f"FEATURE_COUNT_LIST = list(range(2800, 1499, -50))" in modified_content:
    modified_content = modified_content.replace(
        f"FEATURE_COUNT_LIST = list(range(2800, 1499, -50)) if DO_REGRESSION and BALANCING == \"_SMOTED\" else [2800]",
        f"FEATURE_COUNT_LIST = [{BEST_FEATURES}]  # Fixed from best CV params"
    )
else:
    # Find and replace the feature count line
    import re
    pattern = r"FEATURE_COUNT_LIST = .*?# BASELINE"
    replacement = f"FEATURE_COUNT_LIST = [{BEST_FEATURES}]  # Fixed from best CV params"
    modified_content = re.sub(pattern, replacement, modified_content)

# Replace C value list
if "SVM_COST_LIST = [0.3, 1, 3, 10, 30, 100]" in modified_content:
    modified_content = modified_content.replace(
        "SVM_COST_LIST = [0.3, 1, 3, 10, 30, 100] if DO_REGRESSION and BALANCING == \"_SMOTED\" else [1.0]",
        f"SVM_COST_LIST = [{BEST_C}]  # Fixed from best CV params"
    )
else:
    pattern = r"SVM_COST_LIST = .*?# BASELINE"
    replacement = f"SVM_COST_LIST = [{BEST_C}]  # Fixed from best CV params"
    modified_content = re.sub(pattern, replacement, modified_content)

# Write modified script
with open("reproduce_baseline.py", "w", encoding="utf-8") as f:
    f.write(modified_content)

# Run jackknife
print(f"\n{datetime.now()} >> Starting Jackknife CV...")
print("This will take approximately 2-5 minutes...\n")

result = subprocess.run(
    [sys.executable, "reproduce_baseline.py",
     "--balancing", "_SMOTED",
     "--use_cv", "True",
     "--n_folds", "-1",
     "--regression", "True"],
    capture_output=False,  # Show output in real-time
    text=True
)

# Restore original script
with open("reproduce_baseline.py.backup", "r", encoding="utf-8") as f:
    original_content = f.read()
with open("reproduce_baseline.py", "w", encoding="utf-8") as f:
    f.write(original_content)
os.remove("reproduce_baseline.py.backup")

print(f"\n{datetime.now()} >> Jackknife CV complete!")
print("="*70)


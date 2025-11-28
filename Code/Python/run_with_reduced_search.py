"""
Run baseline with reduced parameter search space for faster execution.
Reduces from 162 combinations to 24 combinations.
"""

import os
import sys

# Change to script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Reduced search space
REDUCED_FEATURE_COUNTS = [2800, 2500, 2250, 2000, 1750, 1500]  # 6 values instead of 27
REDUCED_C_VALUES = [1, 10, 30, 100]  # 4 values instead of 6
# Total: 6 × 4 = 24 combinations (vs 162 original)

print("="*70)
print("REDUCED PARAMETER SEARCH")
print("="*70)
print(f"Feature counts: {REDUCED_FEATURE_COUNTS}")
print(f"C values: {REDUCED_C_VALUES}")
print(f"Total combinations: {len(REDUCED_FEATURE_COUNTS) * len(REDUCED_C_VALUES)}")
print("="*70)

# Read script
with open("reproduce_baseline.py", "r", encoding="utf-8") as f:
    content = f.read()

# Save backup
with open("reproduce_baseline.py.backup2", "w", encoding="utf-8") as f:
    f.write(content)

# Modify feature count list
import re
pattern = r"FEATURE_COUNT_LIST = list\(range\(2800, 1499, -50\)\) if DO_REGRESSION and BALANCING == \"_SMOTED\" else \[2800\]"
replacement = f"FEATURE_COUNT_LIST = {REDUCED_FEATURE_COUNTS} if DO_REGRESSION and BALANCING == \"_SMOTED\" else [2800]"
content = re.sub(pattern, replacement, content)

# Modify C value list
pattern = r"SVM_COST_LIST = \[0\.3, 1, 3, 10, 30, 100\] if DO_REGRESSION and BALANCING == \"_SMOTED\" else \[1\.0\]"
replacement = f"SVM_COST_LIST = {REDUCED_C_VALUES} if DO_REGRESSION and BALANCING == \"_SMOTED\" else [1.0]"
content = re.sub(pattern, replacement, content)

# Write modified
with open("reproduce_baseline.py", "w", encoding="utf-8") as f:
    f.write(content)

print("\nScript modified. You can now run:")
print("  python reproduce_baseline.py --balancing \"_SMOTED\" --use_cv \"True\" --n_folds -1 --regression \"True\"")
print("\nEstimated time with reduced search:")
print("  - Independent test: ~5-10 seconds")
print("  - 10-fold CV: ~1-2 minutes")
print("  - Jackknife: ~30-45 minutes")
print("\nTo restore original search space, run:")
print("  python restore_original_search.py")

# Create restore script
restore_script = """import os
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

if os.path.exists("reproduce_baseline.py.backup2"):
    shutil.copy("reproduce_baseline.py.backup2", "reproduce_baseline.py")
    print("Original search space restored!")
else:
    print("Backup not found. Please restore manually.")
"""

with open("restore_original_search.py", "w", encoding="utf-8") as f:
    f.write(restore_script)

print("\nRestore script created: restore_original_search.py")


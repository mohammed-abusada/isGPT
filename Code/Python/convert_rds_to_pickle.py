"""
Helper script to convert RDS files to pickle format for easier Python access.
This is optional - the main script can read RDS files directly using pyreadr.

Usage:
    python convert_rds_to_pickle.py

This will convert all .rds files in the R directory to .pkl files.
"""

import os
import sys
import pickle
try:
    import pyreadr
except ImportError:
    print("pyreadr not installed. Installing...")
    os.system("pip install pyreadr")
    import pyreadr

def convert_rds_to_pickle(rds_file, pkl_file=None):
    """Convert a single RDS file to pickle format."""
    if pkl_file is None:
        pkl_file = rds_file.replace('.rds', '.pkl')
    
    try:
        print(f"Converting {rds_file} to {pkl_file}...")
        result = pyreadr.read_r(rds_file)
        
        # pyreadr returns a dict, get the first (and usually only) dataframe
        if result:
            data = list(result.values())[0]
            with open(pkl_file, 'wb') as f:
                pickle.dump(data, f)
            print(f"  Successfully converted to {pkl_file}")
            return True
        else:
            print(f"  Warning: No data found in {rds_file}")
            return False
    except Exception as e:
        print(f"  Error converting {rds_file}: {e}")
        return False

def main():
    """Convert all RDS files in the R directory."""
    # Get R directory path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    r_dir = os.path.join(os.path.dirname(script_dir), 'R')
    
    if not os.path.exists(r_dir):
        print(f"R directory not found: {r_dir}")
        return
    
    print(f"Looking for RDS files in: {r_dir}")
    
    # Find all RDS files
    rds_files = []
    for root, dirs, files in os.walk(r_dir):
        for file in files:
            if file.endswith('.rds'):
                rds_files.append(os.path.join(root, file))
    
    if not rds_files:
        print("No RDS files found.")
        return
    
    print(f"Found {len(rds_files)} RDS file(s).")
    
    # Convert each file
    success_count = 0
    for rds_file in rds_files:
        if convert_rds_to_pickle(rds_file):
            success_count += 1
    
    print(f"\nConversion complete: {success_count}/{len(rds_files)} files converted successfully.")

if __name__ == "__main__":
    main()


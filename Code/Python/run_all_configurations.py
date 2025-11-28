"""
Run baseline reproduction with all configurations:
1. Independent test (no SMOTE)
2. Independent test (with SMOTE)
3. 10-fold cross-validation (no SMOTE)
4. 10-fold cross-validation (with SMOTE)
5. Jackknife/Leave-one-out (no SMOTE)
6. Jackknife/Leave-one-out (with SMOTE)
"""

import os
import sys
import subprocess
from datetime import datetime

# Configuration combinations to run
configurations = [
    {
        "name": "Independent Test (No SMOTE)",
        "balancing": "",
        "use_cv": False,
        "n_folds": 10
    },
    {
        "name": "Independent Test (With SMOTE)",
        "balancing": "_SMOTED",
        "use_cv": False,
        "n_folds": 10
    },
    {
        "name": "10-Fold Cross-Validation (No SMOTE)",
        "balancing": "",
        "use_cv": True,
        "n_folds": 10
    },
    {
        "name": "10-Fold Cross-Validation (With SMOTE)",
        "balancing": "_SMOTED",
        "use_cv": True,
        "n_folds": 10
    },
    {
        "name": "Jackknife/Leave-One-Out (No SMOTE)",
        "balancing": "",
        "use_cv": True,
        "n_folds": -1
    },
    {
        "name": "Jackknife/Leave-One-Out (With SMOTE)",
        "balancing": "_SMOTED",
        "use_cv": True,
        "n_folds": -1
    }
]

def modify_config(balancing, use_cv, n_folds):
    """Modify the reproduce_baseline.py configuration."""
    script_path = "reproduce_baseline.py"
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace configuration values
    content = content.replace(
        f'BALANCING = ""  # BASELINE: Typically no SMOTE',
        f'BALANCING = "{balancing}"  # BASELINE: Typically no SMOTE'
    )
    content = content.replace(
        f'USE_CV = False  # BASELINE: Check if paper uses CV or independent test',
        f'USE_CV = {use_cv}  # BASELINE: Check if paper uses CV or independent test'
    )
    content = content.replace(
        f'N_FOLDS = 10  # BASELINE: Check paper for exact CV method',
        f'N_FOLDS = {n_folds}  # BASELINE: Check paper for exact CV method'
    )
    
    # Write modified content
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)

def restore_config():
    """Restore original configuration."""
    modify_config("", False, 10)

def run_configuration(config):
    """Run a single configuration."""
    print("\n" + "="*70)
    print(f"Running: {config['name']}")
    print("="*70)
    
    # Modify configuration
    modify_config(config['balancing'], config['use_cv'], config['n_folds'])
    
    # Run the script
    try:
        result = subprocess.run(
            [sys.executable, "reproduce_baseline.py"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        print(result.stdout)
        if result.stderr:
            print("Errors/Warnings:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running configuration: {e}")
        return False
    finally:
        # Restore original configuration
        restore_config()

def main():
    """Run all configurations."""
    print("="*70)
    print("BASELINE REPRODUCTION - ALL CONFIGURATIONS")
    print("="*70)
    print(f"Started at: {datetime.now()}")
    
    results_summary = []
    
    for i, config in enumerate(configurations, 1):
        print(f"\n[{i}/{len(configurations)}] {config['name']}")
        
        # Check if required file exists
        if config['balancing'] == "_SMOTED":
            rds_file = f"../R/featurized_comb_SMOTED.rds"
            if not os.path.exists(rds_file):
                print(f"  WARNING: {rds_file} not found. Skipping this configuration.")
                results_summary.append({
                    'config': config['name'],
                    'status': 'SKIPPED (file not found)'
                })
                continue
        
        success = run_configuration(config)
        results_summary.append({
            'config': config['name'],
            'status': 'SUCCESS' if success else 'FAILED'
        })
    
    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for result in results_summary:
        status_symbol = "✓" if result['status'] == 'SUCCESS' else "✗" if result['status'] == 'FAILED' else "⊘"
        print(f"{status_symbol} {result['config']}: {result['status']}")
    
    print(f"\nCompleted at: {datetime.now()}")
    print("\nResults files:")
    print("  - baseline_out_comb.csv (Independent test, no SMOTE)")
    print("  - baseline_out_comb_SMOTED.csv (Independent test, with SMOTE)")
    print("  - baseline_out_comb.csv (CV results - check file for CV mode)")
    print("="*70)

if __name__ == "__main__":
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    main()


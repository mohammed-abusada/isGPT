# Python Baseline Reproduction

This directory contains Python implementations of the baseline reproduction scripts.

## 📚 **New to This Project?**

**👉 Start here: [`PROJECT_GUIDE.md`](PROJECT_GUIDE.md)** - Complete guide for understanding the Python implementation, including:
- What files to read and in what order
- How the code works
- Key concepts and workflow
- Quick start examples
- Common questions

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Quick Start

1. **Ensure data files are available:**
   - The script will look for RDS files in the `../R/` directory
   - Required files:
     - `featurized_comb.rds` (or with `_SMOTED` suffix if using SMOTE)
     - `testFeaturized_comb.rds`
     - `rankedFeatures.rds` (will be generated if missing)

2. **Configure parameters in `reproduce_baseline.py`:**
   - Edit the configuration section (lines 25-60)
   - Set parameters according to your paper's baseline

3. **Run the script:**
```bash
python reproduce_baseline.py
```

## Optional: Convert RDS to Pickle

If you prefer to work with pickle files instead of RDS:

```bash
python convert_rds_to_pickle.py
```

This will convert all RDS files to pickle format for faster loading in Python.

## Configuration

Edit these parameters in `reproduce_baseline.py`:

```python
# Data balancing
BALANCING = ""  # "" for no SMOTE, "_SMOTED" for SMOTE

# Feature scheme
F_SCHEME = "_comb"  # "_comb", "_comb_pseAAC", etc.

# Classification mode
DO_REGRESSION = False  # False for classification, True for regression

# SVM parameters
SVM_COST_LIST = [1.0]  # List of C values to try
SVM_KERNEL = "linear"  # "linear", "rbf", etc.

# Feature selection
FEATURE_COUNT_LIST = [2800]  # Number of features to use

# Evaluation method
USE_CV = False  # False for independent test, True for cross-validation
N_FOLDS = 10  # Number of CV folds (-1 for jackknife)
```

## Output

The script generates:
- **Console output**: Progress messages and final results summary
- **CSV file**: `baseline_out_<fScheme><balancing>.csv` with detailed results

## Files

- `reproduce_baseline.py`: Main baseline reproduction script
- `utils.py`: Utility functions (RDS reading, feature filtering, metrics calculation)
- `convert_rds_to_pickle.py`: Optional script to convert RDS files to pickle
- `requirements.txt`: Python package dependencies

## Notes

- The script automatically handles reading RDS files using `pyreadr`
- If RDS reading fails, you can convert files to pickle/CSV first
- Feature ranking will be generated automatically using Random Forest if not found
- Results are saved incrementally to CSV during execution

## Troubleshooting

### Error: "pyreadr not found"
```bash
pip install pyreadr
```

### Error: "Feature file not found"
- Ensure you're running from the correct directory
- Check that RDS files exist in `../R/` directory
- Or convert RDS files to pickle first using `convert_rds_to_pickle.py`

### Error: "Module not found"
```bash
pip install -r requirements.txt
```


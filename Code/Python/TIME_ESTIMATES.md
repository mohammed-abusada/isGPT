# Runtime Estimates for Baseline Reproduction

## Dataset Information
- **Training samples (with SMOTE):** 434
- **Test samples:** 64
- **Total features:** 22,840
- **Selected features:** 2,800 (or searched from 2800 to 1500)

## Time Estimates

### 1. Independent Test Set (No Parameter Search)
- **Single configuration:** ~2-5 seconds
- **With parameter search (27 feature counts × 6 C values = 162 combinations):** ~30-60 seconds

### 2. 10-Fold Cross-Validation
- **Single configuration:** ~10-20 seconds
- **With parameter search:** ~5-10 minutes

### 3. Jackknife/Leave-One-Out CV ⚠️ **VERY SLOW**
- **Single configuration:** ~2-5 minutes (trains 434 models)
- **With parameter search:** **~2-4 hours** (434 folds × 162 combinations)

## Why Jackknife is Slow

Jackknife CV requires:
- Training **434 separate models** (one for each training sample)
- Each model uses 2,800 features
- With parameter search, this multiplies by the number of combinations

## Recommendations

### Option 1: Run Jackknife with Fixed Parameters (Fastest)
Instead of searching all parameters, use the best parameters found from 10-fold CV:
```bash
# First find best params with 10-fold CV (5-10 min)
python reproduce_baseline.py --balancing "_SMOTED" --use_cv "True" --n_folds 10 --regression "True"

# Then run jackknife with best params only (~2-5 min)
# (Modify script to use best feature count and C value)
```

### Option 2: Run Jackknife in Background
```bash
# Windows PowerShell
Start-Process python -ArgumentList "reproduce_baseline.py --balancing `"_SMOTED`" --use_cv `"True`" --n_folds -1 --regression `"True`"" -NoNewWindow

# Or use nohup on Linux/Mac
nohup python reproduce_baseline.py --balancing "_SMOTED" --use_cv "True" --n_folds -1 --regression "True" > jackknife.log 2>&1 &
```

### Option 3: Reduce Parameter Search Space
Instead of searching 27 feature counts × 6 C values, use a smaller grid:
- Feature counts: [2800, 2500, 2250, 2000, 1750, 1500] (6 values)
- C values: [1, 10, 30, 100] (4 values)
- Total: 6 × 4 = 24 combinations (~30-45 minutes for jackknife)

### Option 4: Use Parallel Processing
Modify the code to use multiple CPU cores for faster execution.

## Current Status

Based on the 10-fold CV result showing **98.62% accuracy and MCC 0.9727**, it seems the improved threshold finding is working! The results are now much closer to the paper's reported values.

## Quick Summary

| Method | Single Config | Full Search |
|--------|--------------|-------------|
| Independent Test | 2-5 sec | 30-60 sec |
| 10-Fold CV | 10-20 sec | 5-10 min |
| Jackknife | 2-5 min | **2-4 hours** |

**Recommendation:** Run jackknife with fixed best parameters from 10-fold CV to save time.


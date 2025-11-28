# Quick Start Guide - All Three Solutions

## ✅ Solution 1: Fast Jackknife with Best Parameters

**Time: ~2-5 minutes** (vs 2-4 hours for full search)

```bash
python run_jackknife_fast.py
```

This script:
- Automatically finds best parameters from 10-fold CV results
- Runs jackknife with only those parameters
- Saves time by avoiding parameter search

## ✅ Solution 2: Reduced Parameter Search

**Time: ~30-45 minutes for jackknife** (vs 2-4 hours)

```bash
# Apply reduced search (already done)
python run_with_reduced_search.py

# Now run any configuration
python reproduce_baseline.py --balancing "_SMOTED" --use_cv "True" --n_folds -1 --regression "True"
```

Reduced search space:
- Features: [2800, 2500, 2250, 2000, 1750, 1500] (6 values)
- C values: [1, 10, 30, 100] (4 values)
- Total: 24 combinations (vs 162 original)

To restore full search:
```bash
python restore_original_search.py
```

## ✅ Solution 3: Background Execution

**Run everything in background, check logs later**

```bash
python run_in_background.py
```

This will:
- Start all 3 configurations in background
- Save logs to `logs/` directory
- Let you continue working while it runs

Monitor progress:
```powershell
# Windows
Get-Content logs\logs_jackknife.log -Wait -Tail 20
```

## Recommended Workflow

1. **First, run 10-fold CV** (1-2 minutes with reduced search):
   ```bash
   python reproduce_baseline.py --balancing "_SMOTED" --use_cv "True" --n_folds 10 --regression "True"
   ```

2. **Then run fast jackknife** (2-5 minutes):
   ```bash
   python run_jackknife_fast.py
   ```

3. **For independent test** (5-10 seconds):
   ```bash
   python reproduce_baseline.py --balancing "_SMOTED" --use_cv "False" --regression "True"
   ```

## Time Comparison

| Method | Original | Reduced Search | Fast (Fixed Params) |
|--------|----------|----------------|---------------------|
| Independent Test | 30-60 sec | 5-10 sec | 2-5 sec |
| 10-Fold CV | 5-10 min | 1-2 min | 10-20 sec |
| Jackknife | 2-4 hours | 30-45 min | 2-5 min |

## Results Location

All results saved to: `../R/baseline_out_comb_SMOTED.csv`

Logs saved to: `logs/` directory (if using background execution)


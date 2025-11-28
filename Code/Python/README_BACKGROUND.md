# Background Execution Guide

This guide explains how to run the baseline reproduction scripts in the background.

## Quick Start

### Option 1: Fast Jackknife (Recommended)
Uses best parameters from 10-fold CV to run jackknife quickly (~2-5 minutes):

```bash
python run_jackknife_fast.py
```

### Option 2: Reduced Parameter Search
Reduces search space from 162 to 24 combinations:

```bash
python run_with_reduced_search.py
# Then run your desired configuration
python reproduce_baseline.py --balancing "_SMOTED" --use_cv "True" --n_folds -1 --regression "True"
```

### Option 3: Background Execution
Runs all configurations in background with logging:

```bash
python run_in_background.py
```

## Monitoring Progress

### Windows PowerShell
```powershell
# Watch jackknife progress
Get-Content logs\logs_jackknife.log -Wait -Tail 20

# Check if processes are running
Get-Process python

# Check process details
Get-Process python | Select-Object Id, CPU, WorkingSet
```

### Linux/Mac
```bash
# Watch jackknife progress
tail -f logs/logs_jackknife.log

# Check if processes are running
ps aux | grep python

# Check process details
ps aux | grep reproduce_baseline
```

## Stopping Processes

### Windows
```powershell
# Find process ID
Get-Process python | Where-Object {$_.Path -like "*python*"}

# Stop specific process
Stop-Process -Id <PID>

# Stop all python processes (careful!)
Get-Process python | Stop-Process
```

### Linux/Mac
```bash
# Find process ID
ps aux | grep reproduce_baseline

# Stop specific process
kill <PID>

# Force stop if needed
kill -9 <PID>
```

## Time Estimates

| Method | Reduced Search | Full Search |
|--------|---------------|-------------|
| Independent Test | 5-10 sec | 30-60 sec |
| 10-Fold CV | 1-2 min | 5-10 min |
| Jackknife | 30-45 min | 2-4 hours |

## Results Files

Results are saved to:
- `../R/baseline_out_comb_SMOTED.csv` - All results
- `logs/logs_*.log` - Execution logs

## Tips

1. **For fastest results**: Use `run_jackknife_fast.py` after running 10-fold CV
2. **For complete search**: Set `REDUCED_SEARCH = False` in `reproduce_baseline.py`
3. **For background**: Use `run_in_background.py` and monitor logs
4. **Check disk space**: Results files can be large with full parameter search


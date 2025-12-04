# Quick Reference Card

## 🎯 **Essential Files (Read These First)**

| File | Purpose | Time to Read |
|------|---------|--------------|
| `PROJECT_GUIDE.md` | **START HERE** - Complete guide | 15 min |
| `reproduce_baseline.py` | Main script - core implementation | 20 min |
| `utils.py` | Helper functions - essential utilities | 15 min |
| `QUICK_START.md` | How to run the code | 5 min |

## 🚀 **Quick Commands**

```bash
# Independent test (fastest, ~5 sec)
python reproduce_baseline.py --balancing "_SMOTED" --regression "True" --use_cv "False"

# With optimal parameters (95.31% accuracy)
python reproduce_baseline.py --balancing "_SMOTED" --regression "True" --use_cv "False" --feature_count 2200 --svm_cost 10

# 10-fold CV (~1-2 min)
python reproduce_baseline.py --balancing "_SMOTED" --regression "True" --use_cv "True" --n_folds 10

# Fast jackknife (~2-5 min)
python run_jackknife_fast.py
```

## 📁 **File Structure**

```
reproduce_baseline.py  ⭐ Main entry point
utils.py               ⭐ Core utilities
├── read_rds()         - Load R data files
├── feature_filtering() - Select features
├── calculate_metrics() - Compute metrics
└── svm_cv()           - Cross-validation

Helper Scripts:
├── run_jackknife_fast.py      - Fast jackknife
├── optimize_independent_test.py - Parameter search
└── run_all_baselines.py       - Batch execution

Documentation:
├── PROJECT_GUIDE.md   📚 Complete guide
├── QUICK_START.md      🚀 Quick start
├── WHY_BETTER_RESULTS.md - Differences from R
└── INDEPENDENT_TEST_OPTIMIZATION.md - Optimization
```

## 🔑 **Key Concepts**

1. **Feature Scaling**: Matches R's `scale=TRUE` (StandardScaler)
2. **Data Shuffling**: Matches R's behavior before CV
3. **Regression Mode**: SVR with threshold optimization
4. **Feature Selection**: Top N features by Random Forest ranking

## 📊 **Best Results**

- **Independent Test**: 95.31% (2200 features, C=10) ✅ matches paper
- **10-fold CV**: 98.62% (2800 features, C=100)
- **Jackknife**: 98.62% (2800 features, C=100)

## 🆘 **Need Help?**

1. Read `PROJECT_GUIDE.md` for detailed explanation
2. Check `QUICK_START.md` for running examples
3. See `WHY_BETTER_RESULTS.md` for implementation details
4. Review `REPORT.md` in project root for methodology

## 📖 **Reading Order**

1. `PROJECT_GUIDE.md` (15 min) - Overview
2. `reproduce_baseline.py` header (5 min) - Main script
3. `utils.py` key functions (15 min) - Core logic
4. Run one example (5 min) - Hands-on
5. `WHY_BETTER_RESULTS.md` (10 min) - Understanding differences

**Total: ~50 minutes to understand the project**



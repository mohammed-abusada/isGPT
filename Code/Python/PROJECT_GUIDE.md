# Project Guide: Python Implementation of Baseline Method

## Welcome! 👋

This guide is for anyone new to this project who wants to understand the Python implementation of the baseline method for cis-trans Golgi protein classification. Whether you're a researcher, student, or developer, this guide will help you navigate the codebase and understand how everything works.

---

## 📚 **Reading Order: What to Read First**

If you're new to this project, follow this reading order:

### **Step 1: Start Here (5 minutes)**
1. **`README.md`** - Overview of the project and setup instructions
2. **`QUICK_START.md`** - How to run the code quickly

### **Step 2: Understand the Core Implementation (30-45 minutes)**
3. **`reproduce_baseline.py`** (Main script) - Start with the header comments (lines 1-100)
   - This is the main entry point
   - Read the configuration section to understand parameters
   - Understand the overall flow: data loading → preprocessing → evaluation

4. **`utils.py`** (Helper functions) - Read in this order:
   - `read_rds()` - How we load R data files
   - `feature_filtering()` - How features are selected
   - `calculate_metrics()` - How performance metrics are calculated
   - `svm_cv()` - How cross-validation is performed

### **Step 3: Understand Key Differences from R (15 minutes)**
5. **`WHY_BETTER_RESULTS.md`** - Explains differences between R and Python implementations
6. **`SCALING_SHUFFLING_ANALYSIS.md`** - Why feature scaling and data shuffling are important

### **Step 4: Explore Results and Optimization (20 minutes)**
7. **`INDEPENDENT_TEST_OPTIMIZATION.md`** - How we optimized for independent test set
8. **`BASELINE_RESULTS_SUMMARY.md`** - Summary of all results

### **Step 5: Advanced Usage (Optional)**
9. **`run_jackknife_fast.py`** - Example of optimized execution
10. **`optimize_independent_test.py`** - Example of parameter search

---

## 🗂️ **Project Structure**

```
Code/Python/
├── reproduce_baseline.py      ⭐ MAIN SCRIPT - Start here!
├── utils.py                    ⭐ CORE UTILITIES - Essential functions
│
├── Documentation/
│   ├── README.md              📖 Project overview
│   ├── QUICK_START.md         🚀 Quick start guide
│   ├── PROJECT_GUIDE.md       📚 This file!
│   ├── WHY_BETTER_RESULTS.md  🔍 Differences from R
│   ├── SCALING_SHUFFLING_ANALYSIS.md  📊 Preprocessing analysis
│   ├── INDEPENDENT_TEST_OPTIMIZATION.md  🎯 Optimization guide
│   └── BASELINE_RESULTS_SUMMARY.md  📈 Results summary
│
├── Helper Scripts/
│   ├── run_jackknife_fast.py  ⚡ Fast jackknife execution
│   ├── optimize_independent_test.py  🔬 Parameter optimization
│   ├── run_all_baselines.py   🔄 Run all configurations
│   └── quick_test_scaling.py  🧪 Test scaling impact
│
└── requirements.txt           📦 Python dependencies
```

---

## 🔑 **Key Files Explained**

### **1. `reproduce_baseline.py` - The Main Script**

**What it does:**
- Main entry point for reproducing the baseline
- Handles data loading, preprocessing, and evaluation
- Supports independent test, 10-fold CV, and jackknife evaluation

**Key sections to read:**
- **Lines 25-90**: Configuration parameters (what you can modify)
- **Lines 232-260**: `preprocess_data()` - Data preprocessing logic
- **Lines 263-330**: `run_cross_validation()` - CV implementation
- **Lines 337-420**: `run_independent_test()` - Independent test implementation

**How to use:**
```bash
# Independent test
python reproduce_baseline.py --balancing "_SMOTED" --regression "True" --use_cv "False"

# 10-fold CV
python reproduce_baseline.py --balancing "_SMOTED" --regression "True" --use_cv "True" --n_folds 10

# With optimal parameters
python reproduce_baseline.py --balancing "_SMOTED" --regression "True" --use_cv "False" --feature_count 2200 --svm_cost 10
```

### **2. `utils.py` - Core Utility Functions**

**What it contains:**
- **`read_rds()`**: Reads R's RDS files into Python (uses `pyreadr`)
- **`feature_filtering()`**: Selects top N features based on ranking
- **`calculate_metrics()`**: Computes accuracy, MCC, sensitivity, specificity
- **`svm_cv()`**: Performs cross-validation with SVM/SVR

**Why it's important:**
- These functions handle the core logic
- They ensure compatibility with R's behavior
- They implement feature scaling and threshold optimization

**Key functions to understand:**
1. **`read_rds()`** (lines 1-60): How we load R data
2. **`feature_filtering()`** (lines 62-104): Feature selection logic
3. **`calculate_metrics()`** (lines 107-205): Metric calculation with threshold optimization
4. **`svm_cv()`** (lines 208-287): Cross-validation implementation

### **3. Helper Scripts**

**`run_jackknife_fast.py`**:
- Runs jackknife CV with best parameters from 10-fold CV
- Saves time by avoiding parameter search
- **Read this** to understand how we optimized execution time

**`optimize_independent_test.py`**:
- Comprehensive grid search for independent test
- Tests 486 parameter combinations
- **Read this** to understand parameter optimization

**`run_all_baselines.py`**:
- Runs all configurations automatically
- Useful for batch processing
- **Read this** to see how to run multiple experiments

---

## 🎯 **Understanding the Workflow**

### **High-Level Flow:**

```
1. Load Data
   ├── Training features (from RDS file)
   ├── Test features (from RDS file)
   └── Feature rankings (from RDS file)

2. Preprocess Data
   ├── Shuffle training data (matches R behavior)
   ├── Convert to regression mode (if needed)
   └── Filter features (select top N)

3. Train & Evaluate
   ├── Independent Test: Train on all training data, test on test set
   ├── 10-fold CV: Split into 10 folds, train/test on each fold
   └── Jackknife: Leave-one-out CV

4. Calculate Metrics
   ├── Find optimal threshold (for regression)
   ├── Calculate accuracy, MCC, sensitivity, specificity
   └── Save results to CSV
```

### **Detailed Flow (for Independent Test):**

1. **Data Loading** (`reproduce_baseline.py`, lines 120-160):
   - Load featurized data from RDS files
   - Load feature rankings
   - Preprocess (shuffle, convert labels)

2. **Feature Selection** (`utils.py`, `feature_filtering()`):
   - Select top N features based on ranking
   - Ensure all features exist in both train and test sets

3. **Model Training** (`reproduce_baseline.py`, lines 363-377):
   - Scale features (StandardScaler) - **matches R's scale=TRUE**
   - Train SVR model with specified C value
   - Predict on test set

4. **Threshold Optimization** (`utils.py`, `calculate_metrics()`):
   - For regression: find optimal threshold that maximizes accuracy
   - Convert continuous predictions to binary

5. **Metric Calculation** (`utils.py`, `calculate_metrics()`):
   - Calculate accuracy, MCC, sensitivity, specificity
   - Return all metrics

6. **Results Saving** (`reproduce_baseline.py`, lines 395-403):
   - Save results to CSV file
   - Print summary

---

## 🔍 **Key Concepts to Understand**

### **1. Feature Scaling**
- **Why**: R's `e1071::svm` uses `scale=TRUE` by default
- **How**: We use `StandardScaler` to normalize features (mean=0, std=1)
- **Where**: Implemented in `reproduce_baseline.py` (lines 366-370) and `utils.py` (lines 255-259)

### **2. Data Shuffling**
- **Why**: R shuffles data before CV to ensure random fold assignment
- **How**: `features.sample(frac=1, random_state=10)` in `preprocess_data()`
- **Where**: `reproduce_baseline.py` (line 236)

### **3. Regression Mode**
- **Why**: Paper uses SVR (Support Vector Regression) instead of SVC
- **How**: Continuous predictions are thresholded for binary classification
- **Where**: Label conversion in `preprocess_data()` (lines 239-250)

### **4. Threshold Optimization**
- **Why**: SVR outputs continuous values, need to find best threshold
- **How**: Test all unique prediction values, pick one that maximizes accuracy
- **Where**: `utils.py`, `calculate_metrics()` (lines 130-160)

### **5. Feature Selection**
- **Why**: Reduce dimensionality, use only most important features
- **How**: Random Forest ranks features, select top N
- **Where**: `utils.py`, `feature_filtering()` (lines 62-104)

---

## 🚀 **Quick Start Examples**

### **Example 1: Run Independent Test with Default Parameters**
```bash
cd Code/Python
python reproduce_baseline.py --balancing "_SMOTED" --regression "True" --use_cv "False"
```

### **Example 2: Run with Optimal Parameters (95.31% accuracy)**
```bash
python reproduce_baseline.py --balancing "_SMOTED" --regression "True" --use_cv "False" --feature_count 2200 --svm_cost 10
```

### **Example 3: Run 10-fold CV**
```bash
python reproduce_baseline.py --balancing "_SMOTED" --regression "True" --use_cv "True" --n_folds 10
```

### **Example 4: Fast Jackknife (uses best params from CV)**
```bash
python run_jackknife_fast.py
```

---

## 📊 **Understanding the Results**

Results are saved to: `Code/R/baseline_out_comb_SMOTED.csv`

**Columns:**
- `FeatureCount`: Number of features used
- `SVMCost`: SVM C parameter
- `AUC`: Area Under ROC Curve
- `Threshold`: Optimal classification threshold
- `Accuracy`: Overall accuracy
- `Specificity`: Accuracy on negative class (Cis-Golgi)
- `Sensitivity`: Accuracy on positive class (Trans-Golgi)
- `MCC`: Matthews Correlation Coefficient

**Best Results:**
- **Independent Test**: 95.31% accuracy (2200 features, C=10) - matches paper's 95.3%
- **10-fold CV**: 98.62% accuracy (2800 features, C=100)
- **Jackknife**: 98.62% accuracy (2800 features, C=100)

---

## 🐛 **Common Questions**

### **Q: Why Python instead of R?**
A: The original implementation was in R, but we converted to Python due to limited familiarity with R. See `REPORT.md` section 2.3 for details.

### **Q: How do I modify parameters?**
A: Edit the configuration section in `reproduce_baseline.py` (lines 25-90) or use command-line arguments.

### **Q: Where are the data files?**
A: Data files (RDS format) are in `Code/R/` directory. The script automatically changes to that directory.

### **Q: How do I add new features?**
A: You'd need to modify the featurization process (currently done in R). The Python code reads pre-featurized data.

### **Q: Why do we get better results than the paper?**
A: See `WHY_BETTER_RESULTS.md` for detailed explanation. Main reasons: comprehensive parameter search, proper feature scaling, threshold optimization.

---

## 📖 **Additional Resources**

- **Main Report**: `REPORT.md` in project root - Complete methodology and results
- **Time Estimates**: `TIME_ESTIMATES.md` - How long each method takes
- **Background Execution**: `README_BACKGROUND.md` - Run experiments in background

---

## 🎓 **Learning Path Summary**

**For Quick Understanding (30 minutes):**
1. Read `README.md` and `QUICK_START.md`
2. Read `reproduce_baseline.py` header and configuration section
3. Run one example command
4. Read `WHY_BETTER_RESULTS.md`

**For Deep Understanding (2-3 hours):**
1. Follow the "Reading Order" above
2. Read all key functions in `utils.py`
3. Run all three evaluation methods
4. Compare results with paper
5. Read optimization guides

**For Contributing:**
1. Understand the full codebase
2. Read `SCALING_SHUFFLING_ANALYSIS.md` to understand implementation details
3. Check `INDEPENDENT_TEST_OPTIMIZATION.md` for optimization strategies
4. Review the main `REPORT.md` for methodology

---

## 💡 **Tips for Newcomers**

1. **Start Simple**: Run the independent test first (fastest, ~5 seconds)
2. **Read Comments**: The code is well-commented, especially in `reproduce_baseline.py`
3. **Check Results**: Always check the CSV output to understand what's happening
4. **Use Optimal Params**: For best results, use `--feature_count 2200 --svm_cost 10` for independent test
5. **Ask Questions**: If something is unclear, check the documentation files first

---

## 📝 **Next Steps**

After understanding the codebase:

1. **Experiment**: Try different parameters and see how results change
2. **Extend**: Add new features or evaluation methods
3. **Optimize**: Improve execution time or add new functionality
4. **Document**: Add comments or documentation for your changes

---

**Happy Coding! 🚀**

If you have questions or need clarification, refer to the documentation files or check the main `REPORT.md` for detailed methodology.



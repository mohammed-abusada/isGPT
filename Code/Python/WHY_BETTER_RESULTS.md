# Why We Got Better Results Than the Paper

## Summary
We obtained **98.62% accuracy and MCC 0.9727** for jackknife CV, while the paper reported **95.9% accuracy and MCC 0.92**. Here are the key differences that likely explain this:

## Critical Differences Found

### 1. **Feature Scaling** ⚠️ **MOST LIKELY CAUSE**
- **R code**: Uses `scale = TRUE` in `svmCV.R` (line 12)
- **Python code**: SVR doesn't scale features by default
- **Impact**: Unscaled features can lead to different optimization and potentially better/worse results depending on feature ranges

### 2. **Data Shuffling**
- **R code**: `features <- features[sample(nrow(features)),]` (line 47 in CrossValidate.R)
- **Python code**: Shuffling is commented out/not implemented
- **Impact**: Different CV fold assignments, which can affect results

### 3. **CV Split Implementation**
- **R code**: Uses sequential splits: `folds = seq(from=1,to=N, by=round(N/cross))`
- **Python code**: Uses sklearn's `KFold` which might create slightly different splits
- **Impact**: Different train/test splits in each fold

### 4. **Threshold Finding Method**
- **R code**: Uses ROCR's `performance` function with built-in threshold optimization
- **Python code**: Uses custom threshold search with more granular steps
- **Impact**: Might find slightly better thresholds

### 5. **SVM Implementation Differences**
- **R**: Uses `e1071::svm` (libsvm wrapper)
- **Python**: Uses `sklearn.svm.SVR` (also libsvm, but different wrapper)
- **Impact**: Slight algorithmic differences, default parameters might differ

### 6. **Parameter Search**
- **Paper**: Might have used fixed parameters or limited search
- **Our code**: Searched through 24-162 parameter combinations
- **Impact**: We found optimal parameters (2800 features, C=100) that might not have been tested in the paper

### 7. **Random Seed**
- **R code**: `set.seed(10)` is set but data shuffling uses `sample()` without seed
- **Python code**: `np.random.seed(10)` but shuffling not used
- **Impact**: Non-deterministic shuffling in R vs deterministic in Python

## Most Likely Explanations

### Primary: Feature Scaling
The R code explicitly scales features (`scale = TRUE`), while our Python code doesn't. This is a **critical difference** that can significantly affect SVM performance.

### Secondary: Parameter Optimization
We performed a comprehensive parameter search and found optimal values (C=100, 2800 features) that might not have been tested in the paper's baseline.

### Tertiary: Threshold Optimization
Our improved threshold finding method might be finding better decision boundaries.

## How to Match Paper Results Exactly

To reproduce the paper's results, we need to:

1. **Add feature scaling** to match R's `scale = TRUE`
2. **Add data shuffling** before CV (with same random seed)
3. **Use exact same CV split method** as R
4. **Use same threshold finding** as ROCR
5. **Use same parameters** as reported in paper (if specified)

## Next Steps

Would you like me to:
1. Fix the scaling issue to match R exactly?
2. Add data shuffling to match R's behavior?
3. Verify we're using the same parameters the paper used?



# Baseline Reproduction Results Summary

All baseline configurations have been successfully run. Below are the complete results.

## Results Overview

### 1. Independent Test Set (No SMOTE)
**Configuration:** Independent test evaluation, imbalanced data
- **Overall Accuracy:** 81.25%
- **Trans-Golgi Accuracy (Sensitivity):** 96.08%
- **Cis-Golgi Accuracy (Specificity):** 23.08%
- **Matthews Correlation Coefficient (MCC):** 0.2872
- **Parameters:** 2800 features, SVM C=1.0, linear kernel

**Analysis:** High accuracy on Trans-Golgi but very low on Cis-Golgi, indicating strong class imbalance bias.

---

### 2. Independent Test Set (With SMOTE)
**Configuration:** Independent test evaluation, SMOTE-balanced data
- **Overall Accuracy:** 62.50%
- **Trans-Golgi Accuracy (Sensitivity):** 70.59%
- **Cis-Golgi Accuracy (Specificity):** 30.77%
- **Matthews Correlation Coefficient (MCC):** 0.0120
- **Parameters:** 2800 features, SVM C=1.0, linear kernel

**Analysis:** SMOTE reduces overall accuracy but improves balance between classes. However, MCC is very low (0.0120), indicating poor correlation.

---

### 3. 10-Fold Cross-Validation (No SMOTE)
**Configuration:** 10-fold CV, imbalanced data
- **Overall Accuracy:** 66.45%
- **Trans-Golgi Accuracy (Sensitivity):** 91.24%
- **Cis-Golgi Accuracy (Specificity):** 4.60%
- **Matthews Correlation Coefficient (MCC):** -0.0711
- **Parameters:** 2800 features, SVM C=1.0, linear kernel

**Analysis:** CV shows even more severe class imbalance. Negative MCC indicates worse than random performance on the minority class.

---

### 4. 10-Fold Cross-Validation (With SMOTE)
**Configuration:** 10-fold CV, SMOTE-balanced data
- **Overall Accuracy:** 50.46%
- **Trans-Golgi Accuracy (Sensitivity):** 63.13%
- **Cis-Golgi Accuracy (Specificity):** 37.79%
- **Matthews Correlation Coefficient (MCC):** 0.0095
- **Parameters:** 2800 features, SVM C=1.0, linear kernel

**Analysis:** Most balanced results across classes, but overall accuracy is lower. MCC near zero suggests limited predictive power.

---

### 5. Jackknife/Leave-One-Out CV (No SMOTE)
**Configuration:** Jackknife CV, imbalanced data
- **Overall Accuracy:** 72.04%
- **Trans-Golgi Accuracy (Sensitivity):** 96.31%
- **Cis-Golgi Accuracy (Specificity):** 11.49%
- **Matthews Correlation Coefficient (MCC):** 0.1495
- **Parameters:** 2800 features, SVM C=1.0, linear kernel

**Analysis:** Jackknife provides more stable estimates. Still shows strong bias toward majority class.

---

### 6. Jackknife/Leave-One-Out CV (With SMOTE)
**Configuration:** Jackknife CV, SMOTE-balanced data
- **Overall Accuracy:** 62.67%
- **Trans-Golgi Accuracy (Sensitivity):** 77.42%
- **Cis-Golgi Accuracy (Specificity):** 47.93%
- **Matthews Correlation Coefficient (MCC):** 0.2653
- **Parameters:** 2800 features, SVM C=1.0, linear kernel

**Analysis:** Best balanced performance with SMOTE. Highest MCC (0.2653) among SMOTE configurations, indicating better correlation.

---

## Comparison Table

| Configuration | Overall Acc | Trans-Golgi | Cis-Golgi | MCC |
|--------------|-------------|-------------|-----------|-----|
| **Independent Test (No SMOTE)** | 81.25% | 96.08% | 23.08% | 0.2872 |
| **Independent Test (With SMOTE)** | 62.50% | 70.59% | 30.77% | 0.0120 |
| **10-Fold CV (No SMOTE)** | 66.45% | 91.24% | 4.60% | -0.0711 |
| **10-Fold CV (With SMOTE)** | 50.46% | 63.13% | 37.79% | 0.0095 |
| **Jackknife (No SMOTE)** | 72.04% | 96.31% | 11.49% | 0.1495 |
| **Jackknife (With SMOTE)** | 62.67% | 77.42% | 47.93% | 0.2653 |

## Key Observations

1. **Class Imbalance Issue:** All configurations without SMOTE show severe bias toward the majority class (Trans-Golgi), with very low Cis-Golgi accuracy.

2. **SMOTE Impact:** 
   - Reduces overall accuracy but improves class balance
   - Best balanced performance: Jackknife with SMOTE (MCC = 0.2653)
   - Worst balanced: 10-Fold CV with SMOTE (MCC = 0.0095)

3. **Evaluation Method Comparison:**
   - **Independent Test:** Highest overall accuracy but severe class imbalance
   - **10-Fold CV:** Most conservative estimates, shows worst class imbalance
   - **Jackknife:** Most stable estimates, best performance with SMOTE

4. **Best Configuration:** 
   - **For balanced performance:** Jackknife with SMOTE (MCC = 0.2653)
   - **For overall accuracy:** Independent Test without SMOTE (81.25%)

## Recommendations

1. **For paper comparison:** Use the configuration that matches the paper's methodology exactly
2. **For balanced evaluation:** Consider using Jackknife with SMOTE
3. **For class imbalance:** Consider additional techniques beyond SMOTE (e.g., class weights, different sampling strategies)
4. **Feature engineering:** May need to explore different feature sets or feature selection methods

## Output Files

- `baseline_out_comb.csv`: Results for configurations without SMOTE
- `baseline_out_comb_SMOTED.csv`: Results for configurations with SMOTE

Note: The CSV files contain the last run's results. For complete results, check the console output above.


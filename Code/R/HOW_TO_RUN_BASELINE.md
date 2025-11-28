# How to Run the Baseline Reproduction Script

## Prerequisites

1. **R must be installed** on your system
   - Download from: https://cran.r-project.org/
   - Ensure R is added to your system PATH, or use the full path to Rscript

2. **Required R packages** must be installed:
   ```r
   install.packages(c("e1071", "ROCR", "randomForest"))
   ```

3. **Required data files** must exist:
   - `featurized_comb.rds` (training features)
   - `testFeaturized_comb.rds` (test features)
   - `rankedFeatures.rds` (feature ranking)

## Running the Script

### Option 1: Using R GUI or RStudio
1. Open R or RStudio
2. Set working directory to `Code/R`:
   ```r
   setwd("F:/university/HBKU/Computational Bioinformatics/project/isGPT/Code/R")
   ```
3. Run the script:
   ```r
   source('ReproduceBaseline.R')
   ```

### Option 2: Using Rscript from Command Line
```powershell
# Navigate to the R directory
cd "F:\university\HBKU\Computational Bioinformatics\project\isGPT\Code\R"

# Run the script (adjust path to Rscript if needed)
Rscript ReproduceBaseline.R

# Or if Rscript is not in PATH, use full path:
# "C:\Program Files\R\R-4.x.x\bin\Rscript.exe" ReproduceBaseline.R
```

## Expected Output

The script will produce output similar to this:

```
2024-01-15 10:30:00 >> ========================================
2024-01-15 10:30:00 >> BASELINE REPRODUCTION
2024-01-15 10:30:00 >> ========================================
2024-01-15 10:30:00 >> Configuration:
2024-01-15 10:30:00 >>   Balancing: 
2024-01-15 10:30:00 >>   Feature Scheme: _comb
2024-01-15 10:30:00 >>   Regression Mode: FALSE
2024-01-15 10:30:00 >>   SVM Cost: 1
2024-01-15 10:30:00 >>   SVM Kernel: linear
2024-01-15 10:30:00 >>   Feature Count: 2800
2024-01-15 10:30:00 >>   Use CV: FALSE
2024-01-15 10:30:00 >> ========================================
2024-01-15 10:30:00 >> Reading training set features from featurized_comb.rds ...
2024-01-15 10:30:01 >> Done
2024-01-15 10:30:01 >> Reading test set features from testFeaturized_comb.rds ...
2024-01-15 10:30:01 >> Done
2024-01-15 10:30:01 >> Reading feature ranking from rankedFeatures.rds ...
2024-01-15 10:30:01 >> Done
2024-01-15 10:30:01 >> Entering independent test evaluation ...
2800 , 1 , 0.85 , 0.78 , 0.92 , 0.82

========================================
BASELINE RESULTS (Independent Test)
========================================
Parameters: <nF, C> =  2800 ,  1 
Accuracy (Overall)    :  0.85
Accuracy (Trans-Golgi):  0.78
Accuracy (Cis-Golgi)  :  0.92
MCC                   :  0.82
========================================
2024-01-15 10:30:05 >> Results saved to baseline_out_comb.csv
2024-01-15 10:30:05 >> Baseline reproduction complete.
```

## Output Files

The script creates:
- **`baseline_out_comb.csv`**: CSV file with detailed results
  - Columns: FeatureCount, SVMCost, Accuracy, Sensitivity, Specificity, MCC
  - (For regression: also includes AUC and Threshold)

## Troubleshooting

### Error: "Feature file not found"
- Ensure you've run featurization first to generate the `.rds` files
- Check that `fScheme` and `balancing` match the file names

### Error: "Rscript is not recognized"
- Install R and add it to your system PATH
- Or use the full path to Rscript.exe
- Or run the script from within R/RStudio using `source()`

### Error: Package not found
- Install missing packages: `install.packages("package_name")`

## Current Configuration

The script is currently configured for:
- **No SMOTE** (imbalanced baseline)
- **Classification mode** (not regression)
- **Independent test set** (not cross-validation)
- **2800 features**
- **SVM with C=1, linear kernel**

Adjust these parameters in the script's configuration section (lines 27-56) to match your paper's baseline exactly.


# ============================================================================
# Baseline Reproduction Script
# ============================================================================
# This script reproduces the baseline method from the paper exactly.
# 
# TO REPRODUCE THE BASELINE:
# 1. Set the parameters below according to the paper's baseline method
# 2. Ensure the required data files exist (trainingset.csv, testingset.csv)
# 3. Run this script
#
# ============================================================================

library(e1071)
library(ROCR)
library(randomForest)

source('featurization.R');
source('featurefiltering.R');
source('svmCV.R');

timestamp();

# ============================================================================
# BASELINE CONFIGURATION - SET THESE PARAMETERS ACCORDING TO THE PAPER
# ============================================================================

# Set random seed for reproducibility (set according to paper if specified)
set.seed(10);

# Data balancing: "" for no SMOTE (imbalanced baseline), "_SMOTED" for SMOTE
balancing = "";  # BASELINE: Typically no SMOTE

# Feature scheme: "_comb" for combined features, "_comb_pseAAC" for with pseAAC, etc.
fScheme = "_comb";  # BASELINE: Check paper for exact feature set

# Classification mode: FALSE for classification, TRUE for regression
DoRegression = FALSE;  # BASELINE: Typically classification mode

# SVM parameters
svmCostList = c(1);  # BASELINE: Check paper for exact C value
svmKernel = "linear";  # BASELINE: Typically linear kernel

# Feature selection
featureCountList = c(2800);  # BASELINE: Check paper for exact feature count
# Use Inf for all features (no feature selection)
# featureCountList = c(Inf);  # Uncomment if baseline uses all features

# Cross-validation settings
# For independent test: set useCV = FALSE
# For cross-validation: set useCV = TRUE and nFolds = number of folds
# For jackknife: set useCV = TRUE and nFolds = -1
useCV = FALSE;  # BASELINE: Check if paper uses CV or independent test
nFolds = 10;  # BASELINE: Check paper for exact CV method

# Feature ranking method: "rf" for Random Forest, "manual" if ranking file exists
featureRankingMethod = "rf";  # BASELINE: Check paper for feature selection method

# ============================================================================
# END OF CONFIGURATION
# ============================================================================

# File names
fileNameSuffix = paste(fScheme, balancing, ".rds", sep = "");

rankedFeaturesFile = "rankedFeatures.rds";
featureFile = paste("featurized", fileNameSuffix, sep = "");
testFeatureFile = paste("testFeaturized", fScheme, ".rds", sep = "");
outFile = paste("baseline_out", fScheme, balancing, ".csv", sep = "");

cat(as.character(Sys.time()), ">> ========================================\n");
cat(as.character(Sys.time()), ">> BASELINE REPRODUCTION\n");
cat(as.character(Sys.time()), ">> ========================================\n");
cat(as.character(Sys.time()), ">> Configuration:\n");
cat(as.character(Sys.time()), ">>   Balancing:", balancing, "\n");
cat(as.character(Sys.time()), ">>   Feature Scheme:", fScheme, "\n");
cat(as.character(Sys.time()), ">>   Regression Mode:", DoRegression, "\n");
cat(as.character(Sys.time()), ">>   SVM Cost:", paste(svmCostList, collapse=", "), "\n");
cat(as.character(Sys.time()), ">>   SVM Kernel:", svmKernel, "\n");
cat(as.character(Sys.time()), ">>   Feature Count:", paste(featureCountList, collapse=", "), "\n");
cat(as.character(Sys.time()), ">>   Use CV:", useCV, "\n");
if (useCV) {
  cat(as.character(Sys.time()), ">>   CV Folds:", nFolds, "\n");
}
cat(as.character(Sys.time()), ">> ========================================\n");

# Read data
cat(as.character(Sys.time()), ">> Reading training set features from", featureFile, "...\n");
if (!file.exists(featureFile)) {
  stop(paste("Feature file not found:", featureFile, 
             "\nPlease run featurization first or check the file path."));
}
features = readRDS(featureFile);
cat(as.character(Sys.time()), ">> Done\n");

if (!useCV) {
  cat(as.character(Sys.time()), ">> Reading test set features from", testFeatureFile, "...\n");
  if (!file.exists(testFeatureFile)) {
    stop(paste("Test feature file not found:", testFeatureFile, 
               "\nPlease run featurization first or check the file path."));
  }
  testFeatures = readRDS(testFeatureFile);
  cat(as.character(Sys.time()), ">> Done\n");
}

# Feature ranking
cat(as.character(Sys.time()), ">> Reading feature ranking from", rankedFeaturesFile, "...\n");
if (!file.exists(rankedFeaturesFile)) {
  if (featureRankingMethod == "rf") {
    cat(as.character(Sys.time()), ">> Computing feature ranking using Random Forest...\n");
    # Use all features for ranking if featureCountList contains Inf
    maxRankFeatures = if (any(is.infinite(featureCountList))) {
      ncol(features) - 1
    } else {
      max(featureCountList)
    };
    rankingSet = featurefiltering(features, colnames(features)[colnames(features) != "protection"], 
                                   maxRankFeatures);
    rfmodel = randomForest(protection ~ ., rankingSet, importance=TRUE);
    rankedFeatures = rownames(rfmodel$importance[order(-rfmodel$importance[,3]),]);
    saveRDS(rankedFeatures, rankedFeaturesFile);
    cat(as.character(Sys.time()), ">> Done. Saved to", rankedFeaturesFile, "\n");
  } else {
    stop(paste("Feature ranking file not found:", rankedFeaturesFile, 
               "\nPlease generate it first or set featureRankingMethod = 'rf'."));
  }
} else {
  rankedFeatures = readRDS(rankedFeaturesFile);
  cat(as.character(Sys.time()), ">> Done\n");
}

# Data preprocessing
# Random shuffle (if specified in paper, otherwise comment out)
# features <- features[sample(nrow(features)),]

# Convert to regression mode if needed
if (DoRegression) {
  # Cis-Golgi becomes 1 and Trans-Golgi becomes 2.
  # But we want Cis-Golgi (positive class) to be 1 and Trans-Golgi to be 0
  features$protection = 2 - as.numeric(features$protection);
  if (!useCV) {
    testFeatures$protection = 2 - as.numeric(testFeatures$protection);
  }
}

# Initialize results
accData = NULL;
bestPerf = NULL;
bestParams = NULL;

# Main evaluation loop
if (useCV) {
  cat(as.character(Sys.time()), ">> Entering cross validation. Folds = ", nFolds, " ...\n");
  
  # Jackknife
  if (nFolds < 0) {
    nFolds = length(features[,1]);
  }
  
  # Reduce feature vectors to max size for efficiency
  if (!any(is.infinite(featureCountList))) {
    features = featurefiltering(features, rankedFeatures, max(featureCountList));
  }
  
  for (maxFeatureCount in featureCountList) {
    if (is.infinite(maxFeatureCount)) {
      trainingSet = features;
    } else {
      trainingSet = featurefiltering(features, rankedFeatures, maxFeatureCount);
    }
    
    for (svmC in svmCostList) {
      perf = svmCV(protection ~ ., trainingSet, svmCost = svmC, cross = nFolds);
      
      if (DoRegression) {
        cat(maxFeatureCount, ",", svmC, ",", perf$auc, ",", perf$threshold, ",", 
            perf$acc, ",", perf$spec, ",", perf$sens, ",", perf$mcc);
        accData = rbind(accData, c(maxFeatureCount, svmC, perf$auc, perf$threshold, 
                                    perf$acc, perf$spec, perf$sens, perf$mcc));
      } else {
        cat(maxFeatureCount, ",", svmC, ",", perf$acc, ",", perf$sens, ",", 
            perf$spec, ",", perf$mcc);
        accData = rbind(accData, c(maxFeatureCount, svmC, perf$acc, perf$sens, 
                                    perf$spec, perf$mcc));
      }
      
      write.csv(accData, outFile);
      
      if (is.null(bestPerf) || bestPerf$acc < perf$acc) {
        bestPerf = perf;
        bestParams = list(
          "maxFeatureCount" = maxFeatureCount,
          "svmC" = svmC
        );
        cat(",<-- BEST");
      }
      
      cat("\n");
    }
  }
  
  # Print best results
  cat("\n");
  cat("========================================\n");
  cat("BASELINE RESULTS (Cross-Validation)\n");
  cat("========================================\n");
  cat("Best Result for <nF, C> = ", bestParams$maxFeatureCount, ", ", bestParams$svmC, "\n");
  if (DoRegression) {
    cat("AUCROC                : ", bestPerf$auc, "\n");
    cat("Threshold             : ", bestPerf$threshold, "\n");
    # Swap sens and spec for interpretation
    temp = bestPerf$sens;
    bestPerf$sens = bestPerf$spec;
    bestPerf$spec = temp;
  }
  cat("Accuracy (Overall)    : ", bestPerf$acc, "\n");
  cat("Accuracy (Trans-Golgi): ", bestPerf$sens, "\n");
  cat("Accuracy (Cis-Golgi)  : ", bestPerf$spec, "\n");
  cat("MCC                   : ", bestPerf$mcc, "\n");
  cat("========================================\n");
  
} else {
  # Independent test set evaluation
  cat(as.character(Sys.time()), ">> Entering independent test evaluation ...\n");
  
  # Reduce feature vectors to max size for efficiency
  if (!any(is.infinite(featureCountList))) {
    features = featurefiltering(features, rankedFeatures, max(featureCountList));
    testFeatures = featurefiltering(testFeatures, rankedFeatures, max(featureCountList));
  }
  
  for (maxFeatureCount in featureCountList) {
    if (is.infinite(maxFeatureCount)) {
      trainingSet = features;
      testSet = testFeatures;
    } else {
      trainingSet = featurefiltering(features, rankedFeatures, maxFeatureCount);
      testSet = featurefiltering(testFeatures, rankedFeatures, maxFeatureCount);
    }
    
    for (svmC in svmCostList) {
      model = svm(protection ~ ., trainingSet, cost = svmC, kernel = svmKernel);
      pred = predict(model, testSet);
      
      if (DoRegression) {
        # Regression-based performance measurements
        predAndTruth = prediction(pred, testSet$protection);
        auc = ROCR::performance(predAndTruth, "auc")@y.values[[1]];
        
        accSeries = ROCR::performance(predAndTruth, "acc");
        threshold = unlist(accSeries@x.values)[[which.max(unlist(accSeries@y.values))]];
        predAndTruth = prediction(as.numeric(pred >= threshold), testSet$protection);
      } else {
        # Classification-based performance measurements
        predAndTruth = prediction(as.numeric(pred), as.numeric(testSet$protection));
      }
      
      acc = unlist(ROCR::performance(predAndTruth, "acc")@y.values)[2];
      sens = unlist(ROCR::performance(predAndTruth, "sens")@y.values)[2];
      spec = unlist(ROCR::performance(predAndTruth, "spec")@y.values)[2];
      mcc = unlist(ROCR::performance(predAndTruth, "mat")@y.values)[2];
      
      if (DoRegression) {
        cat(maxFeatureCount, ",", svmC, ",", auc, ",", threshold, ",", 
            acc, ",", spec, ",", sens, ",", mcc, "\n");
        accData = rbind(accData, c(maxFeatureCount, svmC, auc, threshold, 
                                    acc, spec, sens, mcc));
      } else {
        cat(maxFeatureCount, ",", svmC, ",", acc, ",", sens, ",", spec, ",", mcc, "\n");
        accData = rbind(accData, c(maxFeatureCount, svmC, acc, sens, spec, mcc));
      }
      
      write.csv(accData, outFile);
      
      # Store results for final summary
      if (is.null(bestPerf)) {
        bestPerf = list(
          "acc" = acc,
          "sens" = sens,
          "spec" = spec,
          "mcc" = mcc
        );
        if (DoRegression) {
          bestPerf$auc = auc;
          bestPerf$threshold = threshold;
        }
        bestParams = list(
          "maxFeatureCount" = maxFeatureCount,
          "svmC" = svmC
        );
      }
    }
  }
  
  # Print results
  cat("\n");
  cat("========================================\n");
  cat("BASELINE RESULTS (Independent Test)\n");
  cat("========================================\n");
  cat("Parameters: <nF, C> = ", bestParams$maxFeatureCount, ", ", bestParams$svmC, "\n");
  if (DoRegression) {
    cat("AUCROC                : ", bestPerf$auc, "\n");
    cat("Threshold             : ", bestPerf$threshold, "\n");
    # Swap sens and spec for interpretation
    temp = bestPerf$sens;
    bestPerf$sens = bestPerf$spec;
    bestPerf$spec = temp;
  }
  cat("Accuracy (Overall)    : ", bestPerf$acc, "\n");
  cat("Accuracy (Trans-Golgi): ", bestPerf$sens, "\n");
  cat("Accuracy (Cis-Golgi)  : ", bestPerf$spec, "\n");
  cat("MCC                   : ", bestPerf$mcc, "\n");
  cat("========================================\n");
}

cat(as.character(Sys.time()), ">> Results saved to", outFile, "\n");
cat(as.character(Sys.time()), ">> Baseline reproduction complete.\n");


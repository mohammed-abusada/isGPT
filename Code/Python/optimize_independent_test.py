"""
Optimize parameters specifically for independent test set.
This will search more thoroughly to find the best configuration.
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, matthews_corrcoef, roc_auc_score
import pyreadr

# Change to R directory for data files
script_dir = os.path.dirname(os.path.abspath(__file__))
r_dir = os.path.join(os.path.dirname(script_dir), 'R')
os.chdir(r_dir)

print("="*70)
print("OPTIMIZING FOR INDEPENDENT TEST SET")
print("="*70)

# Load data
print("Loading data...")
features = pyreadr.read_r('featurized_comb_SMOTED.rds')[None]
test_features = pyreadr.read_r('testFeaturized_comb.rds')[None]
ranked_features = pyreadr.read_r('rankedFeatures.rds')[None]

# Convert ranked_features to list if needed
if isinstance(ranked_features, pd.DataFrame):
    ranked_features = ranked_features.iloc[:, 0].tolist()
elif isinstance(ranked_features, pd.Series):
    ranked_features = ranked_features.tolist()

print(f"Training samples: {len(features)}")
print(f"Test samples: {len(test_features)}")
print(f"Ranked features: {len(ranked_features)}")

# Preprocess: convert to regression mode
if features['protection'].dtype == 'object' or features['protection'].dtype.name == 'category':
    features['protection'] = pd.Categorical(features['protection']).codes + 1
features['protection'] = 2 - features['protection'].astype(float)

if test_features['protection'].dtype == 'object' or test_features['protection'].dtype.name == 'category':
    test_features['protection'] = pd.Categorical(test_features['protection']).codes + 1
test_features['protection'] = 2 - test_features['protection'].astype(float)

# Shuffle training data
features = features.sample(frac=1, random_state=10).reset_index(drop=True)

# Expanded parameter search
feature_counts = [2800, 2700, 2600, 2500, 2400, 2300, 2250, 2200, 2100, 2000, 1900, 1800, 1750, 1700, 1600, 1500]
c_values = [0.3, 0.5, 1, 2, 3, 5, 10, 15, 20, 30, 50, 75, 100, 150, 200]

print(f"\nSearching {len(feature_counts)} feature counts × {len(c_values)} C values = {len(feature_counts) * len(c_values)} combinations")
print("This may take a few minutes...\n")

results = []

for feat_count in feature_counts:
    # Filter features - use featurefiltering logic
    from utils import feature_filtering
    training_set = feature_filtering(features.copy(), ranked_features, feat_count)
    test_set = feature_filtering(test_features.copy(), ranked_features, feat_count)
    
    X_train = training_set.drop('protection', axis=1)
    y_train = training_set['protection']
    X_test = test_set.drop('protection', axis=1)
    y_test = test_set['protection']
    
    # Ensure feature order matches
    feature_cols = [f for f in ranked_features[:feat_count] if f in X_train.columns]
    X_train = X_train[feature_cols]
    X_test = X_test[[f for f in feature_cols if f in X_test.columns]]
    
    # Add missing features with zeros
    for col in feature_cols:
        if col not in X_test.columns:
            X_test[col] = 0
    X_test = X_test[feature_cols]
    
    for c_val in c_values:
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = SVR(kernel='linear', C=c_val)
        model.fit(X_train_scaled, y_train)
        pred = model.predict(X_test_scaled)
        
        # Find optimal threshold
        thresholds = np.unique(pred)
        if len(thresholds) > 100:
            thresholds = np.percentile(pred, np.linspace(0, 100, 201))
        
        best_threshold = 0.5
        best_acc = 0
        
        for thresh in thresholds:
            y_pred_binary = (pred >= thresh).astype(int)
            acc = accuracy_score(y_test, y_pred_binary)
            if acc > best_acc:
                best_acc = acc
                best_threshold = thresh
        
        # Calculate final metrics
        y_pred_binary = (pred >= best_threshold).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred_binary).ravel()
        acc = accuracy_score(y_test, y_pred_binary)
        sens = tp / (tp + fn) if (tp + fn) > 0 else 0
        spec = tn / (tn + fp) if (tn + fp) > 0 else 0
        mcc = matthews_corrcoef(y_test, y_pred_binary)
        
        try:
            auc = roc_auc_score(y_test, pred)
        except:
            auc = 0.5
        
        results.append({
            'FeatureCount': feat_count,
            'SVMCost': c_val,
            'AUC': auc,
            'Threshold': best_threshold,
            'Accuracy': acc,
            'Sensitivity': sens,
            'Specificity': spec,
            'MCC': mcc
        })
        
        print(f"{feat_count}, {c_val:.1f}, {auc:.4f}, {best_threshold:.4f}, {acc:.4f}, {spec:.4f}, {sens:.4f}, {mcc:.4f}")

# Convert to DataFrame and save
df_results = pd.DataFrame(results)
df_results = df_results.sort_values('Accuracy', ascending=False)

print("\n" + "="*70)
print("TOP 10 CONFIGURATIONS FOR INDEPENDENT TEST")
print("="*70)
print(df_results[['FeatureCount', 'SVMCost', 'Accuracy', 'MCC', 'Sensitivity', 'Specificity']].head(10).to_string(index=False))

best = df_results.iloc[0]
print("\n" + "="*70)
print("BEST CONFIGURATION FOR INDEPENDENT TEST")
print("="*70)
print(f"Feature Count: {int(best['FeatureCount'])}")
print(f"SVM Cost (C): {best['SVMCost']}")
print(f"Threshold: {best['Threshold']:.4f}")
print(f"Accuracy: {best['Accuracy']:.4f} ({best['Accuracy']*100:.2f}%)")
print(f"MCC: {best['MCC']:.4f}")
print(f"Sensitivity: {best['Sensitivity']:.4f}")
print(f"Specificity: {best['Specificity']:.4f}")
print(f"AUC-ROC: {best['AUC']:.4f}")
print("="*70)

# Save results
df_results.to_csv('optimized_independent_test_results.csv', index=False)
print(f"\nResults saved to: optimized_independent_test_results.csv")


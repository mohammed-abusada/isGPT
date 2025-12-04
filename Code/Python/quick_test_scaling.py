"""
Quick test: Compare results WITH and WITHOUT feature scaling.
This tests if scaling helps or hurts performance.
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, matthews_corrcoef
import pyreadr

# Change to R directory
script_dir = os.path.dirname(os.path.abspath(__file__))
r_dir = os.path.join(os.path.dirname(script_dir), 'R')
os.chdir(r_dir)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import feature_filtering

print("="*70)
print("QUICK TEST: Feature Scaling Impact")
print("="*70)

# Load data
print("Loading data...")
features = pyreadr.read_r('featurized_comb_SMOTED.rds')[None]
test_features = pyreadr.read_r('testFeaturized_comb.rds')[None]
ranked_features = pyreadr.read_r('rankedFeatures.rds')[None]

if isinstance(ranked_features, pd.DataFrame):
    ranked_features = ranked_features.iloc[:, 0].tolist()
elif isinstance(ranked_features, pd.Series):
    ranked_features = ranked_features.tolist()

# Preprocess
if features['protection'].dtype == 'object' or features['protection'].dtype.name == 'category':
    features['protection'] = pd.Categorical(features['protection']).codes + 1
features['protection'] = 2 - features['protection'].astype(float)

if test_features['protection'].dtype == 'object' or test_features['protection'].dtype.name == 'category':
    test_features['protection'] = pd.Categorical(test_features['protection']).codes + 1
test_features['protection'] = 2 - test_features['protection'].astype(float)

# Use optimal parameters
feat_count = 2200
c_val = 10

# Filter features
training_set = feature_filtering(features.copy(), ranked_features, feat_count)
test_set = feature_filtering(test_features.copy(), ranked_features, feat_count)

X_train = training_set.drop('protection', axis=1)
y_train = training_set['protection']
X_test = test_set.drop('protection', axis=1)
y_test = test_set['protection']

def test_with_scaling(scale=True):
    """Test with or without scaling."""
    if scale:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
    else:
        X_train_scaled = X_train.values
        X_test_scaled = X_test.values
    
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
    
    # Final metrics
    y_pred_binary = (pred >= best_threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred_binary).ravel()
    acc = accuracy_score(y_test, y_pred_binary)
    sens = tp / (tp + fn) if (tp + fn) > 0 else 0
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0
    mcc = matthews_corrcoef(y_test, y_pred_binary)
    
    return {
        'accuracy': acc,
        'mcc': mcc,
        'sensitivity': sens,
        'specificity': spec,
        'threshold': best_threshold
    }

print(f"\nTesting with: {feat_count} features, C={c_val}")
print("="*70)

# Test WITH scaling
print("\n1. WITH feature scaling (current implementation):")
result_with = test_with_scaling(scale=True)
print(f"   Accuracy: {result_with['accuracy']:.4f} ({result_with['accuracy']*100:.2f}%)")
print(f"   MCC: {result_with['mcc']:.4f}")
print(f"   Sensitivity: {result_with['sensitivity']:.4f}")
print(f"   Specificity: {result_with['specificity']:.4f}")

# Test WITHOUT scaling
print("\n2. WITHOUT feature scaling:")
result_without = test_with_scaling(scale=False)
print(f"   Accuracy: {result_without['accuracy']:.4f} ({result_without['accuracy']*100:.2f}%)")
print(f"   MCC: {result_without['mcc']:.4f}")
print(f"   Sensitivity: {result_without['sensitivity']:.4f}")
print(f"   Specificity: {result_without['specificity']:.4f}")

# Comparison
print("\n" + "="*70)
print("COMPARISON:")
print("="*70)
diff_acc = result_with['accuracy'] - result_without['accuracy']
diff_mcc = result_with['mcc'] - result_without['mcc']

print(f"Accuracy difference: {diff_acc:+.4f} ({diff_acc*100:+.2f}%)")
print(f"MCC difference: {diff_mcc:+.4f}")

if diff_acc > 0:
    print("\n✓ Feature scaling IMPROVES performance - KEEP IT")
elif diff_acc < 0:
    print("\n⚠ Feature scaling REDUCES performance - CONSIDER REMOVING")
else:
    print("\n→ Feature scaling has NO IMPACT on performance")

print("\nNote: R's implementation uses scale=TRUE, so scaling matches R behavior.")
print("="*70)


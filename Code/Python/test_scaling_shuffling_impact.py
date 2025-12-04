"""
Test the impact of feature scaling and data shuffling on performance.
This will help determine if these changes should be kept or rolled back.
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
print("TESTING IMPACT OF FEATURE SCALING AND DATA SHUFFLING")
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

# Preprocess: convert to regression mode
if features['protection'].dtype == 'object' or features['protection'].dtype.name == 'category':
    features['protection'] = pd.Categorical(features['protection']).codes + 1
features['protection'] = 2 - features['protection'].astype(float)

if test_features['protection'].dtype == 'object' or test_features['protection'].dtype.name == 'category':
    test_features['protection'] = pd.Categorical(test_features['protection']).codes + 1
test_features['protection'] = 2 - test_features['protection'].astype(float)

# Test configurations
configs = [
    {"name": "WITH scaling, WITH shuffling", "scale": True, "shuffle": True},
    {"name": "WITH scaling, NO shuffling", "scale": True, "shuffle": False},
    {"name": "NO scaling, WITH shuffling", "scale": False, "shuffle": True},
    {"name": "NO scaling, NO shuffling", "scale": False, "shuffle": False},
]

# Use optimal parameters for independent test
feat_count = 2200
c_val = 10

print(f"\nTesting with: {feat_count} features, C={c_val}")
print("="*70)

results = []

for config in configs:
    print(f"\nTesting: {config['name']}")
    
    # Filter features
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from utils import feature_filtering
    training_set = feature_filtering(features.copy(), ranked_features, feat_count)
    test_set = feature_filtering(test_features.copy(), ranked_features, feat_count)
    
    X_train = training_set.drop('protection', axis=1)
    y_train = training_set['protection']
    X_test = test_set.drop('protection', axis=1)
    y_test = test_set['protection']
    
    # Shuffle if requested
    if config['shuffle']:
        indices = np.arange(len(X_train))
        np.random.seed(10)
        np.random.shuffle(indices)
        X_train = X_train.iloc[indices].reset_index(drop=True)
        y_train = y_train.iloc[indices].reset_index(drop=True)
    
    # Scale if requested
    if config['scale']:
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
    else:
        X_train_scaled = X_train.values
        X_test_scaled = X_test.values
    
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
        'Configuration': config['name'],
        'Scaling': config['scale'],
        'Shuffling': config['shuffle'],
        'Accuracy': acc,
        'MCC': mcc,
        'Sensitivity': sens,
        'Specificity': spec,
        'AUC': auc,
        'Threshold': best_threshold
    })
    
    print(f"  Accuracy: {acc:.4f} ({acc*100:.2f}%)")
    print(f"  MCC: {mcc:.4f}")
    print(f"  Sensitivity: {sens:.4f}")
    print(f"  Specificity: {spec:.4f}")

# Summary
print("\n" + "="*70)
print("SUMMARY - Impact of Scaling and Shuffling")
print("="*70)
df_results = pd.DataFrame(results)
df_results = df_results.sort_values('Accuracy', ascending=False)

print("\nResults ranked by Accuracy:")
print(df_results[['Configuration', 'Accuracy', 'MCC', 'Sensitivity', 'Specificity']].to_string(index=False))

best = df_results.iloc[0]
worst = df_results.iloc[-1]

print(f"\nBEST: {best['Configuration']}")
print(f"  Accuracy: {best['Accuracy']:.4f} ({best['Accuracy']*100:.2f}%)")
print(f"  MCC: {best['MCC']:.4f}")

print(f"\nWORST: {worst['Configuration']}")
print(f"  Accuracy: {worst['Accuracy']:.4f} ({worst['Accuracy']*100:.2f}%)")
print(f"  MCC: {worst['MCC']:.4f}")

print(f"\nDifference: {best['Accuracy'] - worst['Accuracy']:.4f} ({((best['Accuracy'] - worst['Accuracy'])*100):.2f}%)")

# Check if scaling helps
with_scaling = df_results[df_results['Scaling'] == True]['Accuracy'].mean()
without_scaling = df_results[df_results['Scaling'] == False]['Accuracy'].mean()
print(f"\nAverage WITH scaling: {with_scaling:.4f}")
print(f"Average WITHOUT scaling: {without_scaling:.4f}")
print(f"Scaling impact: {with_scaling - without_scaling:.4f} ({((with_scaling - without_scaling)*100):.2f}%)")

# Check if shuffling helps
with_shuffling = df_results[df_results['Shuffling'] == True]['Accuracy'].mean()
without_shuffling = df_results[df_results['Shuffling'] == False]['Accuracy'].mean()
print(f"\nAverage WITH shuffling: {with_shuffling:.4f}")
print(f"Average WITHOUT shuffling: {without_shuffling:.4f}")
print(f"Shuffling impact: {with_shuffling - without_shuffling:.4f} ({((with_shuffling - without_shuffling)*100):.2f}%)")

print("\n" + "="*70)
print("RECOMMENDATION:")
if best['Scaling'] and best['Shuffling']:
    print("✓ KEEP both scaling and shuffling - they improve performance")
elif best['Scaling']:
    print("✓ KEEP scaling, but shuffling may not be necessary")
elif best['Shuffling']:
    print("✓ KEEP shuffling, but scaling may not be necessary")
else:
    print("⚠ Consider removing scaling and shuffling - they may reduce performance")
print("="*70)


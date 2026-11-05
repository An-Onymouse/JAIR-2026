#!/usr/bin/env python
import pandas as pd
import statsmodels.api as sm
from scipy import stats
import numpy as np
import sys

# output saved as argument_type_report.csv


import pandas as pd
import statsmodels.api as sm

# Import data
df = pd.read_csv(
    "data_for_multi_regression.csv",
    header=None,
    names=["judge", "first", "last", "main", "target"],
    dtype={
        'judge': str,
        'first': int,
        'last': int,
        'main': int,
        'target': int
    }
)

# Ensure categorical columns are integers (they should be 1-4)
df[['first', 'last', 'main']] = df[['first', 'last', 'main']].astype('int')

# Create dummies (drop first category of each variable to avoid multicollinearity)
X = pd.get_dummies(df[['first', 'last', 'main']], 
                   columns=['first', 'last', 'main'], 
                   drop_first=True)

y = df['target']

# Full dataset model
X_const = sm.add_constant(X).astype('float64')
full_model = sm.Logit(y, X_const).fit(disp=False)
print(full_model.summary())

# Per-judge models
judge_results = {}

for judge in df['judge'].unique():
    idx = df['judge'] == judge
    X_j = X[idx]
    y_j = y[idx]
    
    if y_j.nunique() < 2:
        judge_results[judge] = "Skipped - constant target"
        continue
    
    X_j_const = sm.add_constant(X_j).astype('float64')
    model_j = sm.Logit(y_j, X_j_const).fit(disp=False)
    judge_results[judge] = model_j
    print()

    # View coefficients for first judge as example
    first_judge = df['judge'].unique()[0]
    print(f"\nCoefficients for {judge}:")
    print(judge_results[judge].summary())
    print()
# Regression and Statistical Inference Toolkit

Welcome to the **reg_stat_inference** toolkit!

This toolkit provides functions for treating multicollinearity and performing feature selection based on p-values in linear regression and logistic regression models. It leverages the `statsmodels` library for model analysis.

## Purpose

The purpose of this toolkit is to offer a collection of Python functions that streamline the process of dealing with multicollinearity and feature selection in regression models. It aims to simplify the analysis of complex datasets by automating tasks like variance inflation factor (VIF) calculation and p-value-based feature removal.

## reg_stat_inference

**reg_stat_inference** is a Python package that provides functions for treating multicollinearity and performing statistical inference in regression models. It offers tools to identify and address multicollinearity issues and to iteratively drop features based on p-values. This can help you build more interpretable and robust regression models.

## Installation

You can install **reg_stat_inference** using pip:

```bash
pip install reg-stat-inference
```

## Usage

To use the toolkit, import the functions in your scripts or notebooks:

```python
import pandas as pd
import statsmodels.api as sm
from reg_stat_inference import treat_regression_model

# Create sample data
X = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6]})
y = pd.DataFrame({'target': [0, 1, 0]})

# Use the treat_regression_model function with OLS regression
result = treat_regression_model(X, y, threshhold_vif=5, threshold_pval=0.05, reg_type='OLS')

# Print the treated feature list and the model summary
print("Treated Features:", result.metric_list)
print(result.model.summary())
```
You can then apply these functions to your dataset to enhance the quality of your regression models.

## Git Repo

For detailed documentation and usage examples, please refer to the [GitHub repository](https://github.com/DirceuVio/reg_stat_inference).


## Contributing
Contributions are welcome! If you have suggestions, bug reports, or improvements, please open an issue or submit a pull request.
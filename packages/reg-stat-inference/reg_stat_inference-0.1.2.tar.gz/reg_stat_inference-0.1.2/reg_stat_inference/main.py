import pandas as pd
import numpy as np

import statsmodels.stats.api as sms
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.api as sm

from typing import List, Tuple, Any, Union
from dataclasses import dataclass

@dataclass
class TreatedModelResults:
    """
    An object to store the model's results after treatment

    Parameters:
    - metric_list (List[str]): The metrics returned by the model
    - model (sm.Logit | sm.OLS): The final model after treatment
    """
    metric_list: List[str]
    model: Union[sm.Logit, sm.OLS]

    def __repr__(self) -> str:
        return f"TreatedModelResults(metric_list={self.metric_list}, model={self.model})"


def treat_regression_model(
        X: pd.DataFrame,
        y: pd.DataFrame,
        threshhold_vif: float = 5,
        threshold_pval: float = 0.05,
        reg_type: str = 'OLS'
    ) -> TreatedModelResults:
    """
    Treat multicollinearity and drop features based on p-values in a linear regression or logistic regression model.

    Parameters
    ----------
    X : pd.DataFrame
        The independent variable(s).
    y : pd.DataFrame
        The target variable.
    threshhold_vif : float, optional
        The threshold for variance inflation factor (VIF).
        Default is 5.
    threshold_pval : float, optional
        The threshold p-value. Features with p-values greater than this threshold will be dropped.
        Default is 0.05.
    reg_type : str, optional
        The regression type. Must be "OLS" or "logit".

    Returns
    -------
    TreatedModelResults
        An object containing the results of the model after treatment.

    Raises
    ------
    ValueError
        If `reg_type` is not valid.
    ValueError
        If `threshhold_vif` is not a non-negative number.
    ValueError
        If `threshold_pval` is not within the valid range (0 to 1).

    Notes
    -----
    This function treats multicollinearity in the input DataFrame `X` based on the specified VIF threshold,
    and then iteratively drops features from the treated DataFrame based on their p-values in a linear
    regression or logistic regression model. The regression type is determined by the `reg_type` parameter.

    Examples
    --------
    >>> X = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6]})
    >>> y = pd.DataFrame({'target': [0, 1, 0]})
    >>> result = treat_regression_model(X, y, threshhold_vif=3, threshold_pval=0.1, reg_type='OLS')
    >>> print(result)
    TreatedModelResults(metric_list=['feature1', 'feature2'], model=<statsmodels.regression.linear_model.OLS object at ...>)
    """

    if reg_type not in ['OLS', 'logit']:
        raise ValueError("Invalid 'reg_type'. Must be 'OLS' or 'logit'.")

    if threshhold_vif < 0:
        raise ValueError("Invalid 'threshhold_vif'. Must be a non-negative number.")

    if threshold_pval < 0 or threshold_pval > 1:
        raise ValueError("Invalid 'threshold_pval'. Must be greater than 0 and less than 1")
    
    vif_results = treat_multicollinearity(X, y, threshhold_vif, reg_type)

    pval_results = treat_pvalue(X[vif_results.metric_list], y, threshold_pval, reg_type)

    return pval_results



def treat_multicollinearity(
        X: pd.DataFrame,
        y: pd.DataFrame,
        threshhold_vif: float = 5,
        reg_type: str = 'OLS'
    ) -> TreatedModelResults:
    """
    Treat multicollinearity in a linear regression or logistic regression model.

    Parameters
    ----------
    X : pd.DataFrame
        The independent variable(s).
    y : pd.DataFrame
        The target variable.
    threshhold_vif : float, optional
        The threshold for variance inflation factor (VIF).
        Default is 5.
    reg_type : str, optional
        The regression type. Must be "OLS" or "logit".

    Returns
    -------
    TreatedModelResults
        An object containing the results of the model after treatment.

    Raises
    ------
    ValueError
        If `reg_type` is not valid.
    ValueError
        If `threshhold_vif` is not a positive number.
    """

    regression_mapping = {
        'OLS': (sm.OLS, {}),
        'logit': (sm.Logit, {}),
    }


    if reg_type not in ['OLS', 'logit']:
        raise ValueError("Invalid 'reg_type'. Must be 'OLS' or 'logit'.")

    if threshhold_vif < 0:
        raise ValueError("Invalid 'threshhold_vif'. Must be a positive number.")

    
    model_class, model_args = regression_mapping[reg_type]
    
    vif_series = pd.Series(
        [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
        index=X.columns,
        dtype=float,
    )

    col_to_drop = vif_series.sort_values(ascending=False).index[0]
    max_vif = vif_series.max()

    X = sm.add_constant(X)

    model = model_class(y, X.astype(float), **model_args).fit(disp=False)

    dropped_features = []

    while max_vif >= threshhold_vif and col_to_drop not in dropped_features:
        X = X.drop(col_to_drop, axis=1)
        X = sm.add_constant(X)

        model = model_class(y, X.astype(float), **model_args).fit(disp=False)

        X = X.drop('const', axis=1)
        vif_series = pd.Series(
            [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
            index=X.columns,
            dtype=float,
        )
        col_to_drop = vif_series.sort_values(ascending=False).index[0]
        max_vif = vif_series.max()

        dropped_features.append(col_to_drop)

    return TreatedModelResults(
        vif_series.index.tolist(),
        model
    )

def treat_pvalue(
        X: pd.DataFrame,
        y: pd.DataFrame,
        threshold_pval: float = 0.05,
        reg_type: str = 'OLS'
    ) -> TreatedModelResults:
    """
    Iteratively drops features based on p-values in a linear regression or logistic regression model.

    Parameters
    ----------
    X : pd.DataFrame
        The independent variable(s).
    y : pd.DataFrame
        The target variable.
    threshold_pval : float, optional
        The threshold p-value. Features with p-values greater than this threshold will be dropped.
        Default is 0.05.
    reg_type : str, optional
        The regression type. Must be "OLS" or "logit".

    Returns
    -------
    TreatedModelResults
        An object containing the results of the model after treatment.

    Raises
    ------
    ValueError
        If `reg_type` is not valid.
    ValueError
        If `threshold_pval` is not within the valid range (0 to 1).

    Notes
    -----
    This function iteratively drops features from the input DataFrame `X` based on their p-values in
    a linear regression or logistic regression model. The regression type is determined by the
    `reg_type` parameter.

    Examples
    --------
    >>> X = pd.DataFrame({'feature1': [1, 2, 3], 'feature2': [4, 5, 6]})
    >>> y = pd.DataFrame({'target': [0, 1, 0]})
    >>> result = treat_pvalue(X, y, threshold_pval=0.1, reg_type='OLS')
    >>> print(result)
    TreatedModelResults(metric_list=['feature1', 'feature2'], model=<statsmodels.regression.linear_model.OLS object at ...>)
    """

    regression_mapping = {
        'OLS': (sm.OLS, {}),
        'logit': (sm.Logit, {}),
    }

    if reg_type not in regression_mapping:
        raise ValueError("Invalid 'reg_type'. Must be 'OLS' or 'logit'.")

    if threshold_pval < 0 or threshold_pval > 1:
        raise ValueError("Invalid 'threshold_pval'. Must be greater than 0 and less than 1")

    cols = X.columns.tolist()

    max_p_value = 1

    model_class, model_args = regression_mapping[reg_type]

    cols_to_drop = []

    while max_p_value > threshold_pval:
        X = sm.add_constant(X[cols])

        model = model_class(y, X.astype(float), **model_args).fit(disp=False)

        p_values = model.pvalues
        max_p_value = max(p_values)

        col_to_drop = p_values.idxmax()

        if col_to_drop in cols:
            cols.remove(col_to_drop)
            cols_to_drop.append(col_to_drop)

    return TreatedModelResults(cols_to_drop, model)

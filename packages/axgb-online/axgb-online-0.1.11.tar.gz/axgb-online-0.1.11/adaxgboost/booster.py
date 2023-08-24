from river import base

import xgboost
import pandas as pd
import numpy as np

import typing

from abc import ABC

class Constants(ABC):
    # Supported objectives
    BINARY_LOGISTIC = "binary:logistic"
    MULTI_SOFTPROB = "multi:softprob"
    SUPPORTED_OBJECTIVES = [BINARY_LOGISTIC, MULTI_SOFTPROB]
    SUPPORTED_MULTICLASS_OBJECTIVES = [MULTI_SOFTPROB]

    # booster parameter
    OBJECTIVE = "objective"
    NUM_CLASS = "num_class"

    # Defaults
    DEFAULT_OBJECTIVE = BINARY_LOGISTIC
    DEFAULT_MULTICLASS_OBJECTIVE = MULTI_SOFTPROB

class TreeBooster(base.MiniBatchClassifier, base.Estimator):
    
    def __init__(self, booster_params: dict = {}) -> None:
        """
        XGBoost base tree binary classifier
        This is a river wrapper for the [xgboost](https://xgboost.readthedocs.io/en/stable/) library.

        Parameters
        -----------
        booster_params: optional dict (default {})
            for booster parameters see [Booster documentation](https://xgboost.readthedocs.io/en/stable/parameter.html?highlight=booster%20parameters).
        """
        if not Constants.OBJECTIVE in booster_params.keys():
            booster_params[Constants.OBJECTIVE] = Constants.DEFAULT_OBJECTIVE
        if not booster_params[Constants.OBJECTIVE] in Constants.SUPPORTED_OBJECTIVES:
            raise AttributeError(f"""
                Cannot use {booster_params[Constants.OBJECTIVE]} as objective function.
                Use one in {Constants.SUPPORTED_OBJECTIVES} instead.
            """)
        super().__init__()
        self.__booster_params = booster_params
        self._booster = None

    @property
    def booster_params(self):
        return self.__booster_params
    def set_param(self, param:str, value:typing.Any):
        if self._booster is not None:
            self._booster.set_param(param, value)
        self.__booster_params[param] = value

    def learn_one(self, x: dict, y: base.typing.ClfTarget) -> "base.Estimator":
        raise NotImplementedError("This class is a vrapper of xgboost library. Cannot train xgboost with one data")

    def learn_many(self, X: typing.Union["pd.DataFrame", dict, xgboost.DMatrix], y: "pd.Series") -> "base.MiniBatchClassifier":
        """
        Train booster with given features and labels

        Parameters
        -----------
        X: dict
            dictionary containing training data point (feature: value)
        y: bool | str | int
            target label

        Output:
        ----------
        XGBTreeClassifier:
            trained model
        """
        d_mini_batch_train = self.__cast(X, y)
        self._booster = xgboost.train(self.booster_params, dtrain=d_mini_batch_train, num_boost_round=1, verbose_eval=False, xgb_model = self._booster)
        return self

    @staticmethod
    def __cast(X: typing.Union["pd.DataFrame", dict, xgboost.DMatrix], y: "pd.Series" = None) -> xgboost.DMatrix:
        """
        Cast given data in xgboost.DMatrix

        Parameters
        -----------
        X: pd.DataFrame | dict | xgboost.DMatrix
            data to be converted. If DMatrix is given it apply an identity function (output = input)
        y: optional pd.Series (default None)
            target labels to be added to the output DMatrix (not used if x is a dictionary)

        Outputs
        ----------
        xgboost.DMatrix:
            matrix with given data
        """
        if isinstance(X, dict):
            try:
                X = pd.DataFrame(X)
            except ValueError:
                X = pd.DataFrame(X, index = [0])
            finally:
                d_train = xgboost.DMatrix(X, feature_names=X.columns)
        elif isinstance(X, pd.DataFrame):
            try:
                d_train = xgboost.DMatrix(X, y.astype(int), feature_names=X.columns)
            except AttributeError:
                d_train = xgboost.DMatrix(X, feature_names=X.columns)
        elif isinstance(X, xgboost.DMatrix):
            d_train = X
        else:
            raise ValueError(f"Can cast only dictionaries, pandas DataFrames and xgboost DMatrix, {type(X)} was passed")
        
        return d_train
    
    def __booster_prediction(self, x: xgboost.DMatrix, output_margin: bool = False):
        """
        Uses Booster to perform prediction. If Booster is not trained yet returns .5 for every given row

        Parameters
        -----------
        X: xgboost.DMatrix
            data to perform prediction
        output_margin: optional bool (default = False)
            if True returns booster margins

        Outputs
        ----------
        xgboost.DMatrix:
            matrix with given data
        """
        if self._booster is None:
            return np.array([.5] * x.num_row())
        return self._booster.predict(x, output_margin=output_margin)
    
    def predict_one(self, x: dict, output_margin: bool = False) -> typing.Optional[base.typing.Target]:
        """
        Perform prediction on one data point

        Parameters
        -----------
        X: dict
            data to perform prediction
        output_margin: optional bool (default = False)
            if True returns booster margins

        Outputs
        ----------
        bool | float:
            xgboost.Booster prediction on given data
        """
        X = self.__cast(x)
        return self.__booster_prediction(X, output_margin)

    def predict_many(self, X: typing.Union["pd.DataFrame", "xgboost.DMatrix"]) -> "pd.DataFrame":
        """
        Perform prediction on one DataFrame and output probability of True and False

        Parameters
        -----------
        X: pa.DataFrame
            data to perform prediction

        Outputs
        ----------
        pd.Dataframe:
            containing predicted probability of True and False
        """
        x = self.__cast(X)
        return self.__booster_prediction(x)
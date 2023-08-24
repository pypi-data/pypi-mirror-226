from river import base

import xgboost
import numpy as np

from .booster import TreeBooster

from collections import Counter

import typing

class BaseXGBoost(base.ensemble.WrapperEnsemble, base.Classifier):
    _PUSH_STRATEGY = 'push'
    _REPLACE_STRATEGY = 'replace'
    _DYNAMIC_UPDATE_STRATEGY = "dynamic_update"
    _UPDATE_AND_MAINTAIN_STRATEGY = "update_all"
    _UPDATE_STRATEGIES = [_PUSH_STRATEGY, _REPLACE_STRATEGY, _DYNAMIC_UPDATE_STRATEGY, _UPDATE_AND_MAINTAIN_STRATEGY]

    _LAST_SAMPLE = "last"
    _MOST_COMMON = "most_common"
    _ALLOWED_BASE_PREDICTION_METHODS = [_LAST_SAMPLE, _MOST_COMMON]

    def __init__(self,
        n_models: int = 10,
        booster_params: dict = {},
        seed: int = None,
        max_window_size: int = 1000,
        min_window_size: int = None,
        update_strategy: str = 'replace',
        base_prediction: float = .5,
        base_prediction_method: str = ""
    ):
        """
        Adaptive XGBoost binary classifier
        See [Adaptive XGBoost for Evolving Data Streams](https://arxiv.org/pdf/2005.07353.pdf) paper for more info.
        

        Parameters
        -----------
        n_models: optional int (default = 10)
            number of boosters
        booster_params: optional dict (default None)
            for booster parameters see [Booster documentation](https://xgboost.readthedocs.io/en/stable/parameter.html?highlight=booster%20parameters).
        seed: optional int (default None):
            WrapperEnsamble seed initialization
        max_window_size: optional int (default 1000)
            window size to train new booster
        min_window_size: optional int (default None)
            min window size for early train
        update_strategy: optional str (default 'replace')
            replace and push strategies are described in Adaptive XGBoost paper. Use XGBoostClassifier._PUSH/REPLACE_STRATEGY
        base_prediction: optional float (default .5)
            base xgboost prediction
        base_prediction_method: optional str
            if given the initial base prediction is dinamically inferred

        Raises
        ----------
        AttributeError:
            - if max_window_size param is <= 1
            - if update_strategy is not valid
        """
        booster_params["base_score"] = base_prediction
        self._boosting_params = booster_params
        super().__init__(None, n_models, seed)

        self.__base_prediction = base_prediction
        self.__base_prediction_method = base_prediction_method
        if self.__base_prediction_method == self._LAST_SAMPLE:
            self.last_sample = self.__base_prediction
        if self.__base_prediction_method == self._MOST_COMMON:
            self.counter = Counter()
            self.counter.update((self.__base_prediction,))

        self.n_models = n_models
        if max_window_size <= 1:
            raise AttributeError(f"max_window_size parameter must be > 1, {max_window_size} were given")
        self.max_window_size = max_window_size
        self.min_window_size = min_window_size
        self._first_run = True
        self._init_margin = 0.0
        self._X_buffer = np.matrix([])
        self._y_buffer = np.matrix([])
        self._samples_seen = 0
        self._model_idx = 0
        if update_strategy not in self._UPDATE_STRATEGIES:
            raise AttributeError(f"Invalid update_strategy: {update_strategy}\nValid options: {self._UPDATE_STRATEGIES}")
        self.update_strategy = update_strategy
        self.__features = []
        self._configure()

    def _configure(self):
        """
        Configure Adaptive XGBoost based on given strategy
        """
        if self.update_strategy == self._PUSH_STRATEGY:
            self.data = []
        elif self.update_strategy == self._REPLACE_STRATEGY:
            for i, _ in enumerate(self):
                self[i] = None
        elif self.update_strategy == self._DYNAMIC_UPDATE_STRATEGY or self.update_strategy == self._UPDATE_AND_MAINTAIN_STRATEGY:
            for i, _ in enumerate(self):
                self[i] = self._new_base_model()
        self._reset_window_size()

    def reset(self):
        """
        Reset the estimator.
        """
        self._first_run = True
        self._configure()

    def _adjust_window_size(self):
        """
        Dinamically adjust window size for train Boosters
        """
        if self._dynamic_window_size < self.max_window_size:
            self._dynamic_window_size *= 2
            if self._dynamic_window_size > self.max_window_size:
                self.window_size = self.max_window_size
            else:
                self.window_size = self._dynamic_window_size

    def _reset_window_size(self):
        """
        Reset the window size to the original one
        """
        if self.min_window_size:
            self._dynamic_window_size = self.min_window_size
        else:
            self._dynamic_window_size = self.max_window_size
        self.window_size = self._dynamic_window_size
    
    def _update_model_idx(self):
        """
        Update the model index to be replaced
        """
        self._model_idx += 1
        if self._model_idx == self.n_models:
            self._model_idx = 0

    def learn_one(self, x: dict, y: base.typing.ClfTarget) -> "base.Estimator":
        """
        Learn from one data point

        Parameters
        ----------
        x: dict
            dictionary of data point (feature: value)
        y: str | bool | int
            label of the given data point

        Outputs
        ---------
        XGBoostBase
            self trained
        """
        X = self._handle_missing(x)
        
        if self._first_run:
            self._X_buffer = np.array([X])
            self._y_buffer = np.array([y])
            self._first_run = False
        else:
            pad_width = self.num_features - self._X_buffer.shape[1]
            if pad_width > 0:
                self._X_buffer = np.pad(self._X_buffer, pad_width= ((0,0),(0,pad_width)), constant_values=0)
        
            self._X_buffer = np.concatenate((self._X_buffer, [X]), axis = 0)
            self._y_buffer = np.concatenate((self._y_buffer, [y]), axis = 0)

        while self._X_buffer.shape[0] >= self.window_size:
            self._train_on_mini_batch(X=self._X_buffer[0:self.window_size, :],
                                      y=self._y_buffer[0:self.window_size])
            delete_idx = [i for i in range(self.window_size)]
            self._X_buffer = np.delete(self._X_buffer, delete_idx, axis=0)
            self._y_buffer = np.delete(self._y_buffer, delete_idx, axis=0)

            # Check window size and adjust it if necessary
            self._adjust_window_size()

        self.update_base_prediction(y)
        return self

    def _train_on_mini_batch(self, X: np.ndarray, y: np.ndarray):
        """
        Train xgboost algorith using mini batch window

        Parameters
        ----------
        X: np.ndarray
            mini batch features array
        y: np.ndarray
            mini batch labels array
        """
        if self.update_strategy == self._DYNAMIC_UPDATE_STRATEGY:
            self._update_on_mini_batch(X, y, self._model_idx)
            self._update_model_idx()
        elif self.update_strategy == self._UPDATE_AND_MAINTAIN_STRATEGY:
            self._update_on_mini_batch(X, y, self._model_idx)
            if not self._model_idx == self.n_models - 1:
                self._model_idx += 1
        elif self.update_strategy == self._REPLACE_STRATEGY:
            booster = self._train_booster(X, y, self._model_idx)
            # Update ensemble
            self[self._model_idx] = booster
            # self._samples_seen += X.shape[0]
            self._update_model_idx()
        else:   # self.update_strategy == self._PUSH_STRATEGY
            booster = self._train_booster(X, y, len(self))
            # Update ensemble
            if len(self) == self.n_models:
                self.pop(0)
            self.append(booster)
            # self._samples_seen += X.shape[0]

    def _train_booster(self, X: np.ndarray, y: np.ndarray, last_model_idx: int) -> TreeBooster:
        """
        Train TreeBooster with given mini batch array

        Parameters
        ----------
        X: np.ndarray
            mini batch features array
        y: np.ndarray
            mini batch labels array
        last_model_idx: int
            index of the model to be trained
        
        Outputs
        ---------
        TreeBooster
            base Booster classifier
        """
        d_mini_batch_train = xgboost.DMatrix(X, y, feature_names=self.features, enable_categorical = True)
        # Get margins from trees in the ensemble
        margins = np.asarray(self.init_margins * d_mini_batch_train.num_row())
        for j in range(last_model_idx):
            margins = np.add(margins, self[j].predict_one(d_mini_batch_train, output_margin=True))
            d_mini_batch_train.set_base_margin(margins)
        booster = self._new_base_model()
        booster.learn_many(d_mini_batch_train, None)
        return booster
    
    def _update_on_mini_batch(self, X: np.ndarray, y: np.ndarray, last_model_idx: int) -> None:
        d_mini_batch_train = xgboost.DMatrix(X, y, feature_names=self.features, enable_categorical = True)
        # Get margins from trees in the ensemble
        margins = np.asarray(self.init_margins * d_mini_batch_train.num_row())
        models_range = last_model_idx if last_model_idx < self.n_models else self.n_models
        for j in range(models_range -1):
            self[j].learn_many(d_mini_batch_train, None)
            margins = np.add(margins, self[j].predict_one(d_mini_batch_train, output_margin=True))
            d_mini_batch_train.set_base_margin(margins)
        self[models_range].learn_many(d_mini_batch_train, None)
    
    @property
    def init_margins(self):
        """This can be overridden if needed"""
        return [self._init_margin]

    def _new_base_model(self):
        return TreeBooster(self._boosting_params)

    def _handle_missing(self, x:dict) -> np.ndarray:
        """
        Cast given dictionary to numpy array handling missing and new features

        Parameters
        -----------
        x: dict
            dictionary representing the given data point (feature:value)

        Outputs
        ----------
        np.ndarray with the given features. Indexes are given by the index of the feature in self.features
        """
        input_features = x.keys()
        for feature in input_features:
            if feature not in self.__features:
                self.__features.append(feature)
        ret_array = np.zeros(self.num_features)
        for i, feature in enumerate(self.__features):
            try:
                ret_array[i] = x[feature]
            except KeyError:
                ret_array[i] = self._X_buffer[-1,i]
        return ret_array

    @property
    def features(self):
        """Features seen by the models"""
        return self.__features

    @property
    def num_features(self):
        """Number of features seen by the model"""
        return len(self.features)
    
    def predict_one(self, x: dict) -> typing.Optional[base.typing.ClfTarget]:
        """
        Return the predicted label of the given data point

        Parameters
        -----------
        x: dict
            dictionary of the given data point

        Outputs
        -----------
        Boosters prediction
        """
        if self.update_strategy == self._REPLACE_STRATEGY:
            trees_in_ensemble = sum(i is not None for i in self)
        elif self.update_strategy == self._DYNAMIC_UPDATE_STRATEGY or self.update_strategy == self._UPDATE_AND_MAINTAIN_STRATEGY:
            trees_in_ensemble = sum(i._booster is not None for i in self)
        else:   # self.update_strategy == self._PUSH_STRATEGY
            trees_in_ensemble = len(self)
        if trees_in_ensemble > 0:
            d_test = xgboost.DMatrix(np.array(list(x.values())).reshape(1,-1), feature_names = x.keys())
            for i in range(trees_in_ensemble - 1):
                margins = self[i].predict_one(d_test, output_margin=True)
                d_test.set_base_margin(margin = margins)
            return self[trees_in_ensemble - 1].predict_one(d_test)[0]
        return self.dynamic_base_prediction
    
    @property
    def base_prediction(self):
        return self.__base_prediction

    @property
    def dynamic_base_prediction(self):
        if self.__base_prediction_method == self._LAST_SAMPLE:
            return self.last_sample
        if self.__base_prediction_method == self._MOST_COMMON:
            return max(self.counter, key=self.counter.get)
        
        return self.__base_prediction
    
    def update_base_prediction(self, y):
        if self.__base_prediction_method == self._LAST_SAMPLE:
            self.last_sample = y
        if self.__base_prediction_method == self._MOST_COMMON:
            self.counter.update((y,))
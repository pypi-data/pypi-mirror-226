from .axgboost_base import BaseXGBoost
from .booster import Constants, TreeBooster

import numpy as np

from river import base
from river import drift

import typing
            
class AXGBoostBinaryClassifier(BaseXGBoost):

    def __init__(
        self,
        n_models: int = 10,
        booster_params: dict = {},
        seed: int = None,
        max_window_size: int = 1000,
        min_window_size: int = None,
        detect_drift: bool = False,
        update_strategy: str = 'replace',
        base_prediction: float = 0.5,
        base_prediction_method: str = "",
        drift_detector: base.DriftDetector = None,
    ):
        super().__init__(n_models, booster_params, seed, max_window_size, min_window_size, update_strategy, base_prediction, base_prediction_method)
        self._boosting_params[Constants.OBJECTIVE] = Constants.BINARY_LOGISTIC
        self.detect_drift = detect_drift
        if self.detect_drift:
            self.__bg_learner = BaseXGBoost(n_models, booster_params, seed, 100, 1, self._REPLACE_STRATEGY, base_prediction, base_prediction_method)
            if self.detect_drift:
                self._drift_indexes = []
                self._drift_detector = drift.ADWIN(delta=0.001) if drift_detector is None else drift_detector
    @property
    def _multiclass(self):
        return False

    def predict_one(self, x: dict) -> typing.Optional[bool]:
        return super().predict_one(x) > self.base_prediction

    def predict_proba_one(self, x: dict) -> typing.Dict[bool, float]:
        pred = super().predict_one(x)
        return {True: pred, False: 1 - pred}
    
    def learn_one(self, x: dict, y: base.typing.ClfTarget) -> "base.Classifier":
        self._samples_seen += 1
        if self.detect_drift:
            self.__bg_learner.learn_one(x,y)
        super().learn_one(x, y)

        # Support for concept drift
        if self.detect_drift:
            self.make_drift_detection(x, y)

        return self
    
    def make_drift_detection(self, x, y):
        try:
            last_idx = self.drift_indexes[-1]
        except:
            last_idx = 0
        if self._samples_seen < (self.n_models * self.max_window_size) + last_idx:
            return
        p = self.predict_one(x)
        # Check for warning
        self._drift_detector.update(not p == y)
        # Check if there was a change
        if self._drift_detector.drift_detected:
            # Reset window size
            self._drift_indexes.append(self._samples_seen)
            self._drift_detector = self._drift_detector.clone()

            if (
                self.update_strategy == self._REPLACE_STRATEGY
                or self.update_strategy == self._DYNAMIC_UPDATE_STRATEGY
                or self.update_strategy == self._UPDATE_AND_MAINTAIN_STRATEGY
            ):
                self._model_idx = 0
            new_models = list(filter(lambda m: m is not None, self.__bg_learner.data))
            for i in range(len(new_models)):
                self.data[i] = new_models[i]
            
            self._X_buffer = self.__bg_learner._X_buffer
            self._y_buffer = self.__bg_learner._y_buffer
            self._reset_window_size()
            self.__bg_learner._reset_window_size()
    
    @property
    def drift_indexes(self):
        if not self.detect_drift:
            return []
        return self._drift_indexes

class AXGBoostClassifier(BaseXGBoost):
    def __init__(
        self,
        classes: list,
        objective: str = None,
        n_models: int = 10,
        booster_params: dict = {},
        seed: int = None,
        max_window_size: int = 1000,
        min_window_size: int = None,
        detect_drift: bool = False,
        update_strategy: str = 'replace',
        base_prediction: float = 0.5,
        base_prediction_method: str = ""
    ):
        """
        Multiclass Adaptive XGBoost for online learning

        Params
        --------
        classes: list
            classes that are going to be seen by models. TODO: dinamic class
        objective: optional str (default None)
            objective to be used. Currently supported "multi:softprob"
        """
        super().__init__(
            n_models=n_models,
            booster_params=booster_params,
            seed=seed,
            min_window_size=min_window_size,
            max_window_size=max_window_size,
            update_strategy=update_strategy,
            base_prediction=base_prediction,
            base_prediction_method=base_prediction_method,
        )
        self.__classes = np.array(classes)
        self.__class_dict = {k:v for k,v in zip(classes, range(len(classes)))}
        self._boosting_params[Constants.OBJECTIVE] = objective if objective is not None else Constants.DEFAULT_MULTICLASS_OBJECTIVE
        self._boosting_params[Constants.NUM_CLASS] = self.__classes.shape[0]
        self.detect_drift = detect_drift
    
    @property
    def classes(self):
        return self.__classes
    @property
    def num_class(self):
        return self.__classes.shape[0]

    def predict_one(self, x: dict) -> typing.Optional[base.typing.ClfTarget]:
        pred = super().predict_one(x)
        try:
            return self.classes[pred.argmax()]
        except AttributeError:
            dyn_pred = self.dynamic_base_prediction
            if isinstance(dyn_pred, str):
                return self.dynamic_base_prediction
            return self.classes[0]

    def predict_proba_one(self, x: dict) -> typing.Dict[base.typing.ClfTarget, float]:
        preds = super().predict_one(x)
        return {k:v for k,v in zip(self.classes, preds)}

    def __convert_y(self, y):
        ret = np.zeros(y.shape)
        for i in range(ret.shape[0]):
            ret[i] = self.__class_dict[y[i]]
        return ret

    def _train_booster(self, X: np.ndarray, y: np.ndarray, last_model_idx: int) -> "TreeBooster":
        return super()._train_booster(X, self.__convert_y(y).astype(int), last_model_idx)
    def _update_on_mini_batch(self, X: np.ndarray, y: np.ndarray, last_model_idx: int) -> None:
        return super()._update_on_mini_batch(X, self.__convert_y(y).astype(int), last_model_idx)

    @BaseXGBoost.init_margins.getter
    def init_margins(self):
        return [[self._init_margin] * self.num_class]

    def make_drift_detection(self, x, y):
        correctly_classifies = self.predict_one(x) == y
        # Check for warning
        self._drift_detector.update(int(not correctly_classifies))
        # Check if there was a change
        if self._drift_detector.drift_detected:
            # Reset window size
            self._drift_indexes.append(self._samples_seen)
            self._reset_window_size()
            if self.update_strategy == self._REPLACE_STRATEGY:
                self._model_idx = 0



__all__ = [
    "AXGBoostBinaryClassifier"
]
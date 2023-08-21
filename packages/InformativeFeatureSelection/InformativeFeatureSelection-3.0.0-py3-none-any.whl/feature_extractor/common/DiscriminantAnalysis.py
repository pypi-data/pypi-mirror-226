from abc import ABC, abstractmethod
from typing import Tuple, Union, List, Any

import numpy as np
from scipy import linalg
from numba import njit
from sklearn.covariance import empirical_covariance


def _cov(X):
    """Estimate covariance matrix (using optional covariance_estimator).
    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        Input data.

    Returns
    -------
    s : ndarray of shape (n_features, n_features)
        Estimated covariance matrix.
    """
    return empirical_covariance(X)


def _class_cov(X, y, priors):
    """Compute weighted within-class covariance matrix.

    The per-class covariance are weighted by the class priors.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        Input data.

    y : array-like of shape (n_samples,) or (n_samples, n_targets)
        Target values.

    priors : array-like of shape (n_classes,)
        Class priors.

    Returns
    -------
    cov : array-like of shape (n_features, n_features)
        Weighted within-class covariance matrix
    """
    classes = np.unique(y)
    cov = np.zeros(shape=(X.shape[1], X.shape[1]))
    for idx, group in enumerate(classes):
        Xg = X[y == group, :]
        cov += priors[idx] * np.atleast_2d(_cov(Xg))
    return cov


@njit
def single_feature_statistic(data: Union[np.ndarray, List[np.ndarray]]) -> Tuple[np.ndarray, np.ndarray, Any]:
    """
    Method optimized for calculation individual criteria for single feature.
    Work twice faster that "numba_calculate_matrices"
    :return: scatter_between value, scatter_within value and individual criteria value
    """
    n_classes = len(data)
    separated_into_classes = data
    aig = np.array([np.mean(obj) for obj in separated_into_classes])

    n_k = np.array([class_samples.shape[0] for class_samples in separated_into_classes])
    n = np.sum(n_k)

    wa = np.sum(aig * n_k / n)

    b = np.sum(n_k * (aig - wa) ** 2)
    w = np.sum(np.array([np.sum((separated_into_classes[i] - aig[i]) ** 2) for i in range(0, n_classes)]))

    _lambda = b / (w + b)
    return b, w, _lambda


@njit
def numba_calculate_matrices(data: Union[np.ndarray, List[np.ndarray]]) -> Tuple[np.ndarray, np.ndarray]:
    """
    The method computes scatter-between and scatter-within matrices using the 
    formula provided in Fakunaga's book, with the only difference being 
    that it uses multiplication by priors instead of a power of a set. 
    However, the result produced by this particular function is different
    from the result that may be obtained using scikit-learn's LDA. 
    As of now, no error has been found in the method.
    
    Usefull link with possible sb, sw calculation formulas:
    https://stats.stackexchange.com/questions/123490/what-is-the-correct-formula-for-between-class-scatter-matrix-in-lda
    """
    n_features = data[0].shape[1]
    
    n_samples_total = 0.0
    for class_samples in data:
        n_samples_total += class_samples.shape[0]
    
    Sb = np.zeros((n_features, n_features))
    Sw = np.zeros((n_features, n_features))
    mean_vectors = np.zeros((len(data), n_features,))
    mean = np.zeros((n_features, 1))

    for class_idx, class_samples in enumerate(data):
        for feature_idx in range(n_features):
            mean_vectors[class_idx, feature_idx] = np.mean(class_samples[::, feature_idx])
    for feature_idx in range(n_features):
        mean[feature_idx] = np.mean(mean_vectors[::, feature_idx])
        
    # St = np.cov(np.vstack(data))
    # return St - Sw, Sw

    for cl in range(len(data)):
        priors = data[cl].shape[0] / n_samples_total
        if data[cl].shape[1] == 1:
            # np.cov does not work with data of shape (N, 1) =)
            Sw += priors * np.cov(data[cl][::, 0].T)
        else:
            # Sw += data[cl].shape[0] * (data[cl] - mean_vectors[cl]).dot((data[cl] - mean_vectors[cl]).T)
            Sw += priors * np.cov(data[cl])

    for cl, mean_v in enumerate(mean_vectors):
        priors = data[cl].shape[0] / n_samples_total
        Sb += (mean_v - mean).dot(np.transpose(mean_v - mean))

    return Sb, Sw


@njit
def numba_calculate_individual_criteria(Sb, Sw):
    return np.diag(Sb) / (np.diag(Sw) + np.diag(Sb))


@njit
def numba_calculate_group_criteria(Sb, Sw):
    try:
        return np.trace(np.linalg.inv(Sw + Sb).dot(Sb))
    except:
        return np.trace(np.linalg.pinv(Sw + Sb).dot(Sb))


class BaseDiscriminantAnalysis(ABC):
    @abstractmethod
    def calculate_individual_criteria(self, Sb: np.ndarray, Sw: np.ndarray) -> np.array:
        pass

    @abstractmethod
    def calculate_group_criteria(self, Sb: np.ndarray, Sw: np.ndarray) -> float:
        pass

    @abstractmethod
    def calculate_matrices(self, data: Union[np.ndarray, List[np.ndarray]]) \
            -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Any]]:
        pass


class DiscriminantAnalysis(BaseDiscriminantAnalysis):
    """
    The first version of DA
    """

    def calculate_individual_criteria(self, Sb: np.ndarray, Sw: np.ndarray) -> np.array:
        return numba_calculate_individual_criteria(Sb, Sw)

    def calculate_group_criteria(self, Sb: np.ndarray, Sw: np.ndarray) -> float:
        return numba_calculate_group_criteria(Sb, Sw)

    def calculate_matrices(self, data: Union[np.ndarray, List[np.ndarray]]) \
            -> Union[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray, Any]]:
        """
        Calculates scatter between and scatter within matrices
        :see Linear discriminant analysis

        :note if data with single feature is provided also returns individual criteria value. It also may be usefully
        with extremely large data

        :param data: numpy array of shape (n_classes, n_samples, n_features) or list of numpy arrays (n_classes, ?,
        n_features)
        :return: tuple of two numpy arrays which represents scatter between and scatter within matrices
        """
        if data[0].shape[1] == 1:
            return single_feature_statistic(data)
        return numba_calculate_matrices(data)



class DiscriminantAnalysisV2(BaseDiscriminantAnalysis):
    """
    The latest implementation of the DA Sb and Sw matrices are computed
    in the same way as scikit. 
    However, it requires additional optimization for speed performance. 
    Additionally, the implementation of group criteria calculation has been changed. 
    Instead of computing invariant matrices, which usually results in NaN values 
    and requires computing pseudo-invariant matrices, 
    the new method is a bit faster and does not produce NaNs.
    """
    
    def calculate_matrices(self, data: Union[np.ndarray, List[np.ndarray]]) -> Tuple[np.ndarray, np.ndarray]:
        if data[0].shape[1] == 1:
            return single_feature_statistic(data)
        
        X = np.vstack(data)
        Y = []
        priors = []
        for i, entry in enumerate(data):
            Y.extend([i] * len(entry))
            priors.append(
                len(entry) / len(X)
            )
        
        covs = _class_cov(X, Y, priors)
        
        Sw = covs
        St = _cov(X)
        Sb = St - Sw
        return Sb, Sw

    def calculate_group_criteria(self, Sb: np.ndarray, Sw: np.ndarray) -> float:
        evals, _ = linalg.eigh(Sb, Sw)
        return np.sum(evals)
    
    def calculate_individual_criteria(self, Sb: np.ndarray, Sw: np.ndarray) -> np.array:
        return numba_calculate_individual_criteria(Sb, Sw)

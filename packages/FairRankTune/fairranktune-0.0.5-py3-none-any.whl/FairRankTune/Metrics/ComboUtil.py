# Script containing methods to aggregate group-level metrics to meta-metrics.
import numpy as np


def __MinMaxRatio(vals):
    """
    Agg via min max ratio.
    :param vals: Numpy array of group level metrics.
    :return: Float score.
    """
    return np.min(vals) / np.max(vals)


def __MaxMinRatio(vals):
    """
    Agg via max min ratio
    :param vals: Numpy array of group level metrics.
    :return: Float score.
    """
    return np.max(vals) / np.min(vals)


def __MaxMinDiff(vals):
    """
    Agg via max min difference.
    :param vals: Numpy array of group level metrics.
    :return: Float score.
    """
    return np.max(vals) - np.min(vals)


def __MaxAbsDiff(vals):
    """
    Agg via max absolute difference.
    :param vals: Numpy array of group level metrics.
    :return: Float score.
    """
    mean = np.mean(vals)
    val = 0
    for i in range(0, len(vals)):
        v = vals[i]
        val_curr = np.abs(v - mean)
        if val_curr > val:
            val = val_curr
    return val


def __MeanAbsDev(vals):
    """
    Agg via mean absolute difference,
    :param vals: Numpy array of group level metrics.
    :return: Float score.
    """
    val = np.sum(np.abs(vals - np.mean(vals))) / len(vals)
    return val


def __LTwo(vals):
    """
    Agg via L2 norm.
    :param vals: Numpy array of group level metrics.
    :return: Float score.
    """
    return np.linalg.norm(vals, 2)


def __Variance(vals):
    """
    Agg via variance.
    :param vals: Numpy array of group level metrics.
    :return: Float score.
    """
    return np.var(vals)

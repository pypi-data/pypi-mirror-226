# import warnings
import numpy as np
from .metrics import concordance_index_censored
from .bess_base import bess_base
from .utilities import (new_data_check, categorical_to_dummy)
from .functions import (BreslowEstimator)
# from .nonparametric import _compute_counts


# def fix_docs(cls):
#     # This function is to inherit the docstring from base class
#     # and avoid unnecessary duplications on description.
#     index = cls.__doc__.find("Examples\n    --------\n")
#     if index != -1:
#         cls.__doc__ = cls.__doc__[:index] + \
#             cls.__bases__[0].__doc__ + cls.__doc__[index:]
#     return cls


class LogisticRegression(bess_base):
    r"""
    Linear-time Adaptive Best-subset Selection (LABS) algorithm
    for logistic regression.
    Parameters
    ----------
    splicing_type: {0, 1}, optional, default=0
        The type of splicing:
        "0" for decreasing by half, "1" for decresing by one.
    important_search : int, optional, default=128
        The size of inactive set during updating active set when splicing.
        It should be a non-positive integer and if important_search=0,
        it would be set as the size of whole inactive set.
    Examples
    --------
    >>> from sklabs.linear import LogisticRegression
    >>> from sklabs.datasets import make_glm_data
    >>> import numpy as np
    >>> np.random.seed(12345)
    >>> data = make_glm_data(n = 100, p = 50, k = 10, family = 'binomial')
    >>> model = LogisticRegression()
    >>> model.fit(data.x, data.y)
    LogisticRegression()
    >>> model.predict(data.x)[1:10]
    array([0, 1, 1, 0, 0, 0, 0, 0, 1])
    """

    def __init__(self, max_iter=20, exchange_num=3,
                 alpha=None, ic_type="ebic", ic_coef=1.0,
                 split_train_test=False,
                 screening_size=-1,
                 always_select=None,
                 primary_model_fit_max_iter=10, primary_model_fit_epsilon=1e-8,
                 approximate_Newton=False,
                 thread=1,
                 sparse_matrix=False,
                 splicing_type=0,
                 important_search=0, init_max_sparsity=None, init_type=1,
                 init_gs_start=4, max_sparsity=None,
                 ):
        super().__init__(
            algorithm_type="abess", model_type="Logistic", normalize_type=2,
            max_iter=max_iter, exchange_num=exchange_num,
            alpha=alpha,
            ic_type=ic_type, ic_coef=ic_coef,
            split_train_test=split_train_test,
            screening_size=screening_size,
            always_select=always_select,
            primary_model_fit_max_iter=primary_model_fit_max_iter,
            primary_model_fit_epsilon=primary_model_fit_epsilon,
            approximate_Newton=approximate_Newton,
            thread=thread,
            sparse_matrix=sparse_matrix,
            splicing_type=splicing_type,
            important_search=important_search,
            init_max_sparsity=init_max_sparsity,
            max_sparsity=max_sparsity,
            init_type=init_type, init_gs_start=init_gs_start,
            _estimator_type='classifier'
        )

    def _more_tags(self):
        return {'binary_only': True,
                'no_validation': True}

    def predict_proba(self, X):
        r"""
        Give the probabilities of new sample
        being assigned to different classes.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix to be predicted.
        Returns
        -------
        proba : array-like, shape(n_samples, 2)
            Returns the probabilities for class "0" and "1"
            on given X.
        """
        X = new_data_check(self, X)

        intercept_ = np.ones(X.shape[0]) * self.intercept_
        xbeta = X.dot(self.coef_) + intercept_
        proba = np.exp(xbeta) / (1 + np.exp(xbeta))
        return np.vstack((np.ones(X.shape[0]) - proba, proba)).T

    def predict(self, X):
        r"""
        This function predicts class label for given data.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix to be predicted.
        Returns
        -------
        y : array-like, shape(n_samples,)
            Predict class labels (0 or 1) for samples in X.
        """
        X = new_data_check(self, X)

        intercept_ = np.ones(X.shape[0]) * self.intercept_
        xbeta = X.dot(self.coef_) + intercept_
        y = np.repeat(self.classes_[0], xbeta.size)
        if self.classes_.size == 2:
            y[xbeta > 0] = self.classes_[1]
        return y

    def score(self, X, y):
        r"""
        Give new data, and it returns the entropy function.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix.
        y : array-like, shape(n_samples,)
            Real class labels (0 or 1) for X.
        Returns
        -------
        score : float
            The value of entropy function under given data.
        """
        X, y = new_data_check(self, X, y)

        intercept_ = np.ones(X.shape[0]) * self.intercept_
        xbeta = X.dot(self.coef_) + intercept_
        xbeta[xbeta > 30] = 30
        xbeta[xbeta < -30] = -30
        pr = np.exp(xbeta) / (1 + np.exp(xbeta))
        return (y * np.log(pr) +
                (np.ones(X.shape[0]) - y) *
                np.log(np.ones(X.shape[0]) - pr)).sum()


class LinearRegression(bess_base):
    r"""
    Linear-time Adaptive Best-subset Selection (LABS) algorithm
    for linear regression.
    Parameters
    ----------
    splicing_type: {0, 1}, optional, default=0
        The type of splicing:
        "0" for decreasing by half, "1" for decresing by one.
    important_search : int, optional, default=128
        The size of inactive set during updating active set when splicing.
        It should be a non-positive integer and if important_search=0,
        it would be set as the size of whole inactive set.
    Examples
    --------
    >>> from sklabs.linear import LinearRegression
    >>> from sklabs.datasets import make_glm_data
    >>> import numpy as np
    >>> np.random.seed(12345)
    >>> data = make_glm_data(n = 300, p = 20, k = 6, family = 'gaussian')
    >>> model = LinearRegression()
    >>> model.fit(data.x, data.y)
    LinearRegression()
    >>> model.predict(data.x)[1:10]
    array([ 124.65402724,  598.85321188, -207.77965619,   12.75115769,
            414.74256926,  473.14864107,  214.59591836,   66.40746519,
            61.16806709])
    """

    def __init__(self, max_iter=20, exchange_num=3,
                 alpha=None,
                 ic_type="ebic", ic_coef=1.0, split_train_test=False,
                 screening_size=-1,
                 always_select=None,
                 thread=1, covariance_update=False,
                 sparse_matrix=False,
                 splicing_type=0,
                 important_search=0, init_max_sparsity=None, init_type=1,
                 init_gs_start=4, max_sparsity=None,
                 # primary_model_fit_max_iter=10,
                 # primary_model_fit_epsilon=1e-8,
                 # approximate_Newton=False
                 ):
        super().__init__(
            algorithm_type="abess", model_type="Lm", normalize_type=1,
            max_iter=max_iter, exchange_num=exchange_num,
            alpha=alpha,
            ic_type=ic_type, ic_coef=ic_coef,
            split_train_test=split_train_test,
            screening_size=screening_size,
            always_select=always_select,
            thread=thread, covariance_update=covariance_update,
            sparse_matrix=sparse_matrix,
            splicing_type=splicing_type,
            important_search=important_search,
            init_max_sparsity=init_max_sparsity,
            max_sparsity=max_sparsity,
            init_type=init_type, init_gs_start=init_gs_start,
            _estimator_type='regressor'
        )

    def _more_tags(self):
        return {'multioutput': False,
                'poor_score': True}

    def predict(self, X):
        r"""
        Predict on given data.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix to be predicted.
        Returns
        -------
        y : array-like, shape(n_samples,)
            Prediction of the mean on given X.
        """
        X = new_data_check(self, X)

        intercept_ = np.ones(X.shape[0]) * self.intercept_
        return X.dot(self.coef_) + intercept_

    def score(self, X, y):
        r"""
        Give data, and it returns the prediction error.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix.
        y : array-like, shape(n_samples, p_features)
            Real response for given X.
        Returns
        -------
        score : float
            Prediction error.
        """
        X, y = new_data_check(self, X, y)
        y_pred = self.predict(X)
        return -((y - y_pred) * (y - y_pred)).sum()


class CoxPHSurvivalAnalysis(bess_base, BreslowEstimator):
    r"""
    Linear-time Adaptive Best-subset Selection (LABS) algorithm
    for Cox proportional hazards model.
    Parameters
    ----------
    splicing_type: {0, 1}, optional, default=0
        The type of splicing:
        "0" for decreasing by half, "1" for decresing by one.
    important_search : int, optional, default=128
        The size of inactive set during updating active set when splicing.
        It should be a non-positive integer and if important_search=0,
        it would be set as the size of whole inactive set.
    Examples
    --------
    >>> from sklabs.linear import CoxPHSurvivalAnalysis
    >>> from sklabs.datasets import make_glm_data
    >>> import numpy as np
    >>> np.random.seed(12345)
    >>> data = make_glm_data(n = 300, p = 20, k = 6, family = 'cox')
    censoring rate:0.62
    >>> model = CoxPHSurvivalAnalysis()
    >>> model.fit(data.x, data.y)
    CoxPHSurvivalAnalysis()
    >>> model.predict(data.x)[1:10]
    array([1.11652657e+05, 4.63832609e+13, 2.13250068e-06, 7.26072065e-02,
        1.57555939e+10, 1.50477579e+12, 4.41887874e+04, 5.95076978e-01,
        3.94839859e+00])
    """

    def __init__(self, max_iter=20, exchange_num=3,
                 alpha=None,
                 ic_type="ebic", ic_coef=1.0, split_train_test=False,
                 screening_size=-1,
                 always_select=None,
                 primary_model_fit_max_iter=10, primary_model_fit_epsilon=1e-8,
                 approximate_Newton=False,
                 thread=1,
                 sparse_matrix=False,
                 splicing_type=0,
                 important_search=0, init_max_sparsity=None, init_type=1,
                 init_gs_start=4, max_sparsity=None
                 ):
        super().__init__(
            algorithm_type="abess", model_type="Cox", normalize_type=3,
            max_iter=max_iter, exchange_num=exchange_num,
            alpha=alpha,
            ic_type=ic_type, ic_coef=ic_coef,
            split_train_test=split_train_test,
            screening_size=screening_size,
            always_select=always_select,
            primary_model_fit_max_iter=primary_model_fit_max_iter,
            primary_model_fit_epsilon=primary_model_fit_epsilon,
            approximate_Newton=approximate_Newton,
            thread=thread,
            sparse_matrix=sparse_matrix,
            splicing_type=splicing_type,
            important_search=important_search,
            init_max_sparsity=init_max_sparsity,
            max_sparsity=max_sparsity,
            init_type=init_type, init_gs_start=init_gs_start,
            baseline_model=BreslowEstimator()
        )

    def _more_tags(self):
        # Note: We ignore estimator's check here because it would pass
        # an 1-column `y` for testing, but for `CoxPHSurvivalAnalysis()`,
        # 2-column `y` should be given (one for time, another for censoring).
        return {'_skip_test': True}

    def predict(self, X):
        r"""
        Returns the time-independent part of hazard function,
        i.e. :math:`\exp(X\beta)` on given data.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix to be predicted.
        Returns
        -------
        y : array-like, shape(n_samples,)
            Return :math:`\exp(X\beta)`.
        """
        X = new_data_check(self, X)

        return np.exp(X.dot(self.coef_))

    def score(self, X, y):
        r"""
        Give data, and it returns C-index.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix.
        y : array-like, shape(n_samples, p_features)
            Real response for given X.
        Returns
        -------
        score : float
            C-index.
        """
        X, y = new_data_check(self, X, y)
        risk_score = X.dot(self.coef_)
        y = np.array(y)
        result = concordance_index_censored(
            np.array(y[:, 1], np.bool_), y[:, 0], risk_score)
        return result[0]

    def predict_survival_function(self, X):
        r"""
        Predict survival function.
        The survival function for an individual
        with feature vector :math:`x` is defined as
        .. math::
            S(t \mid x) = S_0(t)^{\exp(x^\top \beta)} ,
        where :math:`S_0(t)` is the baseline survival function,
        estimated by Breslow's estimator.
        Parameters
        ----------
        X : array-like, shape = (n_samples, n_features)
            Data matrix.
        Returns
        -------
        survival : ndarray of :class:`StepFunction`, shape = (n_samples,)
            Predicted survival functions.
        """
        return self.baseline_model.get_survival_function(
            np.log(self.predict(X)))


class PoissonRegression(bess_base):
    r"""
    Linear-time Adaptive Best-subset Selection (LABS) algorithm
    for Poisson regression.
    Parameters
    ----------
    splicing_type: {0, 1}, optional, default=0
        The type of splicing:
        "0" for decreasing by half, "1" for decresing by one.
    important_search : int, optional, default=128
        The size of inactive set during updating active set when splicing.
        It should be a non-positive integer and if important_search=0,
        it would be set as the size of whole inactive set.
    Examples
    --------
    >>> from sklabs.linear import PoissonRegression
    >>> from sklabs.datasets import make_glm_data
    >>> import numpy as np
    >>> np.random.seed(12345)
    >>> data = make_glm_data(n = 300, p = 20, k = 6, family = 'poisson')
    >>> model = PoissonRegression()
    >>> model.fit(data.x, data.y)
    PoissonRegression()
    >>> model.predict(data.x)[1:10]
    array([ 2.94058888, 49.42747087,  0.20824597,  1.14922475, 13.20158449,
        33.0182481 ,  3.32663832,  1.24227759,  1.5788576 ])
    """

    def __init__(self, max_iter=20, exchange_num=3,
                 alpha=None,
                 ic_type="ebic", ic_coef=1.0, split_train_test=False,
                 screening_size=-1,
                 always_select=None,
                 primary_model_fit_max_iter=10, primary_model_fit_epsilon=1e-8,
                 thread=1,
                 sparse_matrix=False,
                 splicing_type=0,
                 important_search=0, init_max_sparsity=None, init_type=1,
                 init_gs_start=4, max_sparsity=None
                 ):
        super().__init__(
            algorithm_type="abess", model_type="Poisson", normalize_type=2,
            max_iter=max_iter, exchange_num=exchange_num,
            alpha=alpha,
            ic_type=ic_type, ic_coef=ic_coef,
            split_train_test=split_train_test,
            screening_size=screening_size,
            always_select=always_select,
            primary_model_fit_max_iter=primary_model_fit_max_iter,
            primary_model_fit_epsilon=primary_model_fit_epsilon,
            thread=thread,
            sparse_matrix=sparse_matrix,
            splicing_type=splicing_type,
            important_search=important_search,
            init_max_sparsity=init_max_sparsity,
            max_sparsity=max_sparsity,
            init_type=init_type, init_gs_start=init_gs_start,
            _estimator_type='regressor'
        )

    def _more_tags(self):
        return {"poor_score": True}

    def predict(self, X):
        r"""
        Predict on given data.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix to be predicted.
        Returns
        -------
        y : array-like, shape(n_samples,)
            Prediction of the mean on X.
        """
        X = new_data_check(self, X)

        intercept_ = np.ones(X.shape[0]) * self.intercept_
        xbeta_exp = np.exp(X.dot(self.coef_) + intercept_)
        return xbeta_exp

    def score(self, X, y):
        r"""
        Give new data, and it returns the prediction error.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix.
        y : array-like, shape(n_samples, p_features)
            Real response for given X.
        Returns
        -------
        score : float
            Prediction error.
        """
        X, y = new_data_check(self, X, y)

        intercept_ = np.ones(X.shape[0]) * self.intercept_
        eta = X.dot(self.coef_) + intercept_
        exp_eta = np.exp(eta)
        return (y * eta - exp_eta).sum()


class MultiTaskRegression(bess_base):
    r"""
    Linear-time Adaptive Best-subset Selection (LABS) algorithm
    for multitasklearning.
    Parameters
    ----------
    splicing_type: {0, 1}, optional, default=0
        The type of splicing:
        "0" for decreasing by half, "1" for decresing by one.
    important_search : int, optional, default=128
        The size of inactive set during updating active set when splicing.
        It should be a non-positive integer and if important_search=0,
        it would be set as the size of whole inactive set.
    Examples
    --------
    >>> from sklabs.linear import MultiTaskRegression
    >>> from sklabs.datasets import make_multivariate_glm_data
    >>> import numpy as np
    >>> np.random.seed(12345)
    >>> data = make_multivariate_glm_data(
    ...     n = 100, p = 50, k = 10, M = 3, family = 'multigaussian')
    >>> model = MultiTaskRegression()
    >>> model.fit(data.x, data.y)
    MultiTaskRegression()
    >>> model.predict(data.x)[1:5,]
    array([[  8.99687125,  -5.74834275,  17.67719359],
        [ 27.60141854, -28.89527087, -13.13808967],
        [ 13.63623637,  -0.81303274,   5.02318398],
        [-28.48945127,  21.52084036,  14.86113707]])
    """

    def __init__(self, max_iter=20, exchange_num=3,
                 alpha=None,
                 ic_type="ebic", ic_coef=1.0, split_train_test=False,
                 screening_size=-1,
                 always_select=None,
                 thread=1, covariance_update=False,
                 sparse_matrix=False,
                 splicing_type=0,
                 important_search=0, init_max_sparsity=None, init_type=1,
                 init_gs_start=4, max_sparsity=None
                 ):
        super().__init__(
            algorithm_type="abess", model_type="Multigaussian",
            normalize_type=1,
            max_iter=max_iter, exchange_num=exchange_num,
            alpha=alpha,
            ic_type=ic_type, ic_coef=ic_coef,
            split_train_test=split_train_test,
            screening_size=screening_size,
            always_select=always_select,
            thread=thread, covariance_update=covariance_update,
            sparse_matrix=sparse_matrix,
            splicing_type=splicing_type,
            important_search=important_search,
            init_max_sparsity=init_max_sparsity,
            max_sparsity=max_sparsity,
            init_type=init_type, init_gs_start=init_gs_start,
            _estimator_type='regressor'
        )

    def _more_tags(self):
        return {'multioutput': True,
                'multioutput_only': True,
                'poor_score': True}

    def predict(self, X):
        r"""
        Prediction of the mean of each response on given data.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix to be predicted.
        Returns
        -------
        y : array-like, shape(n_samples, M_responses)
            Prediction of the mean of each response on given X.
            Each column indicates one response.
        """
        X = new_data_check(self, X)

        intercept_ = np.repeat(
            self.intercept_[np.newaxis, ...], X.shape[0], axis=0)
        y_pred = X.dot(self.coef_) + intercept_
        if len(y_pred.shape) == 1:
            y_pred = y_pred[:, np.newaxis]
        return y_pred

    def score(self, X, y):
        r"""
        Give data, and it returns the prediction error.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix.
        y : array-like, shape(n_samples, M_responses)
            Real responses for given X.
        Returns
        -------
        score : float
            Prediction error.
        """
        X, y = new_data_check(self, X, y)

        y_pred = self.predict(X)
        return -((y - y_pred) * (y - y_pred)).sum()


class MultinomialRegression(bess_base):
    r"""
    Linear-time Adaptive Best-subset Selection (LABS) algorithm
    for multiclassification problem.
    Parameters
    ----------
    splicing_type: {0, 1}, optional, default=0
        The type of splicing:
        "0" for decreasing by half, "1" for decresing by one.
    important_search : int, optional, default=128
        The size of inactive set during updating active set when splicing.
        It should be a non-positive integer and if important_search=0,
        it would be set as the size of whole inactive set.
    Examples
    --------
    >>> from sklabs.linear import MultinomialRegression
    >>> from sklabs.datasets import make_multivariate_glm_data
    >>> import numpy as np
    >>> np.random.seed(12345)
    >>> data = make_multivariate_glm_data(
    ...     n = 100, p = 50, k = 10, M = 3, family = 'multinomial')
    >>> model = MultinomialRegression()
    >>> model.fit(data.x, data.y)
    MultinomialRegression()
    >>> model.predict(data.x)[1:10,]
    array([2, 0, 0, 1, 1, 1, 1, 1, 0])
    """

    def __init__(self, max_iter=20, exchange_num=3,
                 alpha=None,
                 ic_type="ebic", ic_coef=1.0, split_train_test=False,
                 screening_size=-1,
                 always_select=None,
                 primary_model_fit_max_iter=10,
                 primary_model_fit_epsilon=1e-8,
                 #  approximate_Newton=False,
                 thread=1,
                 sparse_matrix=False,
                 splicing_type=0,
                 important_search=0, init_max_sparsity=None, init_type=1,
                 init_gs_start=4, max_sparsity=None
                 ):
        super().__init__(
            algorithm_type="abess", model_type="Multinomial", normalize_type=2,
            max_iter=max_iter, exchange_num=exchange_num,
            alpha=alpha,
            ic_type=ic_type, ic_coef=ic_coef,
            split_train_test=split_train_test,
            screening_size=screening_size,
            always_select=always_select,
            primary_model_fit_max_iter=primary_model_fit_max_iter,
            primary_model_fit_epsilon=primary_model_fit_epsilon,
            approximate_Newton=True,
            thread=thread,
            sparse_matrix=sparse_matrix,
            splicing_type=splicing_type,
            important_search=important_search,
            init_max_sparsity=init_max_sparsity,
            max_sparsity=max_sparsity,
            init_type=init_type, init_gs_start=init_gs_start,
            _estimator_type='classifier'
        )

    def _more_tags(self):
        return {'multilabel': False,
                # 'multioutput_only': True,
                'no_validation': True,
                'poor_score': True}

    def predict_proba(self, X):
        r"""
        Give the probabilities of new data being assigned to different classes.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix to be predicted.
        Returns
        -------
        proba : array-like, shape(n_samples, M_responses)
            Returns the probability of given samples for each class.
            Each column indicates one class.
        """
        X = new_data_check(self, X)

        intercept_ = np.repeat(
            self.intercept_[np.newaxis, ...], X.shape[0], axis=0)
        xbeta = X.dot(self.coef_) + intercept_
        eta = np.exp(xbeta)
        pr = np.zeros_like(xbeta)
        for i in range(X.shape[0]):
            pr[i, :] = eta[i, :] / np.sum(eta[i, :])
        return pr

    def predict(self, X):
        r"""
        Return the most possible class for given data.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix to be predicted.
        Returns
        -------
        y : array-like, shape(n_samples, M_responses)
            Predict class labels for samples in X.
            Each row contains only one "1", and its column index is the
            predicted class for related sample.
        """
        X = new_data_check(self, X)

        intercept_ = np.repeat(
            self.intercept_[np.newaxis, ...], X.shape[0], axis=0)
        xbeta = X.dot(self.coef_) + intercept_
        max_item = np.argmax(xbeta, axis=1)
        # y_pred = np.zeros_like(xbeta)
        # for i in range(X.shape[0]):
        #     y_pred[i, max_item[i]] = 1
        cl = getattr(self, "classes_", np.arange(self.coef_.shape[1]))
        return cl[max_item]

    def score(self, X, y):
        """
        Give new data, and it returns the entropy function.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Test data.
        y : array-like, shape(n_samples, M_responses)
            Test response (dummy variables of real class).
        Returns
        -------
        score : float
            entropy function
        """
        X, y = new_data_check(self, X, y)
        if (len(y.shape) == 1 or y.shape[1] == 1):
            y, _ = categorical_to_dummy(y.squeeze())

        pr = self.predict_proba(X)
        return np.sum(y * np.log(pr))


class GammaRegression(bess_base):
    r"""
    Linear-time Adaptive Best-subset Selection (LABS) algorithm
    for Gamma regression.
    Parameters
    ----------
    splicing_type: {0, 1}, optional, default=0
        The type of splicing:
        "0" for decreasing by half, "1" for decresing by one.
    important_search : int, optional, default=128
        The size of inactive set during updating active set when splicing.
        It should be a non-positive integer and if important_search=0,
        it would be set as the size of whole inactive set.
    Examples
    --------
    >>> from sklabs.linear import GammaRegression
    >>> from sklabs.datasets import make_glm_data
    >>> import numpy as np
    >>> np.random.seed(12345)
    >>> data = make_glm_data(n = 300, p = 20, k = 6, family = 'gamma')
    >>> model = GammaRegression()
    >>> model.fit(data.x, data.y)
    GammaRegression()
    >>> model.predict(data.x)[1:5]
    array([2.77499542e+22, 2.77499542e+22, 2.77499542e+22, 2.77499542e+22])
    """

    def __init__(self, max_iter=20, exchange_num=3,
                 alpha=None, ic_type="ebic", ic_coef=1.0,
                 split_train_test=False,
                 screening_size=-1,
                 always_select=None,
                 primary_model_fit_max_iter=10, primary_model_fit_epsilon=1e-8,
                 thread=1,
                 sparse_matrix=False,
                 splicing_type=0,
                 important_search=0, init_max_sparsity=None, init_type=1,
                 init_gs_start=4, max_sparsity=None
                 ):
        super().__init__(
            algorithm_type="abess", model_type="Gamma", normalize_type=2,
            max_iter=max_iter, exchange_num=exchange_num,
            alpha=alpha,
            ic_type=ic_type, ic_coef=ic_coef,
            split_train_test=split_train_test,
            screening_size=screening_size,
            always_select=always_select,
            primary_model_fit_max_iter=primary_model_fit_max_iter,
            primary_model_fit_epsilon=primary_model_fit_epsilon,
            thread=thread,
            sparse_matrix=sparse_matrix,
            splicing_type=splicing_type,
            important_search=important_search,
            init_max_sparsity=init_max_sparsity,
            max_sparsity=max_sparsity,
            init_type=init_type, init_gs_start=init_gs_start,
            _estimator_type='regressor'
        )

    def _more_tags(self):
        return {'poor_score': True}

    def predict(self, X):
        r"""
        Predict on given data.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix to be predicted.
        Returns
        -------
        y : array-like, shape(n_samples,)
            Prediction of the mean on given X.
        """
        X = new_data_check(self, X)

        intercept_ = np.ones(X.shape[0]) * self.intercept_
        xbeta_exp = np.exp(X.dot(self.coef_) + intercept_)
        return xbeta_exp

    def score(self, X, y, weights=None):
        r"""
        Give new data, and it returns the prediction error.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix.
        y : array-like, shape(n_samples, p_features)
            Real response for given X.
        Returns
        -------
        score : float
            Prediction error.
        """
        if weights is None:
            X = np.array(X)
            weights = np.ones(X.shape[0])
        X, y, weights = new_data_check(self, X, y, weights)

        def deviance(y, y_pred):
            dev = 2 * (np.log(y_pred / y) + y / y_pred - 1)
            return np.sum(weights * dev)

        y_pred = self.predict(X)
        y_mean = np.average(y, weights=weights)
        dev = deviance(y, y_pred)
        dev_null = deviance(y, y_mean)
        return 1 - dev / dev_null


class OrdinalRegression(bess_base):
    r"""
    Linear-time Adaptive Best-subset Selection (LABS) algorithm
    for ordinal regression problem.
    Parameters
    ----------
    splicing_type: {0, 1}, optional, default=0
        The type of splicing:
        "0" for decreasing by half, "1" for decresing by one.
    important_search : int, optional, default=128
        The size of inactive set during updating active set when splicing.
        It should be a non-positive integer and if important_search=0,
        it would be set as the size of whole inactive set.
    Examples
    --------
    >>> from sklabs.linear import OrdinalRegression
    >>> from sklabs.datasets import make_glm_data
    >>> import numpy as np
    >>> np.random.seed(12345)
    >>> data = make_glm_data(n = 300, p = 20, k = 6, family = 'ordinal')
    >>> model = OrdinalRegression()
    >>> model.fit(data.x, data.y)
    OrdinalRegression()
    >>> model.predict(data.x)[1:5]
    array([1, 0, 2, 1])
    """

    def __init__(self, max_iter=20, exchange_num=3,
                 alpha=None,
                 ic_type="ebic", ic_coef=1.0, split_train_test=False,
                 screening_size=-1,
                 always_select=None,
                 primary_model_fit_max_iter=10,
                 primary_model_fit_epsilon=1e-8,
                 approximate_Newton=False,
                 thread=1,
                 sparse_matrix=False,
                 splicing_type=0,
                 important_search=0, init_max_sparsity=None, init_type=1,
                 init_gs_start=4, max_sparsity=None
                 ):
        super().__init__(
            algorithm_type="abess", model_type="Ordinal", normalize_type=2,
            max_iter=max_iter, exchange_num=exchange_num,
            alpha=alpha,
            ic_type=ic_type, ic_coef=ic_coef,
            split_train_test=split_train_test,
            screening_size=screening_size,
            always_select=always_select,
            primary_model_fit_max_iter=primary_model_fit_max_iter,
            primary_model_fit_epsilon=primary_model_fit_epsilon,
            approximate_Newton=approximate_Newton,
            thread=thread,
            sparse_matrix=sparse_matrix,
            splicing_type=splicing_type,
            important_search=important_search,
            init_max_sparsity=init_max_sparsity,
            max_sparsity=max_sparsity,
            init_type=init_type, init_gs_start=init_gs_start,
            # _estimator_type="regressor"
        )

    def predict_proba(self, X):
        r"""
        Give the probabilities of new sample
        being assigned to different classes.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix to be predicted.
        Returns
        -------
        proba : array-like, shape(n_samples, M_classes)
            Returns the probabilities for each class
            on given X.
        """
        X = new_data_check(self, X)
        M = len(self.intercept_)
        cdf = (X @ self.coef_)[:, np.newaxis] + self.intercept_
        cdf = 1 / (1 + np.exp(-cdf))
        proba = np.zeros_like(cdf)
        proba[:, 0] = cdf[:, 0]
        proba[:, 1:(M - 1)] = cdf[:, 1:(M - 1)] - cdf[:, 0:(M - 2)]
        proba[:, M - 1] = 1 - cdf[:, M - 1]
        return proba

    def predict(self, X):
        r"""
        Return the most possible class label (start from 0) for given data.
        Parameters
        ----------
        X : array-like, shape(n_samples, p_features)
            Sample matrix to be predicted.
        Returns
        -------
        y : array-like, shape(n_samples,)
            Predict class labels for samples in X.
        """
        proba = self.predict_proba(X)
        return np.argmax(proba, axis=1)

    # def score(self, X, y):
    #     """
    #     Give new data, and it returns the entropy function.

    #     Parameters
    #     ----------
    #     X : array-like, shape(n_samples, p_features)
    #         Test data.
    #     y : array-like, shape(n_samples, M_responses)
    #         Test response (dummy variables of real class).

    #     Returns
    #     -------
    #     score : float
    #         entropy function
    #     """
    #     X, y = new_data_check(self, X, y)
    #     if len(y.shape) == 1:
    #         y = categorical_to_dummy(y)

    #     return ???

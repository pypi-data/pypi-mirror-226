import numbers
import warnings
import numpy as np
# import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_X_y
from sklearn.exceptions import DataConversionWarning
from .pybind_cabess import pywrap_GLM
from .utilities import categorical_to_dummy


class bess_base(BaseEstimator):
    # attributes
    coef_ = None
    intercept_ = None
    ic_ = 0
    train_loss_ = 0
    test_loss_ = 0

    def __init__(
        self,
        algorithm_type,
        model_type,
        normalize_type,
        max_iter=20,
        exchange_num=3,
        alpha=None,
        ic_type="ebic",
        ic_coef=1.0,
        split_train_test=False,
        screening_size=-1,
        always_select=None,
        primary_model_fit_max_iter=10,
        primary_model_fit_epsilon=1e-8,
        approximate_Newton=False,
        thread=1,
        covariance_update=False,
        sparse_matrix=False,
        splicing_type=0,
        important_search=0,
        init_type=1,
        init_max_sparsity=None,
        init_gs_start=4,
        max_sparsity=None,
        # lambda_min=None, lambda_max=None,
        # early_stop=False, n_lambda=100,
        baseline_model=None,
        _estimator_type=None
    ):
        self.algorithm_type = algorithm_type
        self.model_type = model_type
        self.normalize_type = normalize_type
        self.max_iter = max_iter
        self.exchange_num = exchange_num
        self.alpha = alpha
        self.n_features_in_: int
        self.n_iter_: int
        # self.lambda_min = None
        # self.lambda_max = None
        # self.n_lambda = 100
        self.ic_type = ic_type
        self.ic_coef = ic_coef
        self.split_train_test = split_train_test
        self.screening_size = screening_size
        self.always_select = always_select
        self.primary_model_fit_max_iter = primary_model_fit_max_iter
        self.primary_model_fit_epsilon = primary_model_fit_epsilon
        self.early_stop = False
        self.approximate_Newton = approximate_Newton
        self.thread = thread
        self.covariance_update = covariance_update
        self.sparse_matrix = sparse_matrix
        self.splicing_type = splicing_type
        self.important_search = important_search
        self.baseline_model = baseline_model
        self._estimator_type = _estimator_type
        self.classes_: np.ndarray
        self.max_sparsity = max_sparsity
        self.init_max_sparsity = init_max_sparsity
        self.init_type = init_type
        self.init_gs_start = init_gs_start

    def fit(self,
            X=None,
            y=None,
            is_normal=True,
            weight=None,
            group=None,
            train_test_id=None,
            A_init=None,
            return_path=False):
        r"""
        The fit function is used to transfer
        the information of data and return the fit result.

        Parameters
        ----------
        X : array-like of shape(n_samples, p_features)
            Training data matrix. It should be a numpy array.
        y : array-like of shape(n_samples,) or (n_samples, M_responses)
            Training response values. It should be a numpy array.

            - For regression problem, the element of y should be float.
            - For classification problem,
              the element of y should be either 0 or 1.
              In multinomial regression,
              the p features are actually dummy variables.
            - For survival data, y should be a :math:`n \times 2` array,
              where the columns indicates "censoring" and "time",
              respectively.

        is_normal : bool, optional, default=True
            whether normalize the variables array
            before fitting the algorithm.
        weight : array-like, shape (n_samples,), optional, default=np.ones(n)
            Individual weights for each sample. Only used for is_weight=True.
        group : int, optional, default=np.ones(p)
            The group index for each variable.
        cv_fold_id: array-like, shape (n_samples,), optional, default=None
            An array indicates different folds in CV.
            Samples in the same fold should be given the same number.
        """

        # Input check & init:
        X, y = check_X_y(X,
                         y,
                         accept_sparse=True,
                         multi_output=True,
                         #  y_numeric=True,
                         dtype='numeric')

        if isinstance(X, (coo_matrix, csr_matrix)):
            self.sparse_matrix = True

        # Sort for Cox
        if self.model_type == "Cox":
            X = X[y[:, 0].argsort()]
            y = y[y[:, 0].argsort()]
            time = y[:, 0].reshape(-1)
            y = y[:, 1].reshape(-1)

        # Dummy y & classes
        if self.model_type == "Logistic":
            y, self.classes_ = categorical_to_dummy(y.squeeze())
            if self.classes_.size > 2:
                raise ValueError("Up to 2 classes can be given in y.")
            if self.classes_.size == 1:
                y = np.zeros(X.shape[0])
            else:
                y = y[:, 1]
        elif (self.model_type in ("Multinomial", "Ordinal")
                and (len(y.shape) == 1 or y.shape[1] == 1)):
            y, self.classes_ = categorical_to_dummy(y.squeeze())
            if self.classes_.size == 1:
                # add a useless label
                y = np.hstack((np.zeros((X.shape[0], 1)), y))
                self.classes_ = np.insert(self.classes_, 0, 0)

        # multi_output warning
        if self.model_type in (
                'Lm', 'Logistic', 'Poisson', 'Gamma'):
            if len(y.shape) > 1:
                warnings.warn(
                    "A column-vector y was passed "
                    "when a 1d array was expected",
                    DataConversionWarning)
                y = y.reshape(-1)

        # Init
        n = X.shape[0]
        p = X.shape[1]
        self.n_features_in_ = p

        if y.ndim == 1:
            M = 1
            y = y.reshape(len(y), 1)
        else:
            M = y.shape[1]

        # Algorithm_type: abess
        if self.algorithm_type == "abess":
            algorithm_type_int = 6
        else:
            raise ValueError("algorithm_type should not be " +
                             str(self.algorithm_type))

        # Model_type: lm, logit, poiss, cox, multi-gaussian, multi-nomial
        if self.model_type == "Lm":
            model_type_int = 1
        elif self.model_type == "Logistic":
            model_type_int = 2
        elif self.model_type == "Poisson":
            model_type_int = 3
        elif self.model_type == "Cox":
            model_type_int = 4
        elif self.model_type == "Multigaussian":
            model_type_int = 5
        elif self.model_type == "Multinomial":
            model_type_int = 6
        elif self.model_type == 'Gamma':
            model_type_int = 8
        elif self.model_type == 'Ordinal':
            model_type_int = 9
        else:
            raise ValueError("model_type should not be " +
                             str(self.model_type))

        # ic_type: aic, bic, gic, ebic, cv
        if self.ic_type == "aic":
            tune_type_int = 1
        elif self.ic_type == "bic":
            tune_type_int = 2
        elif self.ic_type == "gic":
            tune_type_int = 3
        elif self.ic_type == "ebic":
            tune_type_int = 4
        elif self.ic_type == "hic":
            tune_type_int = 5
        else:
            raise ValueError(
                "ic_type should be \"aic\", \"bic\", \"ebic\","
                " \"gic\" or \"hic\".")

        # # cv
        # if (not isinstance(self.cv, int) or self.cv <= 0):
        #     raise ValueError("cv should be an positive integer.")
        # if self.cv > n:
        #     raise ValueError("cv should be smaller than n.")

        # # cv_fold_id
        # if cv_fold_id is None:
        #     cv_fold_id = np.array([], dtype="int32")
        # else:
        #     cv_fold_id = np.array(cv_fold_id, dtype="int32")
        #     if cv_fold_id.ndim > 1:
        #         raise ValueError("group should be an 1D array of integers.")
        #     if cv_fold_id.size != n:
        #         raise ValueError(
        #             "The length of group should be equal to X.shape[0].")
        #     if len(set(cv_fold_id)) != self.cv:
        #         raise ValueError(
        #             "The number of different masks should be equal to `cv`.")

        # max_sparsity
        if self.max_sparsity is None:
            max_s = p
        else:
            max_s = self.max_sparsity

        # init_max_sparsity
        if self.init_max_sparsity is None:
            init_max_s = int(
                max(min(p, int(n / (np.log(np.log(n)) * np.log(p)))), 1))
        elif isinstance(self.init_max_sparsity, str):
            init_max_s = int(
                max(min(p, int(n / (np.log(np.log(n)) * np.log(p)))), 1))
            if self.init_max_sparsity.startswith('+'):
                init_max_s += int(self.init_max_sparsity[1:])
            elif self.init_max_sparsity.startswith('-'):
                init_max_s -= int(self.init_max_sparsity[1:])
        else:
            init_max_s = self.init_max_sparsity
        init_max_s = min(init_max_s, max_s)

        # A_init
        if A_init is None:
            A_init = np.array([], dtype="int32")
        else:
            A_init = np.array(A_init, dtype="int32")
            if A_init.ndim > 1:
                raise ValueError("The initial active set should be "
                                 "an 1D array of integers.")
            if (A_init.min() < 0 or A_init.max() >= p):
                raise ValueError("A_init contains wrong index.")

        # Group:
        if group is None:
            g_index = list(range(p))
        else:
            group = np.array(group)
            if group.ndim > 1:
                raise ValueError("group should be an 1D array of integers.")
            if group.size != p:
                raise ValueError(
                    "The length of group should be equal to X.shape[1].")
            g_index = []
            group.sort()
            group_set = list(set(group))
            j = 0
            for i in group_set:
                while group[j] != i:
                    j += 1
                g_index.append(j)

        # Weight:
        if weight is None:
            weight = np.ones(n)
        else:
            weight = np.array(weight)
            if weight.dtype not in ("int", "float"):
                raise ValueError("weight should be numeric.")
            if weight.ndim > 1:
                raise ValueError("weight should be a 1-D array.")
            if weight.size != n:
                raise ValueError("X.shape[0] should be equal to weight.size")

        # alpha
        if self.alpha is None:
            alphas = [0]
        else:
            if isinstance(self.alpha, (numbers.Real, numbers.Integral)):
                alphas = np.empty(1, dtype=float)
                alphas[0] = self.alpha
            else:
                alphas = self.alpha

        # Exchange_num
        if (not isinstance(self.exchange_num, int) or self.exchange_num <= 0):
            raise ValueError("exchange_num should be an positive integer.")

        # screening
        if self.screening_size != -1:
            if self.screening_size == 0:
                self.screening_size = min(
                    p, int(n / (np.log(np.log(n)) * np.log(p))))
            elif self.screening_size > p:
                raise ValueError(
                    "screening size should be smaller than X.shape[1].")

        # Primary fit parameters
        if (not isinstance(self.primary_model_fit_max_iter, int)
                or self.primary_model_fit_max_iter <= 0):
            raise ValueError(
                "primary_model_fit_max_iter should be an positive integer.")
        if self.primary_model_fit_epsilon < 0:
            raise ValueError(
                "primary_model_fit_epsilon should be non-negative.")

        # Thread
        if (not isinstance(self.thread, int) or self.thread < 0):
            raise ValueError("thread should be positive number or 0"
                             " (maximum supported by your device).")

        # Splicing type
        if self.splicing_type not in (0, 1, 2):
            raise ValueError("splicing type should be 0, 1 or 2.")

        # Important_search
        if (not isinstance(self.important_search, int)
                or self.important_search < 0):
            raise ValueError(
                "important_search should be a non-negative number.")

        # Sparse X
        if self.sparse_matrix:
            if not isinstance(X, (coo_matrix)):
                # print("sparse matrix 1")
                nonzero = 0
                tmp = np.zeros([X.shape[0] * X.shape[1], 3])
                for j in range(X.shape[1]):
                    for i in range(X.shape[0]):
                        if X[i, j] != 0.:
                            tmp[nonzero, :] = np.array([X[i, j], i, j])
                            nonzero += 1
                X = tmp[:nonzero, :]
            else:
                # print("sparse matrix 2")
                tmp = np.zeros([len(X.data), 3])
                tmp[:, 1] = X.row
                tmp[:, 2] = X.col
                tmp[:, 0] = X.data

                ind = np.lexsort((tmp[:, 2], tmp[:, 1]))
                X = tmp[ind, :]

        # normalize
        normalize = 0
        if is_normal:
            normalize = self.normalize_type

        # always_select
        if self.always_select is None:
            always_select_list = np.zeros(0, dtype="int32")
        else:
            always_select_list = np.array(self.always_select, dtype="int32")

        # train_test
        if self.split_train_test is False or train_test_id is None:
            train_test_id = np.array([], dtype="int32")
        else:
            train_test_id = np.array(train_test_id, dtype="int32")
            train_size = (train_test_id == 0).sum()
            test_size = (train_test_id == 1).sum()
            if (train_size == 0 or test_size == 0
                    or train_size + test_size < X.shape[0]):
                raise ValueError("train_test_id is invalid.")

        # unused
        early_stop = False
        self.n_iter_ = self.max_iter

        # wrap with cpp
        if n == 1:
            # with only one sample, nothing to be estimated
            result = [np.zeros((p, M)), np.zeros(M), 0, 0, 0]
        else:
            result = pywrap_GLM(
                X, y, weight, n, p, normalize, algorithm_type_int,
                model_type_int,
                self.max_iter, self.exchange_num, tune_type_int,
                self.ic_coef, g_index, alphas, self.screening_size,
                always_select_list, self.primary_model_fit_max_iter,
                self.primary_model_fit_epsilon, early_stop,
                self.approximate_Newton, self.thread, self.covariance_update,
                self.sparse_matrix, self.splicing_type, self.important_search,
                A_init, init_max_s, self.split_train_test, train_test_id,
                return_path,
                self.init_type, self.init_gs_start, max_s)

        # print("linear fit end")
        # print(len(result))
        # print(result)
        self.coef_ = result[0].squeeze()
        self.intercept_ = result[1].squeeze()
        if return_path:
            self.path_ = result[2]

        if self.model_type == "Cox":
            self.baseline_model.fit(np.dot(X, self.coef_), y, time)
        if self.model_type == "Ordinal" and self.coef_.ndim > 1:
            self.coef_ = self.coef_[:, 0]

        return self

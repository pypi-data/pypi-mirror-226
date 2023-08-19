from .linear import (
    LinearRegression,
    LogisticRegression,
    CoxPHSurvivalAnalysis,
    PoissonRegression,
    MultiTaskRegression,
    MultinomialRegression,
    GammaRegression,
    OrdinalRegression
)
# from .decomposition import (SparsePCA, RobustPCA)
from .datasets import (make_glm_data, make_multivariate_glm_data)

__version__ = "0.0.1rc1"
__author__ = "Junxian Zhu, Jin Zhu, Junhao Huang, Heping Zhang, Xueqin Wang"

__all__ = [
    # linear
    "LinearRegression",
    "LogisticRegression",
    "CoxPHSurvivalAnalysis",
    "PoissonRegression",
    "MultiTaskRegression",
    "MultinomialRegression",
    "GammaRegression",
    "OrdinalRegression",
    # decomposition
    # "SparsePCA",
    # "RobustPCA",
    # datasets
    "make_glm_data",
    "make_multivariate_glm_data"
]
